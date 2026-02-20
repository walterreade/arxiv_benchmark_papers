
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
from typing import Optional, List, Dict
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Remove GEMINI_API_KEY if both are set to avoid the warning message
if os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
    del os.environ["GEMINI_API_KEY"]

from google import genai
from google.genai import types


class ResourceExhaustedError(Exception):
    """Raised when API returns resource exhausted error."""
    pass


class IterationTimeoutError(Exception):
    """Raised when a single iteration takes too long."""
    pass

ITERATION_TIMEOUT = 120  # 2 minutes


class ErrorTracker:
    """Thread-safe error counter."""
    def __init__(self, max_errors: int = 5):
        self.max_errors = max_errors
        self.error_count = 0
        self.lock = threading.Lock()
        self.should_exit = threading.Event()
    
    def record_resource_exhausted(self):
        with self.lock:
            self.error_count += 1
            if self.error_count > self.max_errors:
                self.should_exit.set()
                return True
        return False
    
    def check_exit(self) -> bool:
        return self.should_exit.is_set()


class RateLimiter:
    """Thread-safe rate limiter using Condition for efficient waiting."""
    def __init__(self, max_calls: int, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def wait_for_token(self):
        """Blocks until a token is available."""
        with self.condition:
            while True:
                now = time.time()
                # Remove calls older than period
                self.calls = [t for t in self.calls if now - t < self.period]
                
                if len(self.calls) < self.max_calls:
                    self.calls.append(now)
                    return
                
                # Calculate wait time until oldest call expires
                if self.calls:
                    wait_time = self.calls[0] + self.period - now + 0.1
                else:
                    wait_time = 1
                
                # Wait with timeout, releases lock while waiting
                self.condition.wait(timeout=max(0.1, wait_time))
    
    def release_slot(self):
        """Notify waiting threads that a slot may be available."""
        with self.condition:
            self.condition.notify_all()

def load_failed_files(failures_csv: str) -> set:
    """Load filenames that previously failed with non-retryable errors."""
    if not os.path.exists(failures_csv):
        return set()
    
    failed = set()
    with open(failures_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row.get('filename', '')
            error = row.get('error', '').lower()
            # Skip resource exhausted errors - these should be retried
            if 'resource exhausted' in error or '429' in error or 'quota' in error:
                continue
            if filename:
                failed.add(filename)
    return failed


def save_json(data: dict, output_dir: str, filename: str):
    """Save the analysis data to a JSON file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    json_path = os.path.join(output_dir, filename.replace('.pdf', '.json'))
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        tqdm.write(f"Warning: Failed to save JSON for {filename}: {e}")

def analyze_paper_deep_dive(pdf_path: str, api_key: str, model_name: str, 
                            rate_limiter: RateLimiter, error_tracker: ErrorTracker,
                            max_retries: int = 3) -> dict:
    """Analyze the PDF content for deep dive religion details using Gemini API."""
    client = genai.Client(api_key=api_key)
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
        
        prompt = """
    Analyze this academic paper and provide a deep dive on its relation to religion/faith.
    Extract the following information in JSON format:
    
    1. `benchmark_measurement`: string. What specifically did the benchmark measure in terms of faith/religion? (e.g., bias against Muslims, knowledge of Christian theology, stereotype detection in religious contexts).
    2. `religious_groups`: list of strings. Which specific religious groups were measured or mentioned? (e.g., Christianity, Islam, Judaism, Buddhism, Hinduism, Atheism, etc.).
    3. `models_tested`: list of strings. Which specific Large Language Models were evaluated in this paper? (e.g., GPT-4, Llama 2, Claude 3, etc.).
    4. `languages_evaluated`: list of strings. Which languages were evaluated in this paper? (e.g., English, Spanish, Arabic, Chinese, etc.). If not explicitly stated, use ["English"] as default.
    5. `response_type`: list of strings. The type of LLM output evaluated. Use "short" for multiple choice or short answers, "long" for open-ended text generation, or "other" for other types. Multiple values allowed if the paper evaluates different response types.
    6. `religion_component`: string. The extent to which religion is a focus of the paper. Use "major" if religion is the paper's main focus, "minor" if religion is a component but not the main focus, or "none" if the paper doesn't analyze aspects of religion.
    7. `base_benchmarks`: list of strings. Any existing benchmarks this paper is based on, extends, or compares against (e.g., BBQ, StereoSet, CrowS-Pairs, BOLD, WinoBias, etc.). Use an empty list if none.
    8. `continuous_testing`: boolean. True if the paper indicates the evaluation/benchmark will be ongoing or continuously updated, otherwise False.
    9. `findings`: string. What were the key findings related to religion? (e.g., "The model showed high bias against Muslim names", "GPT-4 performed best on theological questions").
    10. `references`: list of strings. All references cited in the paper. Each reference should be a complete citation string as it appears in the references section. Do not include reference numbers (e.g., [1], [2], 1., 2.) that precede the citation.
    
    Make sure the output is valid JSON.
    """
        
        # Retry logic with exponential backoff
        last_exception = None
        for attempt in range(max_retries):
            try:
                if error_tracker.check_exit():
                    raise ResourceExhaustedError("Too many resource exhausted errors, stopping.")
                
                response = client.models.generate_content(
                    model=model_name,
                    contents=[sample_file, prompt],
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                result_text = response.text
                return json.loads(result_text)
                
            except json.JSONDecodeError:
                return {"raw_response": result_text}
            except Exception as e:
                last_exception = e
                error_str = str(e).lower()
                
                # Check for resource exhausted / rate limit errors
                if "resource exhausted" in error_str or "429" in error_str or "quota" in error_str:
                    tqdm.write(f"  Resource exhausted on {Path(pdf_path).name}, attempt {attempt + 1}/{max_retries}")
                    if error_tracker.record_resource_exhausted():
                        raise ResourceExhaustedError("Too many resource exhausted errors, stopping.")
                    
                    # Exponential backoff with jitter
                    backoff = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(backoff)
                elif "500" in error_str or "503" in error_str or "server" in error_str:
                    # Transient server errors - retry
                    tqdm.write(f"  Server error on {Path(pdf_path).name}, attempt {attempt + 1}/{max_retries}")
                    backoff = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(backoff)
                else:
                    # Non-retryable error
                    raise e
        
        # All retries exhausted
        raise last_exception

    finally:
        try:
            if sample_file is not None:
                client.files.delete(name=sample_file.name)
        except Exception as e:
            tqdm.write(f"Warning: Failed to delete file {sample_file.name}: {e}")
        # Notify other threads a slot may be available
        rate_limiter.release_slot()


def process_single_file(pdf_path: str, api_key: str, json_dir: str, model_name: str,
                        rate_limiter: RateLimiter, error_tracker: ErrorTracker,
                        title: str) -> tuple[Optional[dict], Optional[str]]:
    """Process a single file. Returns (result_dict, None) if successful, (None, error_msg) if failed."""
    filename = Path(pdf_path).name
    try:
        # Check if we should exit
        if error_tracker.check_exit():
            return None, "Exiting due to too many resource exhausted errors"
        
        analysis = analyze_paper_deep_dive(pdf_path, api_key, model_name, rate_limiter, error_tracker)
        
        # Save to JSON
        url_slug = filename.replace('.pdf', '')
        json_data = {
            "filename": filename,
            "title": title,
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

def main():
    parser = argparse.ArgumentParser(description="Deep dive analysis of religion papers.")
    parser.add_argument("--csv", default="csv/1st_pass_results.csv", help="Input CSV file")
    parser.add_argument("--pdf_dir", default="pdf", help="Directory containing PDFs")
    parser.add_argument("--json_dir", default="json/2nd_pass_json", help="Directory to save JSON analysis")
    parser.add_argument("--failures", default="csv/2nd_pass_failures.csv", help="CSV file to track failed files")
    parser.add_argument("--reprocess", action="store_true", help="Re-analyze all files, ignoring existing results")
    parser.add_argument("--rpm", type=int, default=50, help="Requests per minute (API rate limit).")
    parser.add_argument("--workers", type=int, default=10, help="Number of worker threads.")
    parser.add_argument("--model", default="gemini-2.5-pro", help="Gemini model name.")
    parser.add_argument("--max-errors", type=int, default=1, help="Max resource exhausted errors before exit.")
    
    args = parser.parse_args()
    
    input_csv = args.csv
    pdf_dir = args.pdf_dir
    json_dir = args.json_dir
    failures_csv = args.failures
    reprocess = args.reprocess
    rpm = args.rpm
    # Cap workers to rpm to reduce thread contention
    max_workers = min(args.workers, rpm)
    model_name = args.model
    max_errors = args.max_errors
    
    # Create json output directory
    if not os.path.exists(json_dir):
        os.makedirs(json_dir, exist_ok=True)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return

    # Initialize Rate Limiter and Error Tracker
    rate_limiter = RateLimiter(max_calls=rpm, period=60.0)
    error_tracker = ErrorTracker(max_errors=max_errors)
    
    # Lock for CSV writing
    csv_lock = threading.Lock()
    
    # Failures tracking
    failure_fieldnames = ["filename", "error", "timestamp"]
    failures_file_exists = os.path.isfile(failures_csv)

    # Read papers to process
    papers_to_process = []
    ai_keywords = ['ai', 'artificial intelligence', 'llm', 'large language model', 'machine learning', 
                   'neural network', 'deep learning', 'gpt', 'transformer', 'nlp', 'natural language']
    if os.path.exists(input_csv):
        with open(input_csv, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Must be faith/ethics related
                if row.get('is_faith_ethics_related') != 'True':
                    continue
                # Must be LLM related OR reasoning indicates AI evaluation
                is_llm = row.get('is_llm_related') == 'True'
                reasoning = row.get('reasoning', '').lower()
                is_ai_reasoning = any(kw in reasoning for kw in ai_keywords)
                if is_llm or is_ai_reasoning:
                    papers_to_process.append(row)
    else:
        print(f"Error: {input_csv} not found.")
        return

    print(f"Found {len(papers_to_process)} papers to analyze.")
    
    # Load previously failed files (excluding resource exhausted errors)
    failed_files = load_failed_files(failures_csv)
    print(f"Previously failed (will skip): {len(failed_files)}")
    
    # Check for already processed by looking for existing JSON files
    if reprocess:
        print("Reprocess flag set - will re-analyze all files.")
        remaining = papers_to_process
    else:
        processed_filenames = set()
        if os.path.exists(json_dir):
            existing_jsons = glob.glob(os.path.join(json_dir, "*.json"))
            for jp in existing_jsons:
                processed_filenames.add(Path(jp).stem + ".pdf")
        
        skip_files = processed_filenames | failed_files
        print(f"Already processed: {len(processed_filenames)}")
        remaining = [p for p in papers_to_process if p['filename'] not in skip_files]
    
    # Filter out papers where PDF doesn't exist
    valid_papers = []
    for paper in remaining:
        pdf_path = os.path.join(pdf_dir, paper['filename'])
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
        
        # Use ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_paper = {
                executor.submit(
                    process_single_file,
                    os.path.join(pdf_dir, paper['filename']),
                    api_key,
                    json_dir,
                    model_name,
                    rate_limiter,
                    error_tracker,
                    paper.get('title', 'Unknown Title')
                ): paper
                for paper in valid_papers
            }
            
            for future in tqdm(as_completed(future_to_paper), total=len(valid_papers), desc="Analyzing papers"):
                paper = future_to_paper[future]
                filename = paper['filename']
                
                # Check if we should exit early
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
