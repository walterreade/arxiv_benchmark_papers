import os
import argparse
import csv
import json
import time
import glob
import random
import sys
from pathlib import Path
from typing import Optional, Set
from tqdm import tqdm
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from google import genai
from google.genai import types
from pypdf import PdfReader
from dotenv import load_dotenv

# Load environment variables: GOOGLE_API_KEY=<your_api_key>
load_dotenv()

# Global error tracking
class ResourceExhaustedError(Exception):
    """Raised when API returns resource exhausted error."""
    pass

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

def get_page_count(pdf_path: str) -> int:
    """Get the total number of pages in the PDF."""
    try:
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except Exception as e:
        # Don't print to stdout in threads to avoid race conditions with tqdm
        return -1

def analyze_content(pdf_path: str, api_key: str, rate_limiter: RateLimiter, model_name: str, 
                    error_tracker: ErrorTracker, max_retries: int = 3) -> dict:
    """Analyze the PDF content using Gemini API with retry logic."""
    client = genai.Client(api_key=api_key)
    sample_file = None
    
    # Check if we should exit before starting
    if error_tracker.check_exit():
        raise ResourceExhaustedError("Too many resource exhausted errors, stopping.")
    
    # Acquiring token for the API operation sequence
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
        
        # Wait for processing
        while sample_file.state.name == "PROCESSING":
            time.sleep(1)
            sample_file = client.files.get(name=sample_file.name)
            
        if sample_file.state.name == "FAILED":
            raise ValueError("File upload failed.")
        
        prompt = """
        Analyze this academic paper and extract the following information in JSON format:
        
        1. `date`: string. The date of the paper in YYYY-MM-DD format. This date is found along the left margin of the paper. If that date is not found, look for a date on the first page that might reasonably be considered the submitted date.
        2. `title`: string. The title of the paper.
        3. `is_benchmark`: boolean. True if and only if the paper deals with benchmarking.
        4. `is_llm_related`: boolean. True if and only if the paper deals with Large Language Models (LLMs).
        5. `is_bias_related`: boolean. True if and only if the paper deals with bias in LLMs.
        6. `is_faith_ethics_related`: boolean. True if and only if the paper deals has a component of evaluating or benchmarking religion (and/or faith, spiritual traditions, theology, epistemology, hermeneutics, etc.), morals, and/or ethics. A brief section on, e.g., "Ethical Considerations" or "Limitations" does not count as a component of evaluating or benchmarking religion, morals, and/or ethics. 
        7. `reference_count`: integer. The approximate number of references cited in the paper. Count them if possible, or look for the numbering in the references section.
        8. `appendix_length`: integer. The number of pages in the appendix.
        9. `is_survey_review`: boolean. True if the paper is a survey, review, or overview paper.
        10. `reasoning`: string. A brief explanation for the `is_faith_ethics_related` classification.
        
        Make sure the output is valid JSON.
        """
        
        # Retry logic with exponential backoff for generate_content
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
        except Exception:
            pass
        # Notify other threads a slot may be available
        rate_limiter.release_slot()

