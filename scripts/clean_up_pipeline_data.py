#!/usr/bin/env python3
"""
Pipeline Data Cleanup

Validates JSON data across pipeline stages and identifies:
- Papers matching download criteria that are missing PDFs
- JSON files that no longer meet pipeline criteria (can be removed)
- Missing JSON files that should exist based on upstream data (can be generated)

Download criteria (papers must have is_llm_related=True AND at least one of:
  is_bias_related, is_faith_ethics_related, bias_and_fairness,
  moral_reasoning, ethics, religion)

Pipeline stages:
  Step 2: json/2_paper_metadata     — one JSON per PDF in pdf/
  Step 3: json/3_paper_bias_targets — only papers where 2_paper_metadata has
           is_llm_related=True AND is_bias_related=True
  Step 4: json/4_religious_bias_analysis — only papers from step 3 whose
           bias_targets contain a religious bias component
"""

import argparse
import glob
import json
import os
import subprocess
import time
from pathlib import Path

import requests

# Religious bias keywords (mirrored from 4_extract_paper_details.py)
_RELIGIOUS_KEYWORDS = [
    'relig', 'faith', 'spiritual', 'theolog',
    'islam', 'muslim', 'christian', 'jewish', 'hindu',
    'buddhis', 'sikh', 'mormon', 'latter-day',
    'antisemit',
]

# Tags that qualify a paper for download when combined with is_llm_related
_DOWNLOAD_QUALIFYING_TAGS = [
    'is_bias_related',
    'is_faith_ethics_related',
    'bias_and_fairness',
    'moral_reasoning',
    'ethics',
    'religion',
]

DELAY_BETWEEN_DOWNLOADS = 3  # seconds between PDF downloads
ASSESSMENT_CACHE_FILE = "utility_files/download_assessments_cache.json"
FAILED_DOWNLOADS_CACHE_FILE = "utility_files/failed_downloads_cache.json"


def _has_religious_bias(second_pass_data: dict) -> bool:
    """Check whether any bias_targets or primary_bias_target mention religious bias."""
    targets = second_pass_data.get('bias_targets', [])
    texts = [t.get('target', '') if isinstance(t, dict) else str(t) for t in targets]
    texts.append(second_pass_data.get('primary_bias_target', ''))

    for text in texts:
        lowered = text.lower()
        if 'faithfulness' in lowered:
            continue
        if any(kw in lowered for kw in _RELIGIOUS_KEYWORDS):
            return True
    return False


def _meets_download_criteria(data: dict) -> bool:
    """Check whether a paper's metadata meets the expanded download criteria.

    Returns True when is_llm_related is True AND at least one qualifying tag
    (is_bias_related, is_faith_ethics_related, bias_and_fairness,
    moral_reasoning, ethics, religion) is True.
    """
    if data.get('is_llm_related') is not True:
        return False
    return any(data.get(tag) is True for tag in _DOWNLOAD_QUALIFYING_TAGS)


def download_pdf(arxiv_id: str, output_dir: str) -> str:
    """Download a PDF for a given arXiv ID.

    Returns:
        'ok'             – downloaded successfully
        'permanent_fail' – paper withdrawn or permanently unavailable (don't retry)
        'transient_fail' – temporary error (retry later)
    """
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    output_path = os.path.join(output_dir, f"{arxiv_id}.pdf")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"     Downloading {arxiv_id}...", end=' ')
        response = requests.get(pdf_url, headers=headers, timeout=60)

        if response.status_code in (403, 404, 410):
            print(f"SKIPPED (HTTP {response.status_code} - unavailable/withdrawn)")
            return 'permanent_fail'

        response.raise_for_status()

        # Check for arXiv "withdrawn" HTML page served as PDF
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' in content_type:
            print(f"SKIPPED (HTML response - likely withdrawn)")
            return 'permanent_fail'

        if len(response.content) < 1000:
            print(f"SKIPPED (too small: {len(response.content)} bytes - likely withdrawn)")
            return 'permanent_fail'

        with open(output_path, 'wb') as f:
            f.write(response.content)

        print(f"OK ({len(response.content) / 1024:.1f} KB)")
        return 'ok'

    except requests.RequestException as e:
        print(f"X Error: {e}")
        return 'transient_fail'


