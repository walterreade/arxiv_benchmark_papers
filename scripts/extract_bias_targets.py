#!/usr/bin/env python3
"""
Extract bias targets from papers that are both LLM-related and bias-related.

This script:
1. Reads JSON files from 1st_pass_json folder
2. Filters for files where both is_llm_related and is_bias_related are true
3. Reanalyzes the equivalent PDF to extract bias targets
4. Adds the bias_targets list to the JSON file
"""

import argparse
import json
import re
import random
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

from shared import (
    genai, types,
    ResourceExhaustedError, IterationTimeoutError, ITERATION_TIMEOUT,
    ErrorTracker, RateLimiter,
)

# Directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
JSON_DIR = PROJECT_DIR / "json" / "1st_pass_json"
PDF_DIR = PROJECT_DIR / "pdf"

# Model configuration
MODEL_NAME = "gemini-3-flash-preview"


EXTRACTION_PROMPT = """Analyze this academic paper and identify what types of bias are being measured or evaluated.

Extract a list of bias target categories that the paper measures. Common examples include (but are not limited to):
- Religious bias (bias against specific religions or religious groups)
- Gender bias (bias against specific genders)
- Racial bias (bias against racial or ethnic groups)
- Age bias (bias against age groups)
- Political bias (bias against political affiliations)
- Socioeconomic bias (bias against income/class groups)
- Disability bias (bias against people with disabilities)
- Sexual orientation bias (bias against LGBTQ+ individuals)
- Nationality bias (bias against specific nationalities)
- Hate speech detection (general toxic or hateful content)
- Stereotyping (reinforcement of stereotypes)
- Fairness in outcomes (disparate treatment or impact)

Return ONLY a JSON object with the following format:
{
  "bias_targets": ["category1", "category2", ...]
}

The bias_targets list should contain short, descriptive category names for each type of bias measured in the paper.
If the paper doesn't clearly measure any specific bias categories, return an empty list.
Be specific about what groups or categories the bias is measured against.
"""


def get_filtered_papers():
    """Get papers where both is_llm_related and is_bias_related are true."""
    filtered = []
    
    for json_file in JSON_DIR.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            if data.get("is_llm_related") is True and data.get("is_bias_related") is True:
                # Check if bias_targets already exists
                if "bias_targets" not in data:
                    filtered.append(json_file)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {json_file}: {e}")
            continue
    
    return filtered


