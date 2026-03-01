#!/usr/bin/env python3
"""
1st pass analysis of arxiv abstracts to find papers measuring bias in NLP/LLMs.

Reads CS abstracts (2015+) from arxiv-metadata-oai-snapshot.json, sends batches
to Gemini 3.0 Flash for classification, and incrementally writes matches to
csv/llm_bias_papers.csv.

Progress is tracked in csv/llm_bias_abstracts_progress.txt so the script can
be resumed safely.
"""

import argparse
import csv
import json
import os
import random
import sys
import time
import threading
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from shared import (
    genai, types,
    ResourceExhaustedError,
    ErrorTracker, RateLimiter,
)


SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
METADATA_FILE = PROJECT_DIR / "arxiv-metadata-oai-snapshot.json"

BATCH_SIZE = 25


def parse_version_date(created_str: str) -> str:
    """Parse arxiv version date string to YYYY-MM-DD format.
    
    Input format: 'Mon, 2 Apr 2007 19:18:42 GMT'
    """
    MONTHS = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
        'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
        'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12',
    }
    try:
        parts = created_str.split()
        day = parts[1].zfill(2)
        month = MONTHS.get(parts[2].lower()[:3], '01')
        year = parts[3]
        return f"{year}-{month}-{day}"
    except (IndexError, KeyError):
        return ""


def load_processed_ids(progress_file: str) -> set:
    """Load set of paper IDs already processed."""
    if not os.path.exists(progress_file):
        return set()
    with open(progress_file, 'r') as f:
        return set(line.strip() for line in f if line.strip())


def load_cs_abstracts_2015(metadata_file: str, processed_ids: set) -> list:
    """Load CS abstracts from 2015+ that haven't been processed yet."""
    papers = []
    skipped = 0

    with open(metadata_file) as f:
        for line in tqdm(f, desc="Loading abstracts", unit=" papers"):
            d = json.loads(line)
            paper_id = d.get('id', '')

            if paper_id in processed_ids:
                skipped += 1
                continue

            cats = d.get('categories', '')
            if 'cs.' not in cats.lower():
                continue

            versions = d.get('versions', [])
            if not versions:
                continue
            created = versions[0].get('created', '')
            parts = created.split()
            if len(parts) < 4:
                continue
            try:
                year = int(parts[3])
            except ValueError:
                continue
            if year < 2015:
                continue

            # Use update_date if available, otherwise parse latest version date
            latest_date = d.get('update_date', '')
            if not latest_date and versions:
                latest_date = parse_version_date(versions[-1].get('created', ''))

            abstract = d.get('abstract', '').strip()
            title = d.get('title', '').strip().replace('\n', ' ')

            papers.append({
                'id': paper_id,
                'title': title,
                'abstract': abstract,
                'latest_date': latest_date,
            })

    print(f"Loaded {len(papers):,} CS abstracts (2015+). Skipped {skipped:,} already processed.")
    return papers


