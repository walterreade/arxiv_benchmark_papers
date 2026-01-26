#!/usr/bin/env python3
"""
Generate a timestamped update markdown file for newly analyzed papers.
"""

import argparse
import json
import os
import csv
from datetime import datetime


def load_csv_metadata(csv_file: str) -> dict:
    """Load CSV file and return dict mapping filename to metadata."""
    metadata = {}
    if not os.path.exists(csv_file):
        return metadata
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row.get('filename', '')
            metadata[filename] = row
    return metadata


def get_arxiv_url(filename: str) -> str:
    """Convert filename to arxiv PDF URL."""
    arxiv_id = filename.replace('.pdf', '').replace('.json', '')
    return f"https://arxiv.org/pdf/{arxiv_id}"


def check_mormon_mention(paper: dict) -> bool:
    """Check if paper mentions Mormon or Latter-day Saints."""
    text_to_check = json.dumps(paper).lower()
    return 'mormon' in text_to_check or 'latter-day saints' in text_to_check


def generate_update_file(json_files: list[str], csv_file: str, output_path: str):
    """Generate update markdown file for the specified JSON files."""
    csv_metadata = load_csv_metadata(csv_file)
    
    # Load paper data from JSON files
    papers = []
    for json_path in json_files:
        if not os.path.exists(json_path):
            continue
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                paper = json.load(f)
                paper['_filename'] = os.path.basename(json_path).replace('.json', '.pdf')
                papers.append(paper)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading {json_path}: {e}")
    
    if not papers:
        print("No papers to include in update.")
        return False
    
    # Sort by filename descending
    papers.sort(key=lambda p: p.get('_filename', ''), reverse=True)
    
    lines = [f"# Analysis Update - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]
    lines.append(f"**New papers analyzed:** {len(papers)}\n")
    
    for paper in papers:
        filename = paper.get('_filename', '')
        meta = csv_metadata.get(filename, {})
        
        title = meta.get('title', 'Unknown Title')
        date = meta.get('date', 'Unknown Date')
        arxiv_url = get_arxiv_url(filename)
        
        benchmark_measurement = paper.get('benchmark_measurement', '')
        findings = paper.get('findings', '')
        combined = f"{benchmark_measurement} {findings}".strip()
        
        mormon_tag = " #Mormon" if check_mormon_mention(paper) else ""
        
        lines.append(f"## {title}{mormon_tag}\n")
        lines.append(f"[{arxiv_url}]({arxiv_url})\n")
        lines.append(f"**Date:** {date}\n")
        lines.append(f"{combined}\n")
        lines.append("")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"Update saved to {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate update markdown for new papers.")
    parser.add_argument("--json-files", nargs='+', required=True, help="List of JSON files to include")
    parser.add_argument("--csv", default="csv/1st_pass_results.csv", help="CSV file with paper metadata")
    parser.add_argument("--output", help="Output markdown file (default: auto-generated timestamp)")
    
    args = parser.parse_args()
    
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"analysis/updates/update_{timestamp}.md"
    
    generate_update_file(args.json_files, args.csv, output_path)


if __name__ == "__main__":
    main()
