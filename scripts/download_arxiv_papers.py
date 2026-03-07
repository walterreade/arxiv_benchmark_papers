#!/usr/bin/env python3
"""
arXiv Bias Paper Downloader

Queries the last 1000 CS papers from arXiv, uses Gemini to classify which ones
measure bias in NLP/LLMs, downloads qualifying papers, and updates llm_bias_papers.csv.
"""

import argparse
import csv
import json
import os
import random
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

from shared import (
    genai, types,
    ResourceExhaustedError,
    ErrorTracker, RateLimiter,
)


SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent

OUTPUT_DIR = "pdf"
CSV_FILE = "csv/llm_bias_papers.csv"
ASSESSMENT_CACHE_FILE = "csv/download_assessments_cache.json"
SNAPSHOT_FILE = "arxiv-metadata-oai-snapshot.json"
ARXIV_API_URL = "http://export.arxiv.org/api/query"

MAX_PAPERS = 2000
RESULTS_PER_PAGE = 200
DELAY_BETWEEN_API_PAGES = 3  # seconds between arxiv API requests
DELAY_BETWEEN_DOWNLOADS = 3  # seconds between PDF downloads
GEMINI_MODEL = "gemini-3-flash-preview"
BATCH_SIZE = 25


# ---------------------------------------------------------------------------
# Snapshot & Cache helpers
# ---------------------------------------------------------------------------

def load_snapshot_ids(snapshot_path: str) -> set[str]:
    """Load all arXiv IDs from the JSONL snapshot file.

    The file is ~5GB so we stream line-by-line and only keep the 'id' field.
    """
    ids = set()
    if not os.path.isfile(snapshot_path):
        return ids

    print(f"  Loading snapshot IDs from {snapshot_path}...")
    with open(snapshot_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                paper = json.loads(line)
                arxiv_id = paper.get('id', '')
                if arxiv_id:
                    ids.add(arxiv_id)
            except json.JSONDecodeError:
                continue
    print(f"  Loaded {len(ids):,} snapshot IDs.")
    return ids


def load_assessment_cache(cache_path: str) -> dict[str, bool]:
    """Load Gemini assessment cache: {arxiv_id: bool}."""
    if not os.path.isfile(cache_path):
        return {}
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_assessment_cache(cache: dict[str, bool], cache_path: str):
    """Persist the assessment cache to disk."""
    os.makedirs(os.path.dirname(cache_path) or '.', exist_ok=True)
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2)


# ---------------------------------------------------------------------------
# arXiv API
# ---------------------------------------------------------------------------

def fetch_recent_cs_papers(max_papers: int = MAX_PAPERS,
                           per_page: int = RESULTS_PER_PAGE) -> list[dict]:
    """Fetch the most recent CS papers from arXiv API."""
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    all_papers = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for start in range(0, max_papers, per_page):
        batch_size = min(per_page, max_papers - start)
        url = (
            f"{ARXIV_API_URL}?search_query=cat:cs.*"
            f"&sortBy=submittedDate&sortOrder=descending"
            f"&start={start}&max_results={batch_size}"
        )
        print(f"  Fetching papers {start + 1}-{start + batch_size}...")

        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  Error fetching page: {e}")
            break

        root = ET.fromstring(resp.content)
        entries = root.findall('atom:entry', ns)

        if not entries:
            print("  No more entries returned.")
            break

        for entry in entries:
            id_text = entry.find('atom:id', ns).text  # http://arxiv.org/abs/XXXX.XXXXXvN
            arxiv_id = id_text.split('/abs/')[-1]
            # Strip version suffix (e.g. v1, v2)
            arxiv_id = re.sub(r'v\d+$', '', arxiv_id)

            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None else "Unknown"
            # Collapse multiple spaces
            title = re.sub(r'\s+', ' ', title)

            summary_elem = entry.find('atom:summary', ns)
            abstract = summary_elem.text.strip() if summary_elem is not None else ""

            published = entry.find('atom:published', ns)
            updated = entry.find('atom:updated', ns)
            pub_date = published.text[:10] if published is not None else ""
            upd_date = updated.text[:10] if updated is not None else pub_date

            all_papers.append({
                'arxiv_id': arxiv_id,
                'title': title,
                'abstract': abstract,
                'published': pub_date,
                'updated': upd_date,
            })

        print(f"  Got {len(entries)} entries (total so far: {len(all_papers)})")

        if len(entries) < batch_size:
            break

        if start + per_page < max_papers:
            time.sleep(DELAY_BETWEEN_API_PAGES)

    return all_papers


# ---------------------------------------------------------------------------
# Gemini classification (same criteria as 1st_pass_analyze_abstracts.py)
# ---------------------------------------------------------------------------