def classify_batch(batch: list, api_key: str, rate_limiter: RateLimiter,
                   model_name: str, error_tracker: ErrorTracker,
                   max_retries: int = 3) -> list:
    """Classify a batch of abstracts. Returns list of bools (True = bias paper)."""
    if error_tracker.check_exit():
        raise ResourceExhaustedError("Too many errors, stopping.")

    abstracts_text = ""
    for i, paper in enumerate(batch):
        abstracts_text += f"[{i}] Title: {paper['title']}\nAbstract: {paper['abstract']}\n\n"

    prompt = f"""You are classifying academic paper abstracts. For each abstract below, determine whether the paper measures, evaluates, or benchmarks bias or fairness in Natural Language Processing (NLP), Language Models (LMs), or Large Language Models (LLMs).

A paper qualifies if it:
- Proposes or uses a benchmark/dataset for measuring bias in language models or NLP systems
- Evaluates social biases (gender, race, religion, etc.) in language models or NLP outputs
- Studies fairness or discrimination in NLP/LLM systems
- Proposes methods to detect or measure bias in text generation, classification, or other NLP tasks

A paper does NOT qualify if it:
- Only mentions bias in passing or as future work
- Deals with statistical/mathematical bias (not social bias), e.g. inductive bias, selection bias in sampling
- Studies bias in non-NLP domains (computer vision only, recommender systems without text, etc.)
- Only proposes debiasing methods without measuring bias

Return a JSON array of {len(batch)} booleans (true/false), one per abstract in order.

{abstracts_text}"""

    client = genai.Client(api_key=api_key)

    rate_limiter.wait_for_token()

    last_exception = None
    for attempt in range(max_retries):
        try:
            if error_tracker.check_exit():
                raise ResourceExhaustedError("Too many errors, stopping.")

            response = client.models.generate_content(
                model=model_name,
                contents=[prompt],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            results = json.loads(response.text)

            if isinstance(results, list) and len(results) == len(batch):
                return results
            elif isinstance(results, list):
                tqdm.write(f"  Warning: got {len(results)} results for {len(batch)} abstracts, padding.")
                return (results + [False] * len(batch))[:len(batch)]
            else:
                tqdm.write(f"  Warning: unexpected response type: {type(results)}")
                return [False] * len(batch)

        except Exception as e:
            last_exception = e
            error_str = str(e).lower()

            if "resource exhausted" in error_str or "429" in error_str or "quota" in error_str:
                tqdm.write(f"  Rate limited on batch, attempt {attempt + 1}/{max_retries}")
                if error_tracker.record_resource_exhausted():
                    raise ResourceExhaustedError("Too many resource exhausted errors.")
                backoff = (2 ** attempt) * 5 + random.uniform(0, 2)
                time.sleep(backoff)
            elif "500" in error_str or "503" in error_str or "server" in error_str:
                tqdm.write(f"  Server error on batch, attempt {attempt + 1}/{max_retries}")
                backoff = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(backoff)
            else:
                raise e

    raise last_exception


def process_batch(batch: list, api_key: str, rate_limiter: RateLimiter,
                  model_name: str, error_tracker: ErrorTracker) -> tuple:
    """Process a single batch. Returns (positive_papers, all_ids)."""
    try:
        results = classify_batch(batch, api_key, rate_limiter, model_name, error_tracker)
        positives = []
        all_ids = []
        for paper, is_bias in zip(batch, results):
            all_ids.append(paper['id'])
            if is_bias:
                positives.append({
                    'paper_id': paper['id'],
                    'latest_date': paper['latest_date'],
                    'title': paper['title'],
                })
        return positives, all_ids, None
    except ResourceExhaustedError as e:
        return [], [p['id'] for p in batch], str(e)
    except Exception as e:
        tqdm.write(f"  Batch error: {e}")
        return [], [], str(e)


def main():
    parser = argparse.ArgumentParser(
        description="Classify arxiv CS abstracts (2015+) for bias in NLP/LLMs using Gemini."
    )
    parser.add_argument("--metadata", default=str(METADATA_FILE),
                        help="Path to arxiv-metadata-oai-snapshot.json")
    parser.add_argument("--output", default="csv/llm_bias_papers.csv",
                        help="Output CSV for positive results")
    parser.add_argument("--progress", default="csv/llm_bias_abstracts_progress.txt",
                        help="File tracking processed paper IDs")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE,
                        help=f"Abstracts per Gemini request (default {BATCH_SIZE})")
    parser.add_argument("--rpm", type=int, default=200,
                        help="Requests per minute (default 200)")
    parser.add_argument("--workers", type=int, default=16,
                        help="Number of worker threads (default 16)")
    parser.add_argument("--model", default="gemini-3-flash-preview",
                        help="Gemini model name (default gemini-3-flash-preview)")
    parser.add_argument("--max-errors", type=int, default=10,
                        help="Max resource exhausted errors before exit (default 10)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit number of abstracts to process (0 = all)")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        sys.exit(1)

    # Ensure output directories exist
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    os.makedirs(os.path.dirname(args.progress) or '.', exist_ok=True)

    # Load progress
    processed_ids = load_processed_ids(args.progress)
    print(f"Found {len(processed_ids):,} already processed paper IDs.")

    # Load abstracts
    papers = load_cs_abstracts_2015(args.metadata, processed_ids)
    if not papers:
        print("No new abstracts to process.")
        return

    if args.limit > 0:
        papers = papers[:args.limit]
        print(f"Limited to {len(papers):,} abstracts.")

    # Create batches
    batches = [papers[i:i + args.batch_size] for i in range(0, len(papers), args.batch_size)]
    print(f"Created {len(batches):,} batches of up to {args.batch_size} abstracts.")

    # Initialize rate limiter and error tracker
    max_workers = min(args.workers, args.rpm)
    rate_limiter = RateLimiter(max_calls=args.rpm, period=60.0)
    error_tracker = ErrorTracker(max_errors=args.max_errors)

    # Locks for file writing
    csv_lock = threading.Lock()

    # CSV setup
    fieldnames = ["paper_id", "latest_date", "title"]
    csv_exists = os.path.isfile(args.output)

    total_positives = 0
    total_processed = 0

    with open(args.output, mode='a', newline='', encoding='utf-8') as csv_f, \
         open(args.progress, mode='a') as prog_f:

        writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
        if not csv_exists:
            writer.writeheader()
            csv_f.flush()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_batch = {
                executor.submit(
                    process_batch, batch, api_key, rate_limiter, model_name=args.model,
                    error_tracker=error_tracker
                ): batch
                for batch in batches
            }

            for future in tqdm(as_completed(future_to_batch), total=len(batches),
                               desc="Classifying", unit=" batch"):
                if error_tracker.check_exit():
                    tqdm.write("Exiting due to too many resource exhausted errors.")
                    executor.shutdown(wait=False, cancel_futures=True)
                    break

                try:
                    positives, all_ids, error = future.result()

                    with csv_lock:
                        # Write positive results to CSV
                        for row in positives:
                            writer.writerow(row)
                        if positives:
                            csv_f.flush()

                        # Record all processed IDs
                        for pid in all_ids:
                            prog_f.write(pid + '\n')
                        if all_ids:
                            prog_f.flush()

                    total_positives += len(positives)
                    total_processed += len(all_ids)

                    if error:
                        tqdm.write(f"  Batch error: {error}")

                except Exception as exc:
                    tqdm.write(f"  Batch exception: {exc}")

    # Summary
    print(f"\nDone. Processed {total_processed:,} abstracts in this run.")
    print(f"Found {total_positives:,} bias-related papers.")
    print(f"Results appended to {args.output}")


if __name__ == "__main__":
    main()
