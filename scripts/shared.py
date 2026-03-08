"""
Shared utilities for the arxiv_benchmark_papers analysis pipeline.

Contains common classes and functions used across multiple scripts:
- API key warning suppression
- RateLimiter, ErrorTracker, and custom exceptions
- File I/O helpers (load_csv_metadata, load_failed_files, save_json)
- Paper utility functions (get_arxiv_url, check_mormon_mention, filter_religion_papers)
"""

import os
import csv
import json
import time
import threading

from dotenv import load_dotenv

# Load environment variables and suppress the dual API key warning
load_dotenv()
if os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
    del os.environ["GEMINI_API_KEY"]

from google import genai
from google.genai import types
from tqdm import tqdm


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ITERATION_TIMEOUT = 120  # 2 minutes


# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------

class ResourceExhaustedError(Exception):
    """Raised when API returns resource exhausted error."""
    pass


class IterationTimeoutError(Exception):
    """Raised when a single iteration takes too long."""
    pass


# ---------------------------------------------------------------------------
# Thread-safe helpers
# ---------------------------------------------------------------------------

class ErrorTracker:
    """Thread-safe error counter."""
    def __init__(self, max_errors: int = 5):
        self.max_errors = max_errors
        self.error_count = 0
        self.lock = threading.Lock()
        self.should_exit = threading.Event()
    
    def record_resource_exhausted(self):
        with self.lock:
            self.error_count += 1
            if self.error_count >= self.max_errors:
                self.should_exit.set()
                return True
        return False
    
    def check_exit(self) -> bool:
        return self.should_exit.is_set()


class RateLimiter:
    """Thread-safe rate limiter using Condition for efficient waiting."""
    def __init__(self, max_calls: int, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def wait_for_token(self):
        """Blocks until a token is available."""
        with self.condition:
            while True:
                now = time.time()
                # Remove calls older than period
                self.calls = [t for t in self.calls if now - t < self.period]
                
                if len(self.calls) < self.max_calls:
                    self.calls.append(now)
                    return
                
                # Calculate wait time until oldest call expires
                if self.calls:
                    wait_time = self.calls[0] + self.period - now + 0.1
                else:
                    wait_time = 1
                
                # Wait with timeout, releases lock while waiting
                self.condition.wait(timeout=max(0.1, wait_time))
    
    def release_slot(self):
        """Notify waiting threads that a slot may be available."""
        with self.condition:
            self.condition.notify_all()


# ---------------------------------------------------------------------------
# File I/O helpers
# ---------------------------------------------------------------------------

def load_csv_metadata(csv_file: str) -> dict:
    """Load CSV file and return dict mapping filename to metadata."""
    metadata = {}
    if not os.path.exists(csv_file):
        return metadata
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row.get('filename', '')
            if filename:
                metadata[filename] = row
    return metadata


def load_failed_files(failures_csv: str) -> set[str]:
    """Load filenames that previously failed with non-retryable errors."""
    if not os.path.exists(failures_csv):
        return set()
    
    failed = set()
    with open(failures_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row.get('filename', '')
            error = row.get('error', '').lower()
            # Skip resource exhausted errors - these should be retried
            if 'resource exhausted' in error or '429' in error or 'quota' in error:
                continue
            if filename:
                failed.add(filename)
    return failed


def save_json(data: dict, output_dir: str, filename: str):
    """Save data to a JSON file, creating the directory if needed."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    json_path = os.path.join(output_dir, filename.replace('.pdf', '.json'))
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        tqdm.write(f"Warning: Failed to save JSON for {filename}: {e}")


# ---------------------------------------------------------------------------
# Paper utility functions
# ---------------------------------------------------------------------------

def get_arxiv_url(filename: str) -> str:
    """Convert filename to arxiv PDF URL."""
    arxiv_id = filename.replace('.pdf', '').replace('.json', '')
    return f"https://arxiv.org/pdf/{arxiv_id}"


def check_mormon_mention(paper: dict) -> bool:
    """Check if paper mentions Mormon or Latter-day Saints."""
    text_to_check = json.dumps(paper).lower()
    return 'mormon' in text_to_check or 'latter-day saints' in text_to_check


def filter_religion_papers(data: list[dict]) -> list[dict]:
    """Filter papers to only include those with religion_component of 'major' or 'minor'."""
    return [p for p in data if p.get('religion_component', '').lower() in ('major', 'minor')]
