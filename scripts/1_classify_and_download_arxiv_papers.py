#!/usr/bin/env python3
"""
arXiv Paper Downloader

Queries papers from arXiv (all categories), uses Gemini to classify which ones
study bias, fairness, religion, ethics, or morality in NLP/LLMs, downloads
qualifying papers, and updates llm_bias_papers.csv.
"""

import argparse
import concurrent.futures
import csv
import json
import os
import random
import re
import sys
import threading
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

from shared import (
    genai, types,
    ResourceExhaustedError,
    ErrorTracker, RateLimiter,
    sanitize_arxiv_id,
)


DEFAULT_MODEL = "gemini-3-flash-preview"
MAX_PAPERS = 4000

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent

OUTPUT_DIR = "pdf"
CSV_FILE = "utility_files/llm_bias_papers.csv"
ASSESSMENT_CACHE_FILE = "utility_files/download_assessments_cache.json"
SNAPSHOT_FILE = "utility_files/arxiv-metadata-oai-snapshot.json"
ARXIV_API_URL = "http://export.arxiv.org/api/query"


RESULTS_PER_PAGE = 200
DELAY_BETWEEN_API_PAGES = 3  # seconds between arxiv API requests
DELAY_BETWEEN_DOWNLOADS = 3  # seconds between PDF downloads
BATCH_SIZE = 100
API_MAX_RETRIES = 3  # retries per API page on server errors

# RSS feed settings (fallback when API is down)
RSS_BASE_URL = "https://rss.arxiv.org/rss"
# All top-level arXiv archives (mirrors the API's "all categories" behavior)
RSS_CATEGORIES = [
    "cs", "econ", "eess", "math", "physics", "q-bio", "q-fin", "stat",
    "astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph",
    "hep-th", "math-ph", "nlin", "nucl-ex", "nucl-th", "quant-ph",
]


# ---------------------------------------------------------------------------
# Snapshot & Cache helpers
# ---------------------------------------------------------------------------

def load_snapshot_papers(snapshot_path: str, skip_ids: set[str]) -> tuple[set[str], list[dict]]:
    """Stream the JSONL snapshot file and return (all_ids, unprocessed_papers).

    The file is ~5GB so we stream line-by-line.
    - all_ids: every arXiv ID in the snapshot (for skipping during API fetch)
    - unprocessed_papers: papers whose ID is NOT in skip_ids, shaped like API results
    """
    all_ids = set()
    unprocessed = []

    if not os.path.isfile(snapshot_path):
        print(f"  Snapshot file not found: {snapshot_path}")
        return all_ids, unprocessed

    print(f"  Streaming snapshot from {snapshot_path}...")
    line_count = 0
    for line in open(snapshot_path, 'r', encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        try:
            paper = json.loads(line)
        except json.JSONDecodeError:
            continue

        arxiv_id = paper.get('id', '')
        if not arxiv_id:
            continue

        all_ids.add(arxiv_id)
        line_count += 1

        if line_count % 500_000 == 0:
            print(f"    Scanned {line_count:,} papers ({len(unprocessed):,} unprocessed so far)...")

        # Skip if already assessed or downloaded
        if arxiv_id in skip_ids:
            continue

        # Extract fields matching the API paper format
        title = paper.get('title', '').replace('\n', ' ').strip()
        title = re.sub(r'\s+', ' ', title)
        abstract = paper.get('abstract', '').strip()

        # Skip papers without abstract (can't classify)
        if not abstract:
            continue

        # Extract date from versions list or update_date
        versions = paper.get('versions', [])
        pub_date = versions[0].get('created', '')[:10] if versions else ''
        upd_date = paper.get('update_date', pub_date)

        unprocessed.append({
            'arxiv_id': arxiv_id,
            'title': title,
            'abstract': abstract,
            'published': pub_date,
            'updated': upd_date,
        })

    print(f"  Scanned {line_count:,} total papers. {len(unprocessed):,} unprocessed.")
    # Sort by ID descending so newer papers are processed first
    unprocessed.sort(key=lambda p: p['arxiv_id'], reverse=True)
    return all_ids, unprocessed


def load_assessment_cache(cache_path: str) -> dict[str, bool]:
    """Load Gemini assessment cache: {arxiv_id: bool}."""
    if not os.path.isfile(cache_path):
        return {}
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_assessment_cache(cache: dict[str, bool], cache_path: str):
    """Persist the assessment cache to disk."""
    os.makedirs(os.path.dirname(cache_path) or '.', exist_ok=True)
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2)