def extract_bias_targets(pdf_path: Path, rate_limiter: RateLimiter,
                         error_tracker: ErrorTracker, max_retries: int = 3) -> list:
    """Extract bias targets from a PDF using Gemini with retry logic."""
    client = genai.Client()
    sample_file = None
    
    # Check if we should exit before starting
    if error_tracker.check_exit():
        raise ResourceExhaustedError("Too many resource exhausted errors, stopping.")
    
    # Wait for rate limit token
    rate_limiter.wait_for_token()
    
    try:
        # Upload the PDF file
        sample_file = client.files.upload(file=pdf_path)
        
        # Wait for processing with timeout
        start_time = time.time()
        while sample_file.state.name == "PROCESSING":
            if time.time() - start_time > ITERATION_TIMEOUT:
                raise IterationTimeoutError(f"File processing timed out after {ITERATION_TIMEOUT}s")
            time.sleep(2)
            sample_file = client.files.get(name=sample_file.name)
        
        if sample_file.state.name == "FAILED":
            raise ValueError(f"File processing failed: {sample_file.state.name}")
        
        # Retry logic with exponential backoff
        last_exception = None
        for attempt in range(max_retries):
            try:
                if error_tracker.check_exit():
                    raise ResourceExhaustedError("Too many resource exhausted errors, stopping.")
                
                # Generate content
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=[
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_uri(
                                    file_uri=sample_file.uri,
                                    mime_type=sample_file.mime_type,
                                ),
                                types.Part.from_text(text=EXTRACTION_PROMPT),
                            ],
                        ),
                    ],
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        max_output_tokens=1024,
                    ),
                )
                
                # Parse response
                response_text = response.text.strip()
                
                # Clean up response if wrapped in markdown
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.startswith("```"):
                    response_text = response_text[3:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()
                
                try:
                    result = json.loads(response_text)
                    return result.get("bias_targets", [])
                except json.JSONDecodeError:
                    # Fallback: try to extract bias_targets array using regex
                    match = re.search(r'"bias_targets"\s*:\s*\[(.*?)\]', response_text, re.DOTALL)
                    if match:
                        items_str = match.group(1)
                        # Extract quoted strings
                        items = re.findall(r'"([^"]+)"', items_str)
                        return items
                    return []
                    
            except (ResourceExhaustedError, json.JSONDecodeError):
                raise
            except Exception as e:
                last_exception = e
                error_str = str(e).lower()
                
                if "resource exhausted" in error_str or "429" in error_str or "quota" in error_str:
                    tqdm.write(f"  Resource exhausted on {pdf_path.name}, attempt {attempt + 1}/{max_retries}")
                    if error_tracker.record_resource_exhausted():
                        raise ResourceExhaustedError("Too many resource exhausted errors, stopping.")
                    backoff = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(backoff)
                elif "500" in error_str or "503" in error_str or "server" in error_str:
                    tqdm.write(f"  Server error on {pdf_path.name}, attempt {attempt + 1}/{max_retries}")
                    backoff = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(backoff)
                else:
                    raise
        
        # All retries exhausted
        raise last_exception

    finally:
        # Clean up uploaded file from Gemini file store
        try:
            if sample_file is not None:
                client.files.delete(name=sample_file.name)
        except Exception:
            pass
        rate_limiter.release_slot()


def process_single_paper(json_path: Path, rate_limiter: RateLimiter,
                         error_tracker: ErrorTracker) -> tuple:
    """Process a single paper and return (arxiv_id, bias_targets, success, error)."""
    arxiv_id = json_path.stem
    pdf_path = PDF_DIR / f"{arxiv_id}.pdf"
    
    if not pdf_path.exists():
        return arxiv_id, [], False, "PDF not found"
    
    try:
        bias_targets = extract_bias_targets(pdf_path, rate_limiter, error_tracker)
        
        # Update JSON file
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        data["bias_targets"] = bias_targets
        
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return arxiv_id, bias_targets, True, None
        
    except Exception as e:
        return arxiv_id, [], False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Extract bias targets from papers")
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=-1,
        help="Number of papers to process. Use -1 for all papers."
    )
    parser.add_argument(
        "--rpm",
        type=int,
        default=15,
        help="Requests per minute (API rate limit). Default: 15"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of worker threads. Default: 8"
    )
    args = parser.parse_args()
    
    # Cap workers to rpm to reduce thread contention
    max_workers = min(args.workers, args.rpm)
    
    print("=" * 70)
    print("Bias Target Extraction")
    print("=" * 70)
    print(f"Model: {MODEL_NAME}")
    print(f"JSON Directory: {JSON_DIR}")
    print(f"PDF Directory: {PDF_DIR}")
    print(f"Limit: {'All' if args.limit == -1 else args.limit}")
    print(f"RPM: {args.rpm} | Workers: {max_workers}")
    print("=" * 70)
    print()
    
    # Get filtered papers
    papers = get_filtered_papers()
    print(f"Found {len(papers)} papers with is_llm_related=true AND is_bias_related=true (without bias_targets)")
    print()
    
    if not papers:
        print("No papers to process.")
        return
    
    # Apply limit
    if args.limit != -1:
        papers = papers[:args.limit]
    
    print(f"Processing {len(papers)} papers...")
    print("-" * 70)
    
    # Initialize rate limiter and error tracker
    rate_limiter = RateLimiter(max_calls=args.rpm, period=60.0)
    error_tracker = ErrorTracker(max_errors=5)
    
    success = 0
    failed = 0
    
    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_paper = {
            executor.submit(process_single_paper, json_path, rate_limiter, error_tracker): json_path
            for json_path in papers
        }
        
        for future in tqdm(as_completed(future_to_paper), total=len(papers), desc="Extracting bias targets"):
            try:
                arxiv_id, bias_targets, was_success, error = future.result()
                if was_success:
                    success += 1
                    tqdm.write(f"{arxiv_id}: {bias_targets}")
                else:
                    failed += 1
                    tqdm.write(f"{arxiv_id}: ERROR - {error}")
            except Exception as exc:
                failed += 1
                tqdm.write(f"Exception: {exc}")
    
    # Summary
    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Processed: {success + failed}")
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print("=" * 70)


if __name__ == "__main__":
    main()
