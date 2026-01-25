
import os
import argparse
import csv
import time
from pathlib import Path
from typing import Optional, List, Dict
from tqdm import tqdm

import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# TODO: add model, rate, etc., options similar to 1st pass
# TODO: save to json instead of md

MODEL = 'gemini-3-pro-preview'

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
    Extract the following information:
    
    1. **Benchmark Measurement**: What specifically did the benchmark measure in terms of faith/religion? (e.g., bias against Muslims, knowledge of Christian theology, stereotype detection in religious contexts).
    2. **Religious Groups**: Which specific religious groups were measured or mentioned? (e.g., Christianity, Islam, Judaism, Buddhism, Hinduism, Atheism, etc.).
    3. **Models Tested**: Which specific Large Language Models were evaluated in this paper? (e.g., GPT-4, Llama 2, Claude 3, etc.).
    4. **Findings**: What were the key findings related to religion? (e.g., "The model showed high bias against Muslim names", "GPT-4 performed best on theological questions").
    
    Format the output as a Markdown block. Do not include the title or filename in the output, just the content.
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[sample_file, prompt],
        )
        result_text = response.text
    finally:
        try:
            client.files.delete(name=sample_file.name)
        except Exception as e:
            tqdm.write(f"Warning: Failed to delete file {sample_file.name}: {e}")
    
    return result_text

def main():
    parser = argparse.ArgumentParser(description="Deep dive analysis of religion papers.")
    parser.add_argument("--csv", default="religion_20260118.csv", help="Input CSV file")
    parser.add_argument("--output", default="religion_analysis_report.md", help="Output Markdown file")
    parser.add_argument("--pdf_dir", default="pdf", help="Directory containing PDFs")
    
    args = parser.parse_args()
    
    input_csv = args.csv
    output_md = args.output
    pdf_dir = args.pdf_dir
    
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
    
    # Initialize Report
    if not os.path.exists(output_md):
        with open(output_md, "w", encoding="utf-8") as f:
            f.write("# Religion Benchmarks Deep Dive\n\n")

    # Check for already processed (simple check based on filename in md content might be hard, 
    # but we can rely on appending or just overwrite if needed. 
    # For now, let's just append new entries. Robust resume would read the MD file.)
    
    # Better resume logic: read the MD file and check for "### [Title](URL)"
    processed_filenames = set()
    if os.path.exists(output_md):
        with open(output_md, "r", encoding="utf-8") as f:
            content = f.read()
            # Match: ### [Title](https://arxiv.org/pdf/1234.5678)
            # The URL excludes .pdf extension, so we need to add it back to match CSV filename if needed,
            # but actually the CSV filenames HAVE .pdf. 
            # So if URL is .../1234.5678, filename is 1234.5678.pdf
            matches = re.findall(r"### \[.*?\]\(https://arxiv\.org/pdf/(.*?)\)", content)
            for m in matches:
                # m is the arXiv ID, e.g. "2409.13843"
                processed_filenames.add(f"{m}.pdf")
    
    print(f"Already processed: {len(processed_filenames)}")
    
    processed_list = [p for p in papers_to_process if p['filename'] not in processed_filenames]
    
    for paper in tqdm(processed_list, desc="Analyzing papers"):
        filename = paper['filename']
        title = paper.get('title', 'Unknown Title')
        pdf_path = os.path.join(pdf_dir, filename)
        
        if not os.path.exists(pdf_path):
            tqdm.write(f"Warning: {pdf_path} not found. Skipping.")
            continue
            
        try:
            analysis_text = analyze_paper_deep_dive(pdf_path, api_key)
            
            with open(output_md, "a", encoding="utf-8") as f:
                url_slug = filename.replace('.pdf', '')
                f.write(f"\n### [{title}](https://arxiv.org/pdf/{url_slug})\n\n")
                f.write(analysis_text)
                f.write("\n\n---\n")
                
            # Rate limit safety
            time.sleep(2)
            
        except Exception as e:
            tqdm.write(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