# ---------------------------------------------------------------------------
# arXiv API
# ---------------------------------------------------------------------------

def fetch_recent_papers(max_papers: int = MAX_PAPERS,
                        per_page: int = RESULTS_PER_PAGE) -> list[dict]:
    """Fetch the most recent papers from arXiv API (all categories)."""
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    all_papers = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for start in range(0, max_papers, per_page):
        batch_size = min(per_page, max_papers - start)
        url = (
            f"{ARXIV_API_URL}?search_query=all:*"
            f"&sortBy=submittedDate&sortOrder=descending"
            f"&start={start}&max_results={batch_size}"
        )
        print(f"  Fetching papers {start + 1}-{start + batch_size}...")

        resp = None
        for attempt in range(API_MAX_RETRIES):
            try:
                resp = requests.get(url, headers=headers, timeout=30)
                if resp.status_code >= 500:
                    wait = (2 ** attempt) * 3 + random.uniform(0, 2)
                    print(f"  Server error ({resp.status_code}), retrying in {wait:.0f}s "
                          f"(attempt {attempt + 1}/{API_MAX_RETRIES})...")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                break
            except requests.RequestException as e:
                if attempt < API_MAX_RETRIES - 1:
                    wait = (2 ** attempt) * 3 + random.uniform(0, 2)
                    print(f"  Error: {e}, retrying in {wait:.0f}s "
                          f"(attempt {attempt + 1}/{API_MAX_RETRIES})...")
                    time.sleep(wait)
                else:
                    print(f"  Error fetching page after {API_MAX_RETRIES} attempts: {e}")
                    return all_papers

        if resp is None or resp.status_code >= 500:
            print(f"  API unavailable after {API_MAX_RETRIES} attempts, stopping.")
            return all_papers

        root = ET.fromstring(resp.content)
        entries = root.findall('atom:entry', ns)

        if not entries:
            print("  No more entries returned.")
            break

        for entry in entries:
            id_text = entry.find('atom:id', ns).text  # http://arxiv.org/abs/XXXX.XXXXXvN
            arxiv_id = id_text.split('/abs/')[-1]
            # Strip version suffix (e.g. v1, v2)
            arxiv_id = re.sub(r'v\d+$', '', arxiv_id)

            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None else "Unknown"
            # Collapse multiple spaces
            title = re.sub(r'\s+', ' ', title)

            summary_elem = entry.find('atom:summary', ns)
            abstract = summary_elem.text.strip() if summary_elem is not None else ""

            published = entry.find('atom:published', ns)
            updated = entry.find('atom:updated', ns)
            pub_date = published.text[:10] if published is not None else ""
            upd_date = updated.text[:10] if updated is not None else pub_date

            all_papers.append({
                'arxiv_id': arxiv_id,
                'title': title,
                'abstract': abstract,
                'published': pub_date,
                'updated': upd_date,
            })

        print(f"  Got {len(entries)} entries (total so far: {len(all_papers)})")

        if len(entries) < batch_size:
            break

        if start + per_page < max_papers:
            time.sleep(DELAY_BETWEEN_API_PAGES)

    return all_papers


