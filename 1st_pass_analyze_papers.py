import os
import argparse
import csv
import json
import time
import glob
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


class RateLimiter:
    """Thread-safe rate limiter."""
    def __init__(self, max_calls: int, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = threading.Lock()

    def wait_for_token(self):
        """Blocks until a token is available."""
        while True:
            with self.lock:
                now = time.time()
                # Remove calls older than period
                self.calls = [t for t in self.calls if now - t < self.period]
                
                if len(self.calls) < self.max_calls:
                    self.calls.append(now)
                    return
                
                # Calculate sleep time while holding lock
                if self.calls:
                    sleep_time = self.calls[0] + self.period - now
                else:
                    sleep_time = 1
            
            # Sleep outside the lock to allow other threads to proceed
            if sleep_time > 0:
                time.sleep(sleep_time)

def get_page_count(pdf_path: str) -> int:
    """Get the total number of pages in the PDF."""
    try:
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except Exception as e:
        # Don't print to stdout in threads to avoid race conditions with tqdm
        return -1

def analyze_content(pdf_path: str, api_key: str, rate_limiter: RateLimiter, model_name: str) -> dict:
    """Analyze the PDF content using Gemini API."""
    client = genai.Client(api_key=api_key)
    
    # Upload the file
    # We might want to rate limit uploads too, but usually generation is the bottleneck.
    # We'll put rate limit before generation to be safe, or before upload?
    # Let's simple-check rate limiter before the whole sensitive block.
    
    # Acquiring token for the API operation sequence
    rate_limiter.wait_for_token()
    
    try:
        # print to tqdm
        tqdm.write(f"Uploading {Path(pdf_path).name}...") 
        # Reducing verbosity for threading
        
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
        
        response = client.models.generate_content(
            model=model_name,
            contents=[sample_file, prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        result_text = response.text
        
        return json.loads(result_text)

    except Exception as e:
        # If we hit a 429, we should arguably retry, but for simplicity in this pass, we raise.
        # The executor will catch it.
        raise e
    finally:
        try:
            if 'sample_file' in locals():
                client.files.delete(name=sample_file.name)
        except Exception:
            pass

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

def process_single_file(pdf_path: str, api_key: str, json_dir: Optional[str], rate_limiter: RateLimiter, model_name: str) -> Optional[dict]:
    """
    Process a single file. Returns a dict of results if successful, None if failed.
    """
    filename = Path(pdf_path).name
    try:
        # 1. Get Page Count locally (fast, no API)
        page_count = get_page_count(pdf_path)

        # 2. Get Content Analysis from Gemini (slow, API)
        analysis = analyze_content(pdf_path, api_key, rate_limiter, model_name)
        
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
        return row

    except Exception as e:
        tqdm.write(f"  Error processing {filename}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Analyze PDF paper(s) with multi-threading.")
    parser.add_argument("input_path", nargs='?', default="pdf", help="Path to the PDF file or directory")
    parser.add_argument("--output", default="1st_pass_results.csv", help="Output CSV file")
    parser.add_argument("--json_dir", default="1st_pass_json", help="Directory to save JSON analysis")
    parser.add_argument("--rpm", type=int, default=15, help="Requests per minute (API rate limit). Default 15.")
    parser.add_argument("--workers", type=int, default=8, help="Number of worker threads. Default 8.")
    parser.add_argument("--model", default="gemini-3-flash-preview", help="Gemini model name.")
    
    args = parser.parse_args()
    
    input_path = args.input_path
    output_csv = args.output
    json_dir = args.json_dir
    rpm = args.rpm
    max_workers = args.workers
    model_name = args.model
    
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

    # Initialize Rate Limiter
    rate_limiter = RateLimiter(max_calls=rpm, period=60.0)
    
    # Lock for CSV writing
    csv_lock = threading.Lock()
    
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

    # Open CSV in append mode
    with open(output_csv, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        
        # Use ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(process_single_file, pdf, api_key, json_dir, rate_limiter, model_name): pdf 
                for pdf in pdfs_to_process
            }
            
            for future in tqdm(as_completed(future_to_file), total=len(pdfs_to_process), desc="Analyzing papers"):
                filename = Path(future_to_file[future]).name
                try:
                    result = future.result()
                    if result:
                        with csv_lock:
                            writer.writerow(result)
                            f.flush()
                except Exception as exc:
                    tqdm.write(f"{filename} generated an exception: {exc}")

if __name__ == "__main__":
    main()
