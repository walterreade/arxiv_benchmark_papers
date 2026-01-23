
import os
import argparse
import csv
import json
import time
import glob
from pathlib import Path
from typing import Optional, Set
from tqdm import tqdm

from google import genai
from google.genai import types
from pypdf import PdfReader
from dotenv import load_dotenv

# Load environment variables: GOOGLE_API_KEY=<your_api_key>
load_dotenv()

MODEL = 'gemini-3-flash-preview'

def get_page_count(pdf_path: str) -> int:
    """Get the total number of pages in the PDF."""
    try:
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except Exception as e:
        print(f"Error reading PDF for page count: {e}")
        return -1

def analyze_content(pdf_path: str, api_key: str) -> dict:
    """Analyze the PDF content using Gemini API."""
    client = genai.Client(api_key=api_key)
    
    # Upload the file
    print(f"Uploading {Path(pdf_path).name} to Gemini...")
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
    6. `is_faith_ethics_related`: boolean. True if and only if the paper deals has a component of evaluating or benchmarking religion (and/or faith, spiritual traditions, theology, epistemology, hermeneutics, etc.), morals, and/or ethics.
    7. `reference_count`: integer. The approximate number of references cited in the paper. Count them if possible, or look for the numbering in the references section.
    8. `appendix_length`: integer. The number of pages in the appendix.
    9. `is_survey_review`: boolean. True if the paper is a survey, review, or overview paper.
    10. `reasoning`: string. A brief explanation for the `is_faith_ethics_related` classification.
    
    Make sure the output is valid JSON.
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[sample_file, prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        result_text = response.text
    finally:
        try:
            client.files.delete(name=sample_file.name)
        except Exception as e:
            print(f"Warning: Failed to delete file {sample_file.name}: {e}")
    
    return json.loads(result_text)

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

def process_file(pdf_path: str, api_key: str, writer: csv.DictWriter, csv_file, json_dir: Optional[str] = None):
    """Process a single file and write to CSV."""
    filename = Path(pdf_path).name
    
    # 1. Get Page Count locally
    page_count = get_page_count(pdf_path)

    # 2. Get Content Analysis from Gemini
    try:
        analysis = analyze_content(pdf_path, api_key)
        
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
        
        writer.writerow(row)
        csv_file.flush() # Ensure it's written

    except Exception as e:
        tqdm.write(f"  Error processing {filename}: {e}")

def save_json(data: dict, output_dir: str, filename: str):
    """Save the analysis JSON to a file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    json_path = os.path.join(output_dir, filename.replace('.pdf', '.json'))
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        tqdm.write(f"Warning: Failed to save JSON for {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Analyze PDF paper(s).")
    parser.add_argument("input_path", nargs='?', default="pdf", help="Path to the PDF file or directory")
    parser.add_argument("--output", default="1st_pass_results.csv", help="Output CSV file")
    parser.add_argument("--json_dir", default="1st_pass_json", help="Directory to save JSON analysis")
    
    args = parser.parse_args()
    
    input_path = args.input_path
    output_csv = args.output
    json_dir = args.json_dir
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return

    processed_files = load_processed_files(output_csv)
    print(f"Found {len(processed_files)} already processed files.")
    
    fieldnames = ["filename", "date", "title", "page_count", "is_benchmark", "is_llm_related", "is_bias_related", "is_faith_ethics_related", "is_survey_review", "reference_count", "appendix_length", "reasoning"]
    
    file_exists = os.path.isfile(output_csv)
    
    # Create JSON directory if it doesn't exist
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    
    with open(output_csv, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
            
        if os.path.isdir(input_path):
            # Process directory
            all_pdfs = sorted(glob.glob(os.path.join(input_path, "*.pdf")), reverse=True)
            
            # Filter first
            pdfs_to_process = [p for p in all_pdfs if Path(p).name not in processed_files]
            
            print(f"Found {len(all_pdfs)} PDFs. {len(processed_files)} processed. {len(pdfs_to_process)} remaining.")
            
            for pdf_file in tqdm(pdfs_to_process, desc="Analyzing papers"):
                # Pass json_dir explicitly or handle saving inside process_file if we refactor it.
                # Since process_file doesn't take json_dir, let's modify it or just logic here?
                # Actually, I need to modify process_file to return the data or pass json_dir to it.
                # Let's modify process_file to take json_dir.
                process_file(pdf_file, api_key, writer, f, json_dir)
                # Rate limit safety
                time.sleep(1) 
                
        elif os.path.isfile(input_path):
            # Process single file
            if Path(input_path).name not in processed_files:
                process_file(input_path, api_key, writer, f, json_dir)
                print(f"Processed {input_path}")
            else:
                print(f"{input_path} already processed.")
        else:
            print(f"Error: {input_path} is not a valid file or directory.")

if __name__ == "__main__":
    main()
