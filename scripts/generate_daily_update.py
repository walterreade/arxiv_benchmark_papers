#!/usr/bin/env python3
"""
Generate a timestamped update markdown file for newly analyzed papers.
"""

import argparse
import json
import os
from datetime import datetime

from shared import load_csv_metadata, get_arxiv_url, check_mormon_mention, filter_religion_papers


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
            
    # Filter papers to only include those with religion_component of 'major' or 'minor'
    papers = filter_religion_papers(papers)
    
    if not papers:
        print("No relevant papers (major/minor religion component) to include in update.")
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
        output_path = f"analysis/daily_updates/update_{timestamp}.md"
    
    generate_update_file(args.json_files, args.csv, output_path)


if __name__ == "__main__":
    main()
