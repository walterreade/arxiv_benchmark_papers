#!/usr/bin/env python3
"""
Generate a timestamped update markdown file for newly analyzed papers.
"""

import argparse
import json
import os
import sys
from datetime import datetime

from shared import load_csv_metadata, get_arxiv_url, check_mormon_mention, filter_religion_papers


def generate_update_file(json_files: list[str], csv_file: str, output_path: str,
                         stage4_dir: str = "json/4_religious_bias_analysis"):
    """Generate update markdown file for the specified JSON files.
    
    Input json_files are Stage 3 paths (json/3_paper_bias_targets/). For each,
    we look up the corresponding Stage 4 file which has religion_component,
    findings, and measurement_description fields needed for the daily update.
    """
    csv_metadata = load_csv_metadata(csv_file)
    
    # Resolve Stage 4 files from Stage 3 paths
    papers = []
    for json_path in json_files:
        basename = os.path.basename(json_path)
        stage4_path = os.path.join(stage4_dir, basename)
        
        if not os.path.exists(stage4_path):
            # Paper didn't make it to Stage 4 (not religion-related)
            continue
        try:
            with open(stage4_path, 'r', encoding='utf-8') as f:
                paper = json.load(f)
                paper['_filename'] = basename.replace('.json', '.pdf')
                papers.append(paper)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading {stage4_path}: {e}")
            
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
        
        measurement_desc = paper.get('measurement_description', '') or paper.get('benchmark_measurement', '')
        findings = paper.get('findings', '')
        combined = f"{measurement_desc} {findings}".strip()
        
        mormon_tag = " #Mormon" if check_mormon_mention(paper) else ""
        focus_tag = " #ReligionFocus" if paper.get('religion_component', '').lower() == 'major' else ""
        
        lines.append(f"## {title}{mormon_tag}{focus_tag}\n")
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
    parser.add_argument("--csv", default="utility_files/1st_pass_results.csv", help="CSV file with paper metadata")
    parser.add_argument("--output", help="Output markdown file (default: auto-generated timestamp)")
    
    args = parser.parse_args()
    
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d')
        output_path = f"reports/daily_updates/{timestamp}_daily_update.md"
    
    success = generate_update_file(args.json_files, args.csv, output_path)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
