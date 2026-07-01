#!/usr/bin/env python3
"""
3rd pass analysis: Extract bias targets from papers that are both LLM-related and bias-related.

This script:
1. Reads JSON files from 2_paper_metadata where both is_llm_related and is_bias_related are true
2. Uploads the corresponding PDF to Gemini for analysis
3. Extracts bias_targets list and primary_bias_target
4. Saves results to 3_paper_bias_targets
"""

import os
import argparse
import csv
import json
import time
import glob
import random
import sys
import threading
from pathlib import Path
from typing import Optional
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from shared import (
    genai, types,
    ResourceExhaustedError, IterationTimeoutError, ITERATION_TIMEOUT, HTTP_TIMEOUT,
    ErrorTracker, RateLimiter,
    load_failed_files, save_json,
    unsanitize_arxiv_id,
)

DEFAULT_MODEL = "gemini-3.1-pro-preview"

PROMPT = """
Analyze this academic paper and identify what types of bias are being measured or evaluated.

Return the results in JSON format with these fields:

1. `bias_targets`: list of objects. Each object describes a bias type that the paper measures or evaluates, with two fields:
   - `target`: string. The category of bias (e.g., "Gender bias", "Racial bias", "Religious bias", "Age bias", "Political bias", "Nationality bias", "Socioeconomic bias", "Disability bias", "Sexual orientation bias", "Cultural bias", "Language bias"). Use concise, descriptive category names.
   - `methodology`: string. A brief description of how the paper measures or evaluates this bias (e.g., "Sentiment analysis of model outputs across demographic groups", "Counterfactual name substitution in prompts", "Multiple-choice stereotype association tests", "Comparing model recommendations across religious identities").
   Include ALL bias types the paper measures.

2. `primary_bias_target`: string. The single primary bias target that is the main focus of the paper.
   - If the paper has a clear primary focus (e.g., it is primarily about gender bias even if it also touches on other biases), use that bias category (e.g., "Gender bias").
   - If the paper measures multiple biases without a clear primary target (e.g., a general fairness benchmark covering many bias types equally), use "No Primary Bias Target".

Make sure the output is valid JSON.
"""