def audit_downloads(step2_dir: str, pdf_dir: str, skip_ids: set[str]) -> list[str]:
    """Check that every paper meeting download criteria has a PDF.

    Returns list of stems (arXiv IDs) that are eligible but have no PDF.
    Papers in skip_ids (failed cache) are excluded.
    """
    pdf_stems = set()
    if os.path.isdir(pdf_dir):
        pdf_stems = {Path(f).stem for f in glob.glob(os.path.join(pdf_dir, "*.pdf"))}

    missing = []
    for jf in glob.glob(os.path.join(step2_dir, "*.json")):
        data = load_json(jf)
        if data and _meets_download_criteria(data):
            stem = Path(jf).stem
            if stem not in pdf_stems and stem not in skip_ids:
                missing.append(stem)

    return sorted(missing)


def audit_cache_downloads(cache_path: str, pdf_dir: str, skip_ids: set[str]) -> list[str]:
    """Check that every paper marked True in the assessment cache has a PDF.

    Returns list of arXiv IDs that were assessed as relevant but have no PDF.
    Papers in skip_ids (failed cache) are excluded.
    """
    cache = load_json(cache_path)
    if not cache or not isinstance(cache, dict):
        return []

    pdf_stems = set()
    if os.path.isdir(pdf_dir):
        pdf_stems = {Path(f).stem for f in glob.glob(os.path.join(pdf_dir, "*.pdf"))}

    missing = [
        aid for aid, val in cache.items()
        if val is True and aid not in pdf_stems and aid not in skip_ids
    ]
    return sorted(missing)


