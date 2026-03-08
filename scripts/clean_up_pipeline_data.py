#!/usr/bin/env python3
"""
Pipeline Data Cleanup

Validates JSON data across pipeline stages and identifies:
- JSON files that no longer meet pipeline criteria (can be removed)
- Missing JSON files that should exist based on upstream data (can be generated)

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
import sys
from pathlib import Path

# Religious bias keywords (mirrored from 4_extract_paper_details.py)
_RELIGIOUS_KEYWORDS = [
    'relig', 'faith', 'spiritual', 'theolog',
    'islam', 'muslim', 'christian', 'jewish', 'hindu',
    'buddhis', 'sikh', 'mormon', 'latter-day',
    'antisemit',
]


def _has_religious_bias(second_pass_data: dict) -> bool:
    """Check whether any bias_targets or primary_bias_target mention religious bias."""
    targets = second_pass_data.get('bias_targets', [])
    texts = [t.get('target', '') for t in targets]
    texts.append(second_pass_data.get('primary_bias_target', ''))

    for text in texts:
        lowered = text.lower()
        if 'faithfulness' in lowered:
            continue
        if any(kw in lowered for kw in _RELIGIOUS_KEYWORDS):
            return True
    return False


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
            print(f"\n  ❌ {description} exited with code {result.returncode}.")
            return False
    except KeyboardInterrupt:
        print(f"\n  WARNING: {description} interrupted by user.")
        return False
    except Exception as e:
        print(f"\n  ❌ Failed to run {description}: {e}")
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
    parser.add_argument("--apply", action="store_true", help="Actually delete invalid files and regenerate missing ones")
    
    args = parser.parse_args()
    apply = args.apply
    
    print("=" * 60)
    print("Pipeline Data Cleanup" + ("" if apply else "  [DRY RUN]"))
    print("=" * 60)
    
    total_invalid = 0
    total_missing = 0
    total_deleted = 0
    
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
    if total_invalid == 0 and total_missing == 0:
        print(f"\n  OK: Pipeline data is clean!")
    elif not apply:
        print(f"\n  To apply these changes, re-run with: --apply")
    print()


if __name__ == "__main__":
    main()