def load_processed_files(output_csv: str) -> Set[str]:
    """Load the set of already processed filenames."""
    if not os.path.exists(output_csv):
        return set()
    
    processed = set()
    with open(output_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'filename' in row:
                processed.add(row['filename'])
    return processed

def save_json(data: dict, output_dir: str, filename: str):
    """Save the analysis JSON to a file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    json_path = os.path.join(output_dir, filename.replace('.pdf', '.json'))
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        tqdm.write(f"Warning: Failed to save JSON for {filename}: {e}")

def process_single_file(pdf_path: str, api_key: str, json_dir: Optional[str], rate_limiter: RateLimiter, 
                        model_name: str, error_tracker: ErrorTracker) -> tuple[Optional[dict], Optional[str]]:
    """
    Process a single file. Returns (result_dict, None) if successful, (None, error_msg) if failed.
    """
    filename = Path(pdf_path).name
    try:
        # Check if we should exit
        if error_tracker.check_exit():
            return None, "Exiting due to too many resource exhausted errors"
        
        # 1. Get Page Count locally (fast, no API)
        page_count = get_page_count(pdf_path)

        # 2. Get Content Analysis from Gemini (slow, API)
        analysis = analyze_content(pdf_path, api_key, rate_limiter, model_name, error_tracker)
        
        if isinstance(analysis, list):
            if len(analysis) > 0:
                analysis = analysis[0]
            else:
                analysis = {}

        # Save JSON
        if json_dir:
            save_json(analysis, json_dir, filename)

        # Prepare row
        row = {
            "filename": filename,
            "date": analysis.get("date"),
            "is_benchmark": analysis.get("is_benchmark"),
            "is_llm_related": analysis.get("is_llm_related"),
            "is_bias_related": analysis.get("is_bias_related"),
            "is_faith_ethics_related": analysis.get("is_faith_ethics_related"),
            "is_survey_review": analysis.get("is_survey_review"),
            "title": analysis.get("title"),
            "page_count": page_count,
            "reference_count": analysis.get("reference_count"),
            "appendix_length": analysis.get("appendix_length"),
            "reasoning": analysis.get("reasoning")
        }
        return row, None

    except ResourceExhaustedError as e:
        return None, str(e)
    except Exception as e:
        tqdm.write(f"  Error processing {filename}: {e}")
        return None, str(e)

def main():
    parser = argparse.ArgumentParser(description="Analyze PDF paper(s) with multi-threading.")
    parser.add_argument("input_path", nargs='?', default="pdf", help="Path to the PDF file or directory")
    parser.add_argument("--output", default="csv/1st_pass_results.csv", help="Output CSV file")
    parser.add_argument("--json_dir", default="json/1st_pass_json", help="Directory to save JSON analysis")
    parser.add_argument("--failures", default="csv/1st_pass_failures.csv", help="CSV file to track failed files")
    parser.add_argument("--rpm", type=int, default=15, help="Requests per minute (API rate limit). Default 15.")
    parser.add_argument("--workers", type=int, default=8, help="Number of worker threads. Default 8.")
    parser.add_argument("--model", default="gemini-3-flash-preview", help="Gemini model name.")
    parser.add_argument("--max-errors", type=int, default=5, help="Max resource exhausted errors before exit. Default 5.")
    
    args = parser.parse_args()
    
    input_path = args.input_path
    output_csv = args.output
    json_dir = args.json_dir
    failures_csv = args.failures
    rpm = args.rpm
    # Cap workers to rpm to reduce thread contention
    max_workers = min(args.workers, rpm)
    model_name = args.model
    max_errors = args.max_errors
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return

    processed_files = load_processed_files(output_csv)
    print(f"Found {len(processed_files)} already processed files.")
    
    fieldnames = ["filename", "date", "title", "page_count", "is_benchmark", "is_llm_related", "is_bias_related", "is_faith_ethics_related", "is_survey_review", "reference_count", "appendix_length", "reasoning"]
    
    file_exists = os.path.isfile(output_csv)
    
    if not os.path.exists(json_dir):
        os.makedirs(json_dir, exist_ok=True)

    # Initialize Rate Limiter and Error Tracker
    rate_limiter = RateLimiter(max_calls=rpm, period=60.0)
    error_tracker = ErrorTracker(max_errors=max_errors)
    
    # Lock for CSV writing
    csv_lock = threading.Lock()
    
    # Failures tracking
    failure_fieldnames = ["filename", "error", "timestamp"]
    failures_file_exists = os.path.isfile(failures_csv)
    
    # Gather files
    pdfs_to_process = []
    if os.path.isdir(input_path):
        all_pdfs = sorted(glob.glob(os.path.join(input_path, "*.pdf")), reverse=True)
        pdfs_to_process = [p for p in all_pdfs if Path(p).name not in processed_files]
        print(f"Found {len(all_pdfs)} PDFs. {len(processed_files)} processed. {len(pdfs_to_process)} remaining.")
    elif os.path.isfile(input_path):
        if Path(input_path).name not in processed_files:
            pdfs_to_process = [input_path]
        else:
            print(f"{input_path} already processed.")
            pdfs_to_process = []
    else:
        print(f"Error: {input_path} is not a valid file or directory.")
        return

    if not pdfs_to_process:
        return

    # Open CSV files in append mode
    with open(output_csv, mode='a', newline='', encoding='utf-8') as f, \
         open(failures_csv, mode='a', newline='', encoding='utf-8') as fail_f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        fail_writer = csv.DictWriter(fail_f, fieldnames=failure_fieldnames)
        if not file_exists:
            writer.writeheader()
        if not failures_file_exists:
            fail_writer.writeheader()
        
        # Use ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(process_single_file, pdf, api_key, json_dir, rate_limiter, model_name, error_tracker): pdf 
                for pdf in pdfs_to_process
            }
            
            for future in tqdm(as_completed(future_to_file), total=len(pdfs_to_process), desc="Analyzing papers"):
                pdf_path = future_to_file[future]
                filename = Path(pdf_path).name
                
                # Check if we should exit early
                if error_tracker.check_exit():
                    tqdm.write("Exiting due to too many resource exhausted errors.")
                    executor.shutdown(wait=False, cancel_futures=True)
                    print(f"\nExited after {error_tracker.error_count} resource exhausted errors.")
                    sys.exit(1)
                
                try:
                    result, error = future.result()
                    if result:
                        with csv_lock:
                            writer.writerow(result)
                            f.flush()
                    elif error:
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
