#!/usr/bin/env python3
"""
arXiv PDF Downloader
Downloads PDFs from arXiv search results with rate limiting and progress tracking.
"""

import requests
from bs4 import BeautifulSoup
import time
import os
from pathlib import Path
from urllib.parse import urljoin
import re
import csv
from datetime import datetime

# Searches for papers with "benchmark", "evaluate", "quantify", "measure", or "dataset" in the title, 2017-2026
BASE_URL = "https://arxiv.org"
# Template for yearly search - we will format with {year}
SEARCH_URL_TEMPLATE = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=benchmark&terms-0-field=title&terms-1-operator=OR&terms-1-term=evaluate&terms-1-field=title&terms-2-operator=OR&terms-2-term=quantify&terms-2-field=title&terms-3-operator=OR&terms-3-term=measure&terms-3-field=title&terms-4-operator=OR&terms-4-term=dataset&terms-4-field=title&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=date_range&date-year=&date-from_date={year}-01-01&date-to_date={year}-12-31&date-date_type=submitted_date&abstracts=hide&size=200&order=-submitted_date"
OUTPUT_DIR = "pdf"
MAX_PAPERS = 50_000
RESULTS_PER_PAGE = 200
DELAY_BETWEEN_DOWNLOADS = 3  # seconds (be respectful to arXiv servers)
DELAY_BETWEEN_PAGES = 10  # seconds
START_YEAR = 2026
END_YEAR = 2026

def create_output_directory():
    """Create output directory if it doesn't exist."""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

def get_search_page(year_url, start=0):
    """Fetch a search results page."""
    url = f"{year_url}&start={start}"
    print(f"Fetching search page: start={start}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching search page: {e}")
        return None

def extract_paper_info(html_content):
    """Extract arXiv paper information from search results page."""
    soup = BeautifulSoup(html_content, 'html.parser')
    papers = []
    
    # Find all paper entries
    results = soup.find_all('li', class_='arxiv-result')
    
    for result in results:
        paper_info = {}
        
        # Extract arXiv ID
        link = result.find('p', class_='list-title')
        if link and link.find('a'):
            href = link.find('a')['href']
            match = re.search(r'/abs/(\d+\.\d+)', href)
            if match:
                paper_info['arxiv_id'] = match.group(1)
            else:
                continue
        else:
            continue
        
        # Extract title
        title_elem = result.find('p', class_='title')
        if title_elem:
            paper_info['title'] = title_elem.get_text(strip=True)
        else:
            paper_info['title'] = "Unknown"
        
        # Extract submitted date
        date_elem = result.find('p', class_='is-size-7')
        if date_elem:
            date_text = date_elem.get_text()
            # Look for "Submitted DD Month YYYY" pattern
            date_match = re.search(r'Submitted\s+(\d+)\s+(\w+),?\s+(\d{4})', date_text)
            if date_match:
                day = date_match.group(1)
                month = date_match.group(2)
                year = date_match.group(3)
                
                # Convert month name to number
                try:
                    date_obj = datetime.strptime(f"{day} {month} {year}", "%d %B %Y")
                    paper_info['submitted_date'] = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    # Try abbreviated month
                    try:
                        date_obj = datetime.strptime(f"{day} {month} {year}", "%d %b %Y")
                        paper_info['submitted_date'] = date_obj.strftime("%Y-%m-%d")
                    except ValueError:
                        paper_info['submitted_date'] = "Unknown"
            else:
                paper_info['submitted_date'] = "Unknown"
        else:
            paper_info['submitted_date'] = "Unknown"
        
        papers.append(paper_info)
    
    return papers

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
        
        # Validate that we got actual content
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
    """Main function to orchestrate the download process."""
    print("=" * 70)
    print("arXiv PDF Downloader (Yearly Search)")
    print("=" * 70)
    print(f"Target: {MAX_PAPERS} papers (global limit)")
    print(f"Query: benchmark (in title)")
    print(f"Query: benchmark (in title)")
    print(f"Years: {START_YEAR}-{END_YEAR}")
    print(f"Delay between downloads: {DELAY_BETWEEN_DOWNLOADS}s")
    print("=" * 70)
    print()
    
    create_output_directory()
    
    # Check for existing files
    existing_files = list(Path(OUTPUT_DIR).glob("*.pdf"))
    if existing_files:
        print(f"Found {len(existing_files)} existing PDF files in {OUTPUT_DIR}")
        print("These will be skipped (resuming download)\n")
    
    downloaded_count = 0
    skipped_count = 0
    failed_count = 0
    
    # Iterate through each year
    for year in range(START_YEAR, END_YEAR + 1):
        if downloaded_count + skipped_count >= MAX_PAPERS:
            break
            
        print(f"\n" + "="*30)
        print(f"Processing Year: {year}")
        print("="*30)
        
        # Construct URL for this year
        year_url = SEARCH_URL_TEMPLATE.format(year=year)
        
        # Reset counters for this year (just for tracking progress within year if we wanted, but we use global break)
        # We need to page through results for this year
        
        # We don't know exact total pages for the year without scraping, so we loop until no results
        # We can safely estimate a high number or just loop with while True
        
        page_num = 0
        while True:
            if downloaded_count + skipped_count >= MAX_PAPERS:
                break
                
            start = page_num * RESULTS_PER_PAGE
            
            print(f"\n--- Year {year} | Page {page_num + 1} (start={start}) ---")
            
            # Fetch search results page
            html_content = get_search_page(year_url, start)
            if not html_content:
                print("Failed to fetch page, skipping to next year...")
                break # Skip to next year if page fetch fails completely
            
            # Extract arXiv paper information
            papers = extract_paper_info(html_content)
            print(f"Found {len(papers)} papers on this page")
            
            if not papers:
                print(f"No more results found for {year}, moving to next year...")
                break
            
            # Download PDFs
            for i, paper in enumerate(papers):
                if downloaded_count + skipped_count >= MAX_PAPERS:
                    break
                
                arxiv_id = paper['arxiv_id']
                print(f"[{downloaded_count + skipped_count + 1}/{MAX_PAPERS}] ({year}) ", end='')
                
                # Check if file already exists
                output_path = os.path.join(OUTPUT_DIR, f"{arxiv_id}.pdf")
                was_downloaded = False
                
                if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                    file_size = os.path.getsize(output_path)
                    print(f"  Skipping {arxiv_id} (already exists, {file_size / 1024:.1f} KB)")
                    skipped_count += 1
                else:
                    result = download_pdf(arxiv_id, OUTPUT_DIR)
                    if result:
                        downloaded_count += 1
                        was_downloaded = True
                    else:
                        failed_count += 1
                
                # Rate limiting
                if was_downloaded and i < len(papers) - 1:
                    time.sleep(DELAY_BETWEEN_DOWNLOADS)
            
            # Wait before fetching next page
            time.sleep(DELAY_BETWEEN_PAGES)
            page_num += 1
            
            # Safety break to prevent infinite loops if something is weird
            if page_num > 100: # 100 * 200 = 20,000 papers per year is plenty
                print(f"Reached safety limit of 100 pages for year {year}, moving to next year...")
                break

    # Summary
    print("\n" + "=" * 70)
    print("Download Complete!")
    print("=" * 70)
    print(f"Newly downloaded: {downloaded_count} papers")
    print(f"Skipped (already existed): {skipped_count} papers")
    print(f"Failed downloads: {failed_count}")
    print(f"Total processed: {downloaded_count + skipped_count} papers")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    main()