def classify_batch(batch: list[dict], api_key: str, rate_limiter: RateLimiter,
                   model_name: str, error_tracker: ErrorTracker,
                   max_retries: int = 3) -> list[bool]:
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
                print(f"  Warning: got {len(results)} results for {len(batch)} abstracts, padding.")
                return (results + [False] * len(batch))[:len(batch)]
            else:
                print(f"  Warning: unexpected response type: {type(results)}")
                return [False] * len(batch)

        except Exception as e:
            last_exception = e
            error_str = str(e).lower()

            if "resource exhausted" in error_str or "429" in error_str or "quota" in error_str:
                print(f"  Rate limited, attempt {attempt + 1}/{max_retries}")
                if error_tracker.record_resource_exhausted():
                    raise ResourceExhaustedError("Too many resource exhausted errors.")
                backoff = (2 ** attempt) * 5 + random.uniform(0, 2)
                time.sleep(backoff)
            elif "500" in error_str or "503" in error_str or "server" in error_str:
                print(f"  Server error, attempt {attempt + 1}/{max_retries}")
                backoff = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(backoff)
            else:
                raise e

    raise last_exception


# ---------------------------------------------------------------------------
# PDF download
# ---------------------------------------------------------------------------

def download_pdf(arxiv_id: str, output_dir: str) -> bool:
    """Download a PDF for a given arXiv ID."""
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    output_path = os.path.join(output_dir, f"{arxiv_id}.pdf")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"  Downloading {arxiv_id}...", end=' ')
        response = requests.get(pdf_url, headers=headers, timeout=60)
        response.raise_for_status()

        if len(response.content) < 1000:
            print(f"✗ Error: Downloaded file too small ({len(response.content)} bytes)")
            return False

        with open(output_path, 'wb') as f:
            f.write(response.content)

        print(f"✓ ({len(response.content) / 1024:.1f} KB)")
        return True

    except requests.RequestException as e:
        print(f"✗ Error: {e}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Download arXiv CS papers that measure bias in NLP/LLMs."
    )
    parser.add_argument("--max-papers", type=int, default=MAX_PAPERS,
                        help=f"Number of recent CS papers to query (default {MAX_PAPERS})")
    parser.add_argument("--output-dir", default=OUTPUT_DIR,
                        help=f"Directory to save PDFs (default {OUTPUT_DIR})")
    parser.add_argument("--csv", default=CSV_FILE,
                        help=f"CSV to append positive results (default {CSV_FILE})")
    parser.add_argument("--model", default=GEMINI_MODEL,
                        help=f"Gemini model for classification (default {GEMINI_MODEL})")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE,
                        help=f"Abstracts per Gemini request (default {BATCH_SIZE})")
    parser.add_argument("--rpm", type=int, default=30,
                        help="Gemini requests per minute (default 30)")
    parser.add_argument("--cache", default=ASSESSMENT_CACHE_FILE,
                        help=f"JSON cache for Gemini assessments (default {ASSESSMENT_CACHE_FILE})")
    parser.add_argument("--snapshot", default=SNAPSHOT_FILE,
                        help=f"arXiv metadata snapshot JSONL file (default {SNAPSHOT_FILE})")
    parser.add_argument("--max-errors", type=int, default=5,
                        help="Max resource exhausted errors before exit (default 5)")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        sys.exit(1)

    print("=" * 70)
    print("arXiv Bias Paper Downloader")
    print("=" * 70)

    # Ensure output dirs exist
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    os.makedirs(os.path.dirname(args.csv) or '.', exist_ok=True)

    # Step 1: Load snapshot IDs and assessment cache
    print(f"\nStep 1: Loading snapshot and cache...")
    print("-" * 40)
    snapshot_ids = load_snapshot_ids(args.snapshot)
    assessment_cache = load_assessment_cache(args.cache)
    print(f"  Assessment cache: {len(assessment_cache):,} entries")

    # Step 2: Fetch recent CS papers
    print(f"\nStep 2: Fetching last {args.max_papers} CS papers from arXiv API...")
    print("-" * 40)
    papers = fetch_recent_cs_papers(max_papers=args.max_papers)
    print(f"\nFetched {len(papers)} papers.")

    if not papers:
        print("No papers fetched. Exiting.")
        return

    # Step 3: Filter out papers already in snapshot, cache, or downloaded
    existing_pdfs = {f.stem for f in Path(args.output_dir).glob("*.pdf")}
    all_paper_ids = {p['arxiv_id'] for p in papers}

    skip_ids = existing_pdfs | set(assessment_cache.keys()) | snapshot_ids
    new_papers = [p for p in papers if p['arxiv_id'] not in skip_ids]

    # Also identify papers that were cached as positive but not yet downloaded
    cached_positive_not_downloaded = [
        p for p in papers
        if assessment_cache.get(p['arxiv_id']) is True
        and p['arxiv_id'] not in existing_pdfs
        and p['arxiv_id'] not in snapshot_ids
    ]

    print(f"\nStep 3: Filtering...")
    print(f"  In snapshot:          {len(snapshot_ids & all_paper_ids)}")
    print(f"  Already downloaded:   {len(existing_pdfs & all_paper_ids)}")
    print(f"  Previously assessed:  {len(set(assessment_cache.keys()) & all_paper_ids)}")
    print(f"  New papers to assess: {len(new_papers)}")
    if cached_positive_not_downloaded:
        print(f"  Cached positive, not yet downloaded: {len(cached_positive_not_downloaded)}")

    if not new_papers and not cached_positive_not_downloaded:
        print("\nAll papers already processed. Nothing to do.")
        return

    # Step 4: Classify new papers with Gemini
    qualifying_papers = list(cached_positive_not_downloaded)  # start with cached positives needing download

    if new_papers:
        print(f"\nStep 4: Classifying {len(new_papers)} abstracts with Gemini...")
        print("-" * 40)

        rate_limiter = RateLimiter(max_calls=args.rpm, period=60.0)
        error_tracker = ErrorTracker(max_errors=args.max_errors)

        batches = [new_papers[i:i + args.batch_size]
                   for i in range(0, len(new_papers), args.batch_size)]

        for batch_idx, batch in enumerate(batches):
            print(f"  Batch {batch_idx + 1}/{len(batches)} ({len(batch)} papers)...", end=' ')

            try:
                results = classify_batch(batch, api_key, rate_limiter, args.model, error_tracker)
                positives = sum(results)
                print(f"{positives} qualifying")

                for paper, is_bias in zip(batch, results):
                    assessment_cache[paper['arxiv_id']] = bool(is_bias)
                    if is_bias:
                        qualifying_papers.append(paper)

                # Flush cache after each batch so progress is not lost
                save_assessment_cache(assessment_cache, args.cache)

            except ResourceExhaustedError:
                print("\nStopping classification due to too many API errors.")
                save_assessment_cache(assessment_cache, args.cache)
                break
            except Exception as e:
                print(f"error: {e}")
                save_assessment_cache(assessment_cache, args.cache)

        print(f"\nFound {len(qualifying_papers)} qualifying bias papers "
              f"({len(qualifying_papers) - len(cached_positive_not_downloaded)} new + "
              f"{len(cached_positive_not_downloaded)} cached).")
    else:
        print(f"\nStep 4: No new papers to classify.")
        if cached_positive_not_downloaded:
            print(f"  {len(cached_positive_not_downloaded)} cached positive papers still need downloading.")

    if not qualifying_papers:
        print("No bias papers to download.")
        return

    # Step 4: Download PDFs
    print(f"\nStep 5: Downloading {len(qualifying_papers)} PDFs...")
    print("-" * 40)

    downloaded = 0
    failed = 0

    for i, paper in enumerate(qualifying_papers):
        result = download_pdf(paper['arxiv_id'], args.output_dir)
        if result:
            downloaded += 1
        else:
            failed += 1

        if i < len(qualifying_papers) - 1:
            time.sleep(DELAY_BETWEEN_DOWNLOADS)

    # Step 6: Update CSV
    print(f"\nStep 6: Updating {args.csv}...")
    fieldnames = ["paper_id", "latest_date", "title"]
    csv_exists = os.path.isfile(args.csv)

    # Load existing IDs to avoid duplicates
    existing_csv_ids = set()
    if csv_exists:
        with open(args.csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_csv_ids.add(row.get('paper_id', ''))

    new_csv_rows = []
    for paper in qualifying_papers:
        if paper['arxiv_id'] not in existing_csv_ids:
            new_csv_rows.append({
                'paper_id': paper['arxiv_id'],
                'latest_date': paper['updated'],
                'title': paper['title'],
            })

    if new_csv_rows:
        with open(args.csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not csv_exists:
                writer.writeheader()
            writer.writerows(new_csv_rows)
        print(f"  Added {len(new_csv_rows)} new entries to {args.csv}")
    else:
        print(f"  No new entries to add (all already in CSV).")

    # Summary
    print("\n" + "=" * 70)
    print("Done!")
    print("=" * 70)
    print(f"  Papers queried:     {len(papers)}")
    print(f"  Already downloaded: {len(papers) - len(new_papers)}")
    print(f"  Classified:         {len(new_papers)}")
    print(f"  Qualifying:         {len(qualifying_papers)}")
    print(f"  Downloaded:         {downloaded}")
    print(f"  Failed:             {failed}")
    print(f"  CSV entries added:  {len(new_csv_rows)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
