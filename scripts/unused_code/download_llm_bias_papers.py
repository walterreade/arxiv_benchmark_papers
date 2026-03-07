#!/usr/bin/env python3
"""
Temporary script to download PDFs for all papers in llm_bias_papers.csv
that are not already in the pdf/ folder.
"""

import csv
import os
import time
import requests
from pathlib import Path

OUTPUT_DIR = "pdf"
CSV_FILE = "csv/llm_bias_papers.csv"
DELAY_BETWEEN_DOWNLOADS = 3  # seconds (be respectful to arXiv servers)


def download_pdf(arxiv_id, output_dir):
    """Download a PDF for a given arXiv ID."""
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    output_path = os.path.join(output_dir, f"{arxiv_id}.pdf")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"  Downloading {arxiv_id}...", end=' ')
        response = requests.get(pdf_url, headers=headers, timeout=60)
        response.raise_for_status()

        if len(response.content) < 1000:
            print(f"✗ Error: Downloaded file too small ({len(response.content)} bytes)")
            return False

        with open(output_path, 'wb') as f:
            f.write(response.content)

        print(f"✓ ({len(response.content) / 1024:.1f} KB)")
        return True

    except requests.RequestException as e:
        print(f"✗ Error: {e}")
        return False


def main():
    print("=" * 70)
    print("Download PDFs for llm_bias_papers.csv")
    print("=" * 70)

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Load paper IDs from CSV
    paper_ids = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row.get('paper_id', '').strip()
            if pid:
                paper_ids.append(pid)

    print(f"Papers in CSV: {len(paper_ids)}")

    # Check which already exist
    existing_pdfs = {f.stem for f in Path(OUTPUT_DIR).glob("*.pdf")}
    to_download = [pid for pid in paper_ids if pid not in existing_pdfs]

    print(f"Already in pdf/: {len(paper_ids) - len(to_download)}")
    print(f"To download: {len(to_download)}")
    print(f"Delay between downloads: {DELAY_BETWEEN_DOWNLOADS}s")
    print("=" * 70)

    if not to_download:
        print("Nothing to download.")
        return

    downloaded = 0
    failed = 0

    for i, arxiv_id in enumerate(to_download):
        print(f"[{i + 1}/{len(to_download)}]", end='')
        result = download_pdf(arxiv_id, OUTPUT_DIR)
        if result:
            downloaded += 1
        else:
            failed += 1

        if i < len(to_download) - 1:
            time.sleep(DELAY_BETWEEN_DOWNLOADS)

    print("\n" + "=" * 70)
    print("Download Complete!")
    print("=" * 70)
    print(f"Newly downloaded: {downloaded}")
    print(f"Failed: {failed}")
    print(f"Already existed: {len(paper_ids) - len(to_download)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