def fetch_rss_papers(categories: list[str] = None) -> list[dict]:
    """Fetch recent papers from arXiv RSS feeds (fallback when API is down).

    RSS feeds are updated daily and served from separate infrastructure.
    Returns papers in the same format as fetch_recent_papers().
    """
    if categories is None:
        categories = RSS_CATEGORIES

    # Combine categories with + for a single request (up to 2000 items)
    cat_str = "+".join(categories)
    url = f"{RSS_BASE_URL}/{cat_str}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    print(f"  Fetching RSS feed: {url}")
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  Error fetching RSS feed: {e}")
        return []

    root = ET.fromstring(resp.content)
    all_papers = []
    seen_ids = set()
    today = time.strftime('%Y-%m-%d')

    for item in root.iter('item'):
        # Extract arXiv ID from <link> (e.g. http://arxiv.org/abs/2603.12345v1)
        link_elem = item.find('link')
        if link_elem is None or not link_elem.text:
            continue
        link = link_elem.text.strip()
        arxiv_id = link.split('/abs/')[-1] if '/abs/' in link else ''
        arxiv_id = re.sub(r'v\d+$', '', arxiv_id)
        if not arxiv_id or arxiv_id in seen_ids:
            continue
        seen_ids.add(arxiv_id)

        # Title
        title_elem = item.find('title')
        title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None and title_elem.text else "Unknown"
        # RSS titles often have a prefix like "Title. (arXiv:2603.12345v1 ...)"
        # Clean up the arXiv ID suffix if present
        title = re.sub(r'\s*\(arXiv:[^)]+\)\s*$', '', title)
        title = re.sub(r'\s+', ' ', title)

        # Abstract from <description>
        desc_elem = item.find('description')
        abstract = ""
        if desc_elem is not None and desc_elem.text:
            desc = desc_elem.text.strip()
            # The description often contains HTML with <p> tags
            # Remove HTML tags
            abstract = re.sub(r'<[^>]+>', ' ', desc)
            abstract = re.sub(r'\s+', ' ', abstract).strip()
            # Strip RSS metadata prefix: "arXiv:XXXX.XXXXXv1 Announce Type: new Abstract: "
            abstract = re.sub(r'^arXiv:\S+\s+Announce Type:\s*\w+\s+Abstract:\s*', '', abstract)

        if not abstract:
            continue

        all_papers.append({
            'arxiv_id': arxiv_id,
            'title': title,
            'abstract': abstract,
            'published': today,
            'updated': today,
        })

    print(f"  Got {len(all_papers)} papers from RSS feed")
    return all_papers


# ---------------------------------------------------------------------------
# Gemini classification
# ---------------------------------------------------------------------------

def classify_batch(batch: list[dict], api_key: str, rate_limiter: RateLimiter,
                   model_name: str, error_tracker: ErrorTracker,
                   max_retries: int = 3) -> list[bool]:
    """Classify a batch of abstracts. Returns list of bools (True = relevant paper)."""
    if error_tracker.check_exit():
        raise ResourceExhaustedError("Too many errors, stopping.")

    abstracts_text = ""
    for i, paper in enumerate(batch):
        abstracts_text += f"[{i}] Title: {paper['title']}\nAbstract: {paper['abstract']}\n\n"

    prompt = f"""You are classifying academic paper abstracts. For each abstract below, determine whether the paper is relevant to ANY of the following topics in the context of Large Language Models (LLMs), Language Models (LMs), Natural Language Processing (NLP), or AI systems:

**1. Bias & Fairness**
- Social bias (gender, race, religion, age, disability, etc.)
- Fairness or discrimination in NLP/LLM systems
- Benchmarks or datasets for measuring bias

**2. Morality & Moral Reasoning**
- Moral reasoning, moral bias, moral judgment, moral pluralism
- Moral dilemmas, moral benchmarks, moral datasets
- Cultural morality, societal values

**3. Ethics & Ethical Reasoning**
- Ethical reasoning, ethical frameworks, ethical bias
- Ethical judgment, ethical dilemmas
- Ethics benchmarks, ethics datasets
- Secular ethics, secular morality
- Normative reasoning, deontology, consequentialism, utilitarianism
- Virtue ethics, value pluralism, value systems

**4. Religion**
- Religious representation, inclusion of religion
- Discussion of religion, religious values
- How LLMs handle, represent, or respond to religious topics, beliefs, or groups

A paper qualifies if it studies, evaluates, benchmarks, or measures any of the above topics in LLMs, language models, or NLP systems.

A paper does NOT qualify if it:
- Only mentions these topics in passing or as future work
- Deals with statistical/mathematical bias (e.g. inductive bias, selection bias) rather than social bias
- Studies bias in non-NLP domains only (computer vision, recommender systems without text)
- Discusses AI ethics policy/governance without evaluating LLM behavior

Return a JSON array of {len(batch)} booleans (true/false), one per abstract in order.

{abstracts_text}"""

    client = genai.Client(api_key=api_key)
    rate_limiter.wait_for_token()

    last_exception = None
    for attempt in range(max_retries):
        try:
            if error_tracker.check_exit():
                raise ResourceExhaustedError("Too many errors, stopping.")

            response = client.models.generate_content(
                model=model_name,
                contents=[prompt],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            results = json.loads(response.text)

            if isinstance(results, list) and len(results) == len(batch):
                return results
            elif isinstance(results, list):
                print(f"  Warning: got {len(results)} results for {len(batch)} abstracts, padding.")
                return (results + [False] * len(batch))[:len(batch)]
            else:
                print(f"  Warning: unexpected response type: {type(results)}")
                return [False] * len(batch)

        except Exception as e:
            last_exception = e
            error_str = str(e).lower()

            if "resource exhausted" in error_str or "429" in error_str or "quota" in error_str:
                print(f"  Rate limited, attempt {attempt + 1}/{max_retries}")
                if error_tracker.record_resource_exhausted():
                    raise ResourceExhaustedError("Too many resource exhausted errors.")
                backoff = (2 ** attempt) * 5 + random.uniform(0, 2)
                time.sleep(backoff)
            elif "500" in error_str or "503" in error_str or "server" in error_str:
                print(f"  Server error, attempt {attempt + 1}/{max_retries}")
                backoff = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(backoff)
            else:
                raise e

    raise last_exception


# ---------------------------------------------------------------------------
# PDF download
# ---------------------------------------------------------------------------

def download_pdf(arxiv_id: str, output_dir: str) -> bool:
    """Download a PDF for a given arXiv ID."""
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    safe_id = sanitize_arxiv_id(arxiv_id)
    output_path = os.path.join(output_dir, f"{safe_id}.pdf")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"  Downloading {arxiv_id}...", end=' ')
        response = requests.get(pdf_url, headers=headers, timeout=60)
        response.raise_for_status()

        if len(response.content) < 1000:
            print(f"X Error: Downloaded file too small ({len(response.content)} bytes)")
            return False

        with open(output_path, 'wb') as f:
            f.write(response.content)

        print(f"OK ({len(response.content) / 1024:.1f} KB)")
        return True

    except requests.RequestException as e:
        print(f"X Error: {e}")
        return False