def load_json(path: str) -> dict | None:
    """Load a JSON file, returning None on failure."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def get_stems(directory: str) -> set[str]:
    """Get the set of file stems (no extension) from a directory of JSON files."""
    if not os.path.isdir(directory):
        return set()
    return {Path(f).stem for f in glob.glob(os.path.join(directory, "*.json"))}


def audit_step2(pdf_dir: str, step2_dir: str) -> tuple[list[str], list[str]]:
    """
    Step 2 (paper metadata): should have one JSON per PDF.
    Returns (orphaned_jsons, missing_jsons).
    """
    pdf_stems = set()
    if os.path.isdir(pdf_dir):
        for f in glob.glob(os.path.join(pdf_dir, "*.pdf")):
            pdf_stems.add(Path(f).stem)
    
    json_stems = get_stems(step2_dir)
    
    orphaned = sorted(json_stems - pdf_stems)
    missing = sorted(pdf_stems - json_stems)
    
    return orphaned, missing


def audit_step3(step2_dir: str, step3_dir: str) -> tuple[list[str], list[str]]:
    """
    Step 3 (bias targets): should only have entries where step 2 has
    is_llm_related=True AND is_bias_related=True.
    Returns (invalid_jsons, missing_jsons).
    """
    # Build set of eligible papers from step 2
    eligible = set()
    for jf in glob.glob(os.path.join(step2_dir, "*.json")):
        data = load_json(jf)
        if data and data.get('is_llm_related') is True and data.get('is_bias_related') is True:
            eligible.add(Path(jf).stem)
    
    step3_stems = get_stems(step3_dir)
    
    # Invalid: in step 3 but not eligible from step 2
    invalid = sorted(step3_stems - eligible)
    
    # Missing: eligible from step 2 but not in step 3
    missing = sorted(eligible - step3_stems)
    
    return invalid, missing


def audit_step4(step2_dir: str, step3_dir: str, step4_dir: str) -> tuple[list[str], list[str]]:
    """
    Step 4 (religious bias analysis): should only have entries where:
    - step 2 has is_llm_related=True AND is_bias_related=True
    - step 3 bias_targets contain a religious bias component
    Returns (invalid_jsons, missing_jsons).
    """
    eligible = set()
    for jf in glob.glob(os.path.join(step3_dir, "*.json")):
        stem = Path(jf).stem
        
        # Verify step 2 eligibility
        step2_path = os.path.join(step2_dir, f"{stem}.json")
        step2_data = load_json(step2_path)
        if not step2_data:
            continue
        if step2_data.get('is_llm_related') is not True or step2_data.get('is_bias_related') is not True:
            continue
        
        # Check religious bias in step 3 data
        step3_data = load_json(jf)
        if step3_data and _has_religious_bias(step3_data):
            eligible.add(stem)
    
    step4_stems = get_stems(step4_dir)
    
    invalid = sorted(step4_stems - eligible)
    missing = sorted(eligible - step4_stems)
    
    return invalid, missing


def print_section(title: str, items: list[str], label: str, directory: str):
    """Print a list of files with a header."""
    if not items:
        print(f"  OK: No {label} files.")
        return
    print(f"  WARNING: {len(items)} {label} file(s):")
    for stem in items[:20]:
        print(f"     - {stem}.json")
    if len(items) > 20:
        print(f"     ... and {len(items) - 20} more")


def delete_files(stems: list[str], directory: str):
    """Delete JSON files by stem name from a directory."""
    deleted = 0
    for stem in stems:
        path = os.path.join(directory, f"{stem}.json")
        if os.path.isfile(path):
            os.remove(path)
            deleted += 1
    print(f"  DELETED: Deleted {deleted} file(s) from {directory}")


def run_pipeline_step(command: list[str], description: str) -> bool:
    """Run a pipeline script via subprocess. Returns True if successful."""
    print(f"\n  REGEN: Regenerating: {description}")
    print(f"     Running: {' '.join(command)}")
    print()
    try:
        result = subprocess.run(command, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"\n  OK: {description} completed successfully.")
            return True
        else:
            print(f"\n  ERROR: {description} exited with code {result.returncode}.")
            return False
    except KeyboardInterrupt:
        print(f"\n  WARNING: {description} interrupted by user.")
        return False
    except Exception as e:
        print(f"\n  ERROR: Failed to run {description}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Validate and clean up pipeline JSON data across stages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Pipeline stages:
  Step 2: json/2_paper_metadata          — one JSON per PDF
  Step 3: json/3_paper_bias_targets      — LLM + bias papers only
  Step 4: json/4_religious_bias_analysis  — religious bias papers only
        """
    )
    parser.add_argument("--pdf-dir", default="pdf", help="Directory with PDFs")
    parser.add_argument("--step2-dir", default="json/2_paper_metadata", help="Step 2 JSON directory")
    parser.add_argument("--step3-dir", default="json/3_paper_bias_targets", help="Step 3 JSON directory")
    parser.add_argument("--step4-dir", default="json/4_religious_bias_analysis", help="Step 4 JSON directory")
    parser.add_argument("--cache", default=ASSESSMENT_CACHE_FILE,
                        help=f"Assessment cache JSON (default {ASSESSMENT_CACHE_FILE})")
    parser.add_argument("--apply", action="store_true", help="Actually delete invalid files and regenerate missing ones")
    
    args = parser.parse_args()
    apply = args.apply
    
    print("=" * 60)
    print("Pipeline Data Cleanup" + ("" if apply else "  [DRY RUN]"))
    print("=" * 60)
    
    total_invalid = 0
    total_missing = 0
    total_deleted = 0
    total_downloaded = 0

    # Load failed-downloads cache
    failed_cache_path = FAILED_DOWNLOADS_CACHE_FILE
    failed_cache = load_json(failed_cache_path) or {}
    if not isinstance(failed_cache, dict):
        failed_cache = {}
    failed_ids = set(failed_cache.keys())
    if failed_ids:
        print(f"\n  Skipping {len(failed_ids)} previously failed download(s)")

    # --- Downloads: ensure qualifying papers have PDFs ---
    print(f"\n>> Downloads: Qualifying papers ({args.step2_dir} -> {args.pdf_dir})")
    print("-" * 40)
    missing_pdfs = audit_downloads(args.step2_dir, args.pdf_dir, failed_ids)
    if not missing_pdfs:
        print(f"  OK: All qualifying papers have PDFs.")
    else:
        print(f"  WARNING: {len(missing_pdfs)} qualifying paper(s) missing PDFs:")
        for stem in missing_pdfs[:20]:
            print(f"     - {stem}")
        if len(missing_pdfs) > 20:
            print(f"     ... and {len(missing_pdfs) - 20} more")
        total_missing += len(missing_pdfs)

        if apply:
            os.makedirs(args.pdf_dir, exist_ok=True)
            downloaded = 0
            failed = 0
            for i, stem in enumerate(missing_pdfs):
                result = download_pdf(stem, args.pdf_dir)
                if result == 'ok':
                    downloaded += 1
                elif result == 'permanent_fail':
                    failed_cache[stem] = time.strftime('%Y-%m-%d')
                    failed += 1
                else:
                    failed += 1
                if i < len(missing_pdfs) - 1:
                    time.sleep(DELAY_BETWEEN_DOWNLOADS)
            print(f"  Downloaded: {downloaded}, Failed: {failed}")
            total_downloaded += downloaded

    # --- Cache downloads: ensure assessed-positive papers have PDFs ---
    print(f"\n>> Cache Downloads: Assessment cache ({args.cache} -> {args.pdf_dir})")
    print("-" * 40)
    missing_cached = audit_cache_downloads(args.cache, args.pdf_dir, set(failed_cache.keys()))
    if not missing_cached:
        print(f"  OK: All cache-positive papers have PDFs.")
    else:
        print(f"  WARNING: {len(missing_cached)} cache-positive paper(s) missing PDFs:")
        for stem in missing_cached[:20]:
            print(f"     - {stem}")
        if len(missing_cached) > 20:
            print(f"     ... and {len(missing_cached) - 20} more")
        total_missing += len(missing_cached)

        if apply:
            os.makedirs(args.pdf_dir, exist_ok=True)
            downloaded = 0
            failed = 0
            for i, stem in enumerate(missing_cached):
                result = download_pdf(stem, args.pdf_dir)
                if result == 'ok':
                    downloaded += 1
                elif result == 'permanent_fail':
                    failed_cache[stem] = time.strftime('%Y-%m-%d')
                    failed += 1
                else:
                    failed += 1
                if i < len(missing_cached) - 1:
                    time.sleep(DELAY_BETWEEN_DOWNLOADS)
            print(f"  Downloaded: {downloaded}, Failed: {failed}")
            total_downloaded += downloaded

    # Save failed-downloads cache if it changed
    if apply and failed_cache:
        os.makedirs(os.path.dirname(failed_cache_path) or '.', exist_ok=True)
        with open(failed_cache_path, 'w', encoding='utf-8') as f:
            json.dump(failed_cache, f, indent=2)
        print(f"\n  Saved {len(failed_cache)} entries to {failed_cache_path}")

    # --- Step 2: paper metadata ---
    # Note: we never delete step 2 metadata. PDFs may be intentionally removed
    # but we keep the metadata. We only report unprocessed PDFs (missing metadata).
    print(f"\n>> Step 2: Paper Metadata ({args.step2_dir})")
    print("-" * 40)
    orphaned2, missing2 = audit_step2(args.pdf_dir, args.step2_dir)
    
    step2_json_count = len(get_stems(args.step2_dir))
    pdf_count = len([f for f in glob.glob(os.path.join(args.pdf_dir, "*.pdf"))]) if os.path.isdir(args.pdf_dir) else 0
    print(f"  {step2_json_count} metadata files, {pdf_count} PDFs")
    if orphaned2:
        print(f"  INFO: {len(orphaned2)} metadata file(s) without matching PDF (kept)")
    print_section("Unprocessed PDFs (no metadata JSON)", missing2, "unprocessed", args.step2_dir)
    total_missing += len(missing2)
    
    if missing2 and apply:
        run_pipeline_step(
            ["uv", "run", "python", "scripts/2_extract_paper_metadata.py"],
            "Step 2: Extract paper metadata"
        )
    
    # --- Step 3: bias targets ---
    print(f"\n>> Step 3: Bias Targets ({args.step3_dir})")
    print("-" * 40)
    invalid3, missing3 = audit_step3(args.step2_dir, args.step3_dir)
    
    print_section("Invalid JSON (criteria no longer met)", invalid3, "invalid", args.step3_dir)
    print_section("Missing JSON (eligible but not processed)", missing3, "missing", args.step3_dir)
    total_invalid += len(invalid3)
    total_missing += len(missing3)
    
    if invalid3 and apply:
        delete_files(invalid3, args.step3_dir)
        total_deleted += len(invalid3)
    
    if missing3 and apply:
        run_pipeline_step(
            ["uv", "run", "python", "scripts/3_extract_bias_targets.py"],
            "Step 3: Extract bias targets"
        )
    
    # --- Step 4: religious bias analysis ---
    print(f"\n>> Step 4: Religious Bias Analysis ({args.step4_dir})")
    print("-" * 40)
    invalid4, missing4 = audit_step4(args.step2_dir, args.step3_dir, args.step4_dir)
    
    print_section("Invalid JSON (criteria no longer met)", invalid4, "invalid", args.step4_dir)
    print_section("Missing JSON (eligible but not processed)", missing4, "missing", args.step4_dir)
    total_invalid += len(invalid4)
    total_missing += len(missing4)
    
    if invalid4 and apply:
        delete_files(invalid4, args.step4_dir)
        total_deleted += len(invalid4)
    
    if missing4 and apply:
        run_pipeline_step(
            ["uv", "run", "python", "scripts/4_extract_paper_details.py"],
            "Step 4: Extract paper details (religious bias analysis)"
        )
    
    # --- Summary ---
    print(f"\n{'=' * 60}")
    print(f"Summary")
    print(f"{'=' * 60}")
    print(f"  Invalid files found: {total_invalid}")
    print(f"  Missing files found: {total_missing}")
    if apply:
        print(f"  Files deleted:       {total_deleted}")
        print(f"  PDFs downloaded:     {total_downloaded}")
    if total_invalid == 0 and total_missing == 0:
        print(f"\n  OK: Pipeline data is clean!")
    elif not apply:
        print(f"\n  To apply these changes, re-run with: --apply")
    print()


if __name__ == "__main__":
    main()

