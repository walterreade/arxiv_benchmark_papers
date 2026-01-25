
import os
import argparse
import csv
import json
import time
from pathlib import Path
from typing import Optional, List, Dict
from tqdm import tqdm

import glob
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# TODO: add model, rate, etc., options similar to 1st pass

MODEL = 'gemini-3-pro-preview'

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

def analyze_paper_deep_dive(pdf_path: str, api_key: str) -> dict:
    """Analyze the PDF content for deep dive religion details using Gemini API."""
    client = genai.Client(api_key=api_key)
    
    # Upload the file
    # tqdm.write(f"Uploading {Path(pdf_path).name} to Gemini...")
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
    Analyze this academic paper and provide a deep dive on its relation to religion/faith.
    Extract the following information in JSON format:
    
    1. `benchmark_measurement`: string. What specifically did the benchmark measure in terms of faith/religion? (e.g., bias against Muslims, knowledge of Christian theology, stereotype detection in religious contexts).
    2. `religious_groups`: list of strings. Which specific religious groups were measured or mentioned? (e.g., Christianity, Islam, Judaism, Buddhism, Hinduism, Atheism, etc.).
    3. `models_tested`: list of strings. Which specific Large Language Models were evaluated in this paper? (e.g., GPT-4, Llama 2, Claude 3, etc.).
    4. `findings`: string. What were the key findings related to religion? (e.g., "The model showed high bias against Muslim names", "GPT-4 performed best on theological questions").
    
    Make sure the output is valid JSON.
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[sample_file, prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        result_text = response.text
        return json.loads(result_text)
    except json.JSONDecodeError:
        return {"raw_response": result_text}
    finally:
        try:
            client.files.delete(name=sample_file.name)
        except Exception as e:
            tqdm.write(f"Warning: Failed to delete file {sample_file.name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Deep dive analysis of religion papers.")
    parser.add_argument("--csv", default="1st_pass_results.csv", help="Input CSV file")
    parser.add_argument("--pdf_dir", default="pdf", help="Directory containing PDFs")
    parser.add_argument("--json_dir", default="2nd_pass_json", help="Directory to save JSON analysis")
    parser.add_argument("--reprocess", action="store_true", help="Re-analyze all files, ignoring existing results")
    
    args = parser.parse_args()
    
    input_csv = args.csv
    pdf_dir = args.pdf_dir
    json_dir = args.json_dir
    reprocess = args.reprocess
    
    # Create json output directory
    if not os.path.exists(json_dir):
        os.makedirs(json_dir, exist_ok=True)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return

    # Read papers to process
    papers_to_process = []
    if os.path.exists(input_csv):
        with open(input_csv, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('is_faith_ethics_related') == 'TRUE':
                    papers_to_process.append(row)
    else:
        print(f"Error: {input_csv} not found.")
        return

    print(f"Found {len(papers_to_process)} papers to analyze.")
    
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
        
        print(f"Already processed: {len(processed_filenames)}")
        remaining = [p for p in papers_to_process if p['filename'] not in processed_filenames]
    
    for paper in tqdm(remaining, desc="Analyzing papers"):
        filename = paper['filename']
        title = paper.get('title', 'Unknown Title')
        pdf_path = os.path.join(pdf_dir, filename)
        
        if not os.path.exists(pdf_path):
            tqdm.write(f"Warning: {pdf_path} not found. Skipping.")
            continue
            
        try:
            analysis = analyze_paper_deep_dive(pdf_path, api_key)
            
            # Save to JSON
            url_slug = filename.replace('.pdf', '')
            json_data = {
                "filename": filename,
                "title": title,
                "arxiv_url": f"https://arxiv.org/pdf/{url_slug}",
                **analysis
            }
            save_json(json_data, json_dir, filename)
                
            # Rate limit safety
            time.sleep(2)
            
        except Exception as e:
            tqdm.write(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