# ---------------------------------------------------------------------------
# Classify & download pipeline (shared by snapshot and API paths)
# ---------------------------------------------------------------------------

def classify_and_download(papers: list[dict], assessment_cache: dict[str, bool],
                          existing_pdfs: set[str], api_key: str, args,
                          rate_limiter: RateLimiter, error_tracker: ErrorTracker,
                          source_label: str) -> list[dict]:
    """Classify papers and download qualifying ones. Returns list of qualifying papers.
    
    Mutates assessment_cache in place and flushes to disk after each batch.
    """
    # Split into papers needing classification vs cached positives needing download
    new_papers = [p for p in papers
                  if p['arxiv_id'] not in assessment_cache
                  and sanitize_arxiv_id(p['arxiv_id']) not in existing_pdfs]
    
    cached_positive_not_downloaded = [
        p for p in papers
        if assessment_cache.get(p['arxiv_id']) is True
        and sanitize_arxiv_id(p['arxiv_id']) not in existing_pdfs
    ]
    
    print(f"  Papers from {source_label}: {len(papers)}")
    print(f"    Already downloaded:            {len([p for p in papers if sanitize_arxiv_id(p['arxiv_id']) in existing_pdfs])}")
    print(f"    Previously assessed:           {len([p for p in papers if p['arxiv_id'] in assessment_cache])}")
    print(f"    New papers to assess:          {len(new_papers)}")
    if cached_positive_not_downloaded:
        print(f"    Cached positive, need download: {len(cached_positive_not_downloaded)}")
    
    if not new_papers and not cached_positive_not_downloaded:
        print(f"  Nothing to do for {source_label}.")
        return []
    
    qualifying_papers = list(cached_positive_not_downloaded)
    
    if new_papers:
        print(f"\n  Classifying {len(new_papers)} abstracts from {source_label} "
              f"({args.workers} workers)...")
        
        batches = [new_papers[i:i + args.batch_size]
                   for i in range(0, len(new_papers), args.batch_size)]
        
        cache_lock = threading.Lock()
        stop_event = threading.Event()
        completed = [0]  # mutable counter for progress
        start_time = time.time()
        
        def process_batch(batch_idx_and_batch):
            batch_idx, batch = batch_idx_and_batch
            if stop_event.is_set():
                return []
            try:
                results = classify_batch(batch, api_key, rate_limiter, args.model, error_tracker)
                positives = sum(results)
                batch_qualifying = []
                
                with cache_lock:
                    completed[0] += 1
                    done = completed[0]
                    elapsed = time.time() - start_time
                    
                    # Build progress line
                    msg = (f"    Batch {done}/{len(batches)} ({len(batch)} papers): "
                           f"{positives} qualifying")
                    
                    # Show ETA every 25 batches
                    if done % 25 == 0:
                        rate = done / elapsed
                        remaining = (len(batches) - done) / rate
                        mins, secs = divmod(int(remaining), 60)
                        hrs, mins = divmod(mins, 60)
                        if hrs > 0:
                            msg += f"  [ETA: {hrs}h {mins}m]"
                        else:
                            msg += f"  [ETA: {mins}m {secs}s]"
                    
                    print(msg)
                    
                    for paper, is_bias in zip(batch, results):
                        assessment_cache[paper['arxiv_id']] = bool(is_bias)
                        if is_bias:
                            batch_qualifying.append(paper)
                    # Flush cache to disk periodically so progress survives crashes
                    if done % 10 == 0:
                        save_assessment_cache(assessment_cache, args.cache)
                
                return batch_qualifying
                
            except ResourceExhaustedError:
                stop_event.set()
                print(f"\n  Stopping classification due to too many API errors.")
                return []
            except Exception as e:
                print(f"    Batch {batch_idx + 1} error: {e}")
                return []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = list(executor.map(process_batch, enumerate(batches)))
        
        for batch_results in futures:
            qualifying_papers.extend(batch_results)
        
        save_assessment_cache(assessment_cache, args.cache)
        
        new_qualifying = len(qualifying_papers) - len(cached_positive_not_downloaded)
        print(f"\n  Found {len(qualifying_papers)} qualifying bias papers "
              f"({new_qualifying} new + {len(cached_positive_not_downloaded)} cached).")
    elif cached_positive_not_downloaded:
        print(f"  {len(cached_positive_not_downloaded)} cached positive papers still need downloading.")
    
    # Download qualifying papers
    if qualifying_papers:
        print(f"\n  Downloading {len(qualifying_papers)} PDFs from {source_label}...")
        downloaded = 0
        failed = 0
        for i, paper in enumerate(qualifying_papers):
            result = download_pdf(paper['arxiv_id'], args.output_dir)
            if result:
                downloaded += 1
                existing_pdfs.add(sanitize_arxiv_id(paper['arxiv_id']))
            else:
                failed += 1
            if i < len(qualifying_papers) - 1:
                time.sleep(DELAY_BETWEEN_DOWNLOADS)
        print(f"  Downloaded: {downloaded}, Failed: {failed}")
    
    return qualifying_papers


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Download arXiv papers that measure bias in NLP/LLMs."
    )
    parser.add_argument("--max-papers", type=int, default=MAX_PAPERS,
                        help=f"Number of recent papers to query from API (default {MAX_PAPERS})")
    parser.add_argument("--output-dir", default=OUTPUT_DIR,
                        help=f"Directory to save PDFs (default {OUTPUT_DIR})")
    parser.add_argument("--csv", default=CSV_FILE,
                        help=f"CSV to append positive results (default {CSV_FILE})")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Gemini model for classification (default {DEFAULT_MODEL})")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE,
                        help=f"Abstracts per Gemini request (default {BATCH_SIZE})")
    parser.add_argument("--rpm", type=int, default=500,
                        help="Gemini requests per minute (default 500)")
    parser.add_argument("--cache", default=ASSESSMENT_CACHE_FILE,
                        help=f"JSON cache for Gemini assessments (default {ASSESSMENT_CACHE_FILE})")
    parser.add_argument("--snapshot", default=SNAPSHOT_FILE,
                        help=f"arXiv metadata snapshot JSONL file (default {SNAPSHOT_FILE})")
    parser.add_argument("--max-errors", type=int, default=5,
                        help="Max resource exhausted errors before exit (default 5)")
    parser.add_argument("--use-snapshot", action="store_true",
                        help="Process unclassified papers from the snapshot file before fetching API papers")
    parser.add_argument("--workers", type=int, default=10,
                        help="Number of concurrent classification threads (default 10)")
    parser.add_argument("--use-rss", action="store_true",
                        help="Use RSS feeds instead of the API for fetching recent papers")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        sys.exit(1)

    print("=" * 70)
    print("arXiv Bias Paper Downloader")
    print("=" * 70)

    # Ensure output dirs exist
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    os.makedirs(os.path.dirname(args.csv) or '.', exist_ok=True)

    # Step 1: Load cache and existing PDFs
    print(f"\nStep 1: Loading cache and existing PDFs...")
    print("-" * 40)
    assessment_cache = load_assessment_cache(args.cache)
    existing_pdfs = {f.stem for f in Path(args.output_dir).glob("*.pdf")}
    existing_json = {f.stem for f in Path("json/2_paper_metadata").glob("*.json")}
    existing_pdfs |= existing_json  # skip classification for papers already in stage 2
    print(f"  Assessment cache: {len(assessment_cache):,} entries")
    print(f"  Existing PDFs:    {len({f.stem for f in Path(args.output_dir).glob('*.pdf')}):,}")
    print(f"  Existing stage 2: {len(existing_json):,}")
    print(f"  Total skip set:   {len(existing_pdfs):,}")

    # Shared rate limiter and error tracker
    rate_limiter = RateLimiter(max_calls=args.rpm, period=60.0)
    error_tracker = ErrorTracker(max_errors=args.max_errors)

    all_qualifying = []

    # Step 2: Process snapshot papers (retroactive)
    if args.use_snapshot:
        print(f"\nStep 2: Scanning snapshot for unprocessed papers...")
        print("-" * 40)
        skip_ids = existing_pdfs | set(assessment_cache.keys())
        snapshot_ids, snapshot_papers = load_snapshot_papers(args.snapshot, skip_ids)

        if snapshot_papers:
            print(f"\n  Processing {len(snapshot_papers):,} unprocessed snapshot papers...")
            qualifying = classify_and_download(
                snapshot_papers, assessment_cache, existing_pdfs,
                api_key, args, rate_limiter, error_tracker,
                source_label="snapshot"
            )
            all_qualifying.extend(qualifying)
        else:
            print("  All snapshot papers already processed.")
    else:
        print(f"\nStep 2: Skipping snapshot (use --use-snapshot to process)")
        snapshot_ids = set()

    # Step 3: Fetch recent papers from arXiv API (or RSS fallback)
    if args.use_rss:
        print(f"\nStep 3: Fetching recent papers from RSS feeds...")
        print("-" * 40)
        api_papers = fetch_rss_papers()
    else:
        print(f"\nStep 3: Fetching last {args.max_papers} papers from arXiv API...")
        print("-" * 40)
        api_papers = fetch_recent_papers(max_papers=args.max_papers)

        if not api_papers:
            print(f"\n  API returned no papers. Falling back to RSS feeds...")
            print("-" * 40)
            api_papers = fetch_rss_papers()

    print(f"\nFetched {len(api_papers)} papers.")

    if api_papers:
        # Filter out papers already in snapshot (already processed or skipped above)
        api_only = [p for p in api_papers if p['arxiv_id'] not in snapshot_ids]
        if len(api_papers) != len(api_only):
            print(f"  Filtered out {len(api_papers) - len(api_only)} papers already in snapshot.")

        if api_only:
            qualifying = classify_and_download(
                api_only, assessment_cache, existing_pdfs,
                api_key, args, rate_limiter, error_tracker,
                source_label="API"
            )
            all_qualifying.extend(qualifying)
        else:
            print("  All API papers already processed via snapshot.")

    # Step 4: Update CSV
    print(f"\nStep 4: Updating {args.csv}...")
    fieldnames = ["paper_id", "latest_date", "title"]
    csv_exists = os.path.isfile(args.csv)

    existing_csv_ids = set()
    if csv_exists:
        with open(args.csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_csv_ids.add(row.get('paper_id', ''))

    new_csv_rows = []
    for paper in all_qualifying:
        if paper['arxiv_id'] not in existing_csv_ids:
            new_csv_rows.append({
                'paper_id': paper['arxiv_id'],
                'latest_date': paper['updated'],
                'title': paper['title'],
            })

    if new_csv_rows:
        with open(args.csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not csv_exists:
                writer.writeheader()
            writer.writerows(new_csv_rows)
        print(f"  Added {len(new_csv_rows)} new entries to {args.csv}")
    else:
        print(f"  No new entries to add (all already in CSV).")

    # Summary
    print("\n" + "=" * 70)
    print("Done!")
    print("=" * 70)
    print(f"  Total qualifying: {len(all_qualifying)}")
    print(f"  CSV entries added: {len(new_csv_rows)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