def analyze_bias_targets(pdf_path: str, api_key: str, model_name: str,
                         rate_limiter: RateLimiter, error_tracker: ErrorTracker,
                         max_retries: int = 3) -> dict:
    """Analyze a PDF to extract bias targets using Gemini API."""
    client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=HTTP_TIMEOUT))
    sample_file = None

    # Check if we should exit before starting
    if error_tracker.check_exit():
        raise ResourceExhaustedError("Too many resource exhausted errors, stopping.")

    # Acquire rate limit token
    rate_limiter.wait_for_token()

    try:
        tqdm.write(f"Uploading {Path(pdf_path).name}...")

        with open(pdf_path, 'rb') as f:
            sample_file = client.files.upload(
                file=f,
                config=types.UploadFileConfig(
                    display_name=Path(pdf_path).name,
                    mime_type='application/pdf'
                )
            )

        # Wait for processing with timeout
        processing_start = time.time()
        while sample_file.state.name == "PROCESSING":
            if time.time() - processing_start > ITERATION_TIMEOUT:
                raise IterationTimeoutError(f"File processing timed out after {ITERATION_TIMEOUT}s")
            time.sleep(1)
            sample_file = client.files.get(name=sample_file.name)

        if sample_file.state.name == "FAILED":
            raise ValueError("File upload failed.")

        # Retry logic with exponential backoff
        last_exception = None
        for attempt in range(max_retries):
            try:
                if error_tracker.check_exit():
                    raise ResourceExhaustedError("Too many resource exhausted errors, stopping.")

                response = client.models.generate_content(
                    model=model_name,
                    contents=[sample_file, PROMPT],
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                result_text = response.text
                return json.loads(result_text)

            except json.JSONDecodeError:
                tqdm.write(f"  Malformed JSON on {Path(pdf_path).name}, attempt {attempt + 1}/{max_retries}")
                if attempt == max_retries - 1:
                    return {"raw_response": result_text}
            except Exception as e:
                last_exception = e
                error_str = str(e).lower()

                if "resource exhausted" in error_str or "429" in error_str or "quota" in error_str:
                    tqdm.write(f"  Resource exhausted on {Path(pdf_path).name}, attempt {attempt + 1}/{max_retries}")
                    if error_tracker.record_resource_exhausted():
                        raise ResourceExhaustedError("Too many resource exhausted errors, stopping.")
                    backoff = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(backoff)
                elif "500" in error_str or "503" in error_str or "server" in error_str:
                    tqdm.write(f"  Server error on {Path(pdf_path).name}, attempt {attempt + 1}/{max_retries}")
                    backoff = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(backoff)
                else:
                    raise e

        # All retries exhausted
        raise last_exception

    finally:
        try:
            if sample_file is not None:
                client.files.delete(name=sample_file.name)
        except Exception as e:
            tqdm.write(f"Warning: Failed to delete file {sample_file.name}: {e}")
        rate_limiter.release_slot()


def process_single_file(pdf_path: str, api_key: str, json_dir: str, model_name: str,
                        rate_limiter: RateLimiter, error_tracker: ErrorTracker,
                        first_pass_data: dict) -> tuple[Optional[dict], Optional[str]]:
    """Process a single file. Returns (result_dict, None) if successful, (None, error_msg) if failed."""
    filename = Path(pdf_path).name
    try:
        if error_tracker.check_exit():
            return None, "Exiting due to too many resource exhausted errors"

        analysis = analyze_bias_targets(pdf_path, api_key, model_name, rate_limiter, error_tracker)

        # Save to JSON
        url_slug = filename.replace('.pdf', '')
        url_slug = unsanitize_arxiv_id(url_slug)
        json_data = {
            "filename": filename,
            "title": first_pass_data.get("title", ""),
            "arxiv_url": f"https://arxiv.org/pdf/{url_slug}",
            **analysis
        }
        save_json(json_data, json_dir, filename)

        return json_data, None

    except ResourceExhaustedError as e:
        return None, str(e)
    except Exception as e:
        tqdm.write(f"  Error processing {filename}: {e}")
        return None, str(e)


def load_eligible_papers(first_pass_dir: str, skip_filenames: set[str] = None) -> list[dict]:
    """Load eligible papers. Uses CSV for fast filtering when available.

    If skip_filenames is provided, only loads JSON for papers NOT in that set,
    avoiding expensive NFS reads for already-processed papers.
    """
    import csv
    csv_path = "utility_files/1st_pass_results.csv"

    eligible_filenames = set()
    if os.path.isfile(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                if (row.get('is_llm_related', '').lower() == 'true' and
                        row.get('is_bias_related', '').lower() == 'true'):
                    eligible_filenames.add(row['filename'])
        print(f"  CSV fast-path: {len(eligible_filenames)} eligible from CSV.")
    else:
        json_files = glob.glob(os.path.join(first_pass_dir, "*.json"))
        for jf in json_files:
            try:
                with open(jf, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if data.get('is_llm_related') is True and data.get('is_bias_related') is True:
                    eligible_filenames.add(Path(jf).stem + '.pdf')
            except (json.JSONDecodeError, IOError):
                continue
        print(f"  JSON scan: {len(eligible_filenames)} eligible papers found.")

    if skip_filenames:
        to_load = eligible_filenames - skip_filenames
        print(f"  Skipping {len(eligible_filenames) - len(to_load)} already processed/failed. Loading {len(to_load)} JSON files.")
    else:
        to_load = eligible_filenames

    eligible = []
    for filename in to_load:
        stem = Path(filename).stem
        jf = os.path.join(first_pass_dir, stem + ".json")
        if os.path.isfile(jf):
            try:
                with open(jf, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data['_source_path'] = jf
                data['_filename'] = filename
                eligible.append(data)
            except (json.JSONDecodeError, IOError):
                continue

    return eligible


def main():
    parser = argparse.ArgumentParser(description="3rd pass: Extract bias targets from LLM+bias papers.")
    parser.add_argument("--first_pass_dir", default="json/2_paper_metadata", help="Directory with paper metadata JSON files")
    parser.add_argument("--pdf_dir", default="pdf", help="Directory containing PDFs")
    parser.add_argument("--json_dir", default="json/3_paper_bias_targets", help="Directory to save bias targets JSON analysis")
    parser.add_argument("--failures", default="utility_files/2nd_pass_failures.csv", help="CSV file to track failed files")
    parser.add_argument("--reprocess", action="store_true", help="Re-analyze all files, ignoring existing results")
    parser.add_argument("--rpm", type=int, default=20, help="Requests per minute (API rate limit).")
    parser.add_argument("--workers", type=int, default=10, help="Number of worker threads.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Gemini model name.")
    parser.add_argument("--max-errors", type=int, default=1, help="Max resource exhausted errors before exit.")

    args = parser.parse_args()

    first_pass_dir = args.first_pass_dir
    pdf_dir = args.pdf_dir
    json_dir = args.json_dir
    failures_csv = args.failures
    reprocess = args.reprocess
    rpm = args.rpm
    max_workers = min(args.workers, rpm)
    model_name = args.model
    max_errors = args.max_errors

    # Create output directory
    os.makedirs(json_dir, exist_ok=True)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return

    # Load previously failed files
    failed_files = load_failed_files(failures_csv)
    print(f"Previously failed (will skip): {len(failed_files)}")

    # Check for already processed
    processed_filenames = set()
    if not reprocess and os.path.exists(json_dir):
        existing_jsons = glob.glob(os.path.join(json_dir, "*.json"))
        for jp in existing_jsons:
            processed_filenames.add(Path(jp).stem + ".pdf")
    print(f"Already processed: {len(processed_filenames)}")

    # Load eligible papers, skipping already-processed to avoid unnecessary NFS reads
    skip_filenames = processed_filenames | failed_files if not reprocess else None
    print(f"Loading papers from {first_pass_dir}...")
    eligible = load_eligible_papers(first_pass_dir, skip_filenames=skip_filenames)
    print(f"Found {len(eligible)} papers to process.")

    # Initialize Rate Limiter and Error Tracker
    rate_limiter = RateLimiter(max_calls=rpm, period=60.0)
    error_tracker = ErrorTracker(max_errors=max_errors)

    # Lock for CSV writing
    csv_lock = threading.Lock()

    # Failures tracking
    failure_fieldnames = ["filename", "error", "timestamp"]
    failures_file_exists = os.path.isfile(failures_csv)

    remaining = eligible

    # Filter out papers where PDF doesn't exist
    valid_papers = []
    for paper in remaining:
        pdf_path = os.path.join(pdf_dir, paper['_filename'])
        if os.path.exists(pdf_path):
            valid_papers.append(paper)
        else:
            tqdm.write(f"Warning: {pdf_path} not found. Skipping.")

    if not valid_papers:
        print("No papers to process.")
        return

    print(f"Processing {len(valid_papers)} papers with {max_workers} workers at {rpm} RPM...")

    # Open failures CSV in append mode
    with open(failures_csv, mode='a', newline='', encoding='utf-8') as fail_f:
        fail_writer = csv.DictWriter(fail_f, fieldnames=failure_fieldnames)
        if not failures_file_exists:
            fail_writer.writeheader()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_paper = {
                executor.submit(
                    process_single_file,
                    os.path.join(pdf_dir, paper['_filename']),
                    api_key,
                    json_dir,
                    model_name,
                    rate_limiter,
                    error_tracker,
                    paper
                ): paper
                for paper in valid_papers
            }

            for future in tqdm(as_completed(future_to_paper), total=len(valid_papers), desc="Extracting bias targets"):
                paper = future_to_paper[future]
                filename = paper['_filename']

                if error_tracker.check_exit():
                    tqdm.write("Exiting due to too many resource exhausted errors.")
                    executor.shutdown(wait=False, cancel_futures=True)
                    print(f"\nExited after {error_tracker.error_count} resource exhausted errors.")
                    sys.exit(1)

                try:
                    result, error = future.result()
                    if error:
                        with csv_lock:
                            fail_writer.writerow({
                                "filename": filename,
                                "error": error,
                                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                            })
                            fail_f.flush()
                except Exception as exc:
                    tqdm.write(f"{filename} generated an exception: {exc}")
                    with csv_lock:
                        fail_writer.writerow({
                            "filename": filename,
                            "error": str(exc),
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                        fail_f.flush()

    # Final summary
    if error_tracker.error_count > 0:
        print(f"\nCompleted with {error_tracker.error_count} resource exhausted error(s).")


if __name__ == "__main__":
    main()
