#!/usr/bin/env python3
"""
Identify Religious Bias in LLM papers picked up by the wider net (non-CS categories).

Cross-references processed papers in json/4_religious_bias_analysis/ against the
arXiv snapshot to find papers that include non-CS arXiv categories (e.g. stat.ML,
physics.soc-ph, econ.TH). Generates a report in the same format as Summaries.md.
"""

import csv
import json
import os
import sys
from collections import Counter
from pathlib import Path

# Add scripts dir to path for shared imports
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from shared import get_arxiv_url, unsanitize_arxiv_id, load_csv_metadata


STAGE4_DIR = PROJECT_DIR / "json" / "4_religious_bias_analysis"
SNAPSHOT_FILE = PROJECT_DIR / "utility_files" / "arxiv-metadata-oai-snapshot.json"
CSV_FILE = PROJECT_DIR / "utility_files" / "llm_bias_papers.csv"
OUTPUT_FILE = PROJECT_DIR / "reports" / "Picked Up with Wider Net.md"


def get_stage4_paper_ids() -> set[str]:
    """Get all arXiv IDs from stage 4 JSON filenames."""
    return {f.stem for f in STAGE4_DIR.glob("*.json")}


def load_snapshot_categories(paper_ids: set[str]) -> dict[str, str]:
    """Stream the snapshot and extract categories for the given paper IDs.
    
    Returns {arxiv_id: categories_string}.
    """
    categories = {}
    if not SNAPSHOT_FILE.exists():
        print(f"Warning: Snapshot file not found: {SNAPSHOT_FILE}")
        return categories

    print(f"Streaming snapshot to find categories for {len(paper_ids)} papers...")
    found = 0
    for line_num, line in enumerate(open(SNAPSHOT_FILE, "r", encoding="utf-8"), 1):
        line = line.strip()
        if not line:
            continue
        try:
            paper = json.loads(line)
        except json.JSONDecodeError:
            continue

        arxiv_id = paper.get("id", "")
        if arxiv_id in paper_ids:
            categories[arxiv_id] = paper.get("categories", "")
            found += 1
            if found == len(paper_ids):
                break

        if line_num % 500_000 == 0:
            print(f"  Scanned {line_num:,} lines ({found}/{len(paper_ids)} found)...")

    print(f"  Found categories for {found}/{len(paper_ids)} papers")
    return categories


def has_non_cs_category(categories_str: str) -> bool:
    """Return True if any of the paper's categories does NOT start with 'cs.'."""
    if not categories_str:
        return False
    cats = categories_str.split()
    return any(not c.startswith("cs.") for c in cats)


def get_non_cs_categories(categories_str: str) -> list[str]:
    """Return the non-CS categories from a categories string."""
    if not categories_str:
        return []
    return [c for c in categories_str.split() if not c.startswith("cs.")]


def load_stage4_data(arxiv_id: str) -> dict:
    """Load stage 4 JSON data for a paper."""
    json_path = STAGE4_DIR / f"{arxiv_id}.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def check_mormon_mention(paper_data: dict) -> bool:
    """Check if the paper mentions Mormon/Latter-day Saints."""
    text = json.dumps(paper_data).lower()
    return any(term in text for term in ["mormon", "latter-day", "lds"])


def main():
    # 1. Get all processed paper IDs
    paper_ids = get_stage4_paper_ids()
    print(f"Total papers in stage 4: {len(paper_ids)}")

    # 2. Load categories from snapshot
    categories = load_snapshot_categories(paper_ids)

    # 3. Categorize papers
    cs_only_ids = set()
    wider_net_ids = set()  # Papers with non-CS categories
    exclusively_non_cs_ids = set()  # Papers with NO CS categories

    for pid in paper_ids:
        if pid not in categories:
            continue
        cats = categories[pid].split()
        has_cs = any(c.startswith("cs.") for c in cats)
        has_non_cs = any(not c.startswith("cs.") for c in cats)

        if has_non_cs and not has_cs:
            exclusively_non_cs_ids.add(pid)
            wider_net_ids.add(pid)
        elif has_non_cs and has_cs:
            wider_net_ids.add(pid)
        else:
            cs_only_ids.add(pid)

    not_in_snapshot = paper_ids - set(categories.keys())
    
    print(f"\n  CS-only papers: {len(cs_only_ids)}")
    print(f"  Cross-listed (CS + other categories): {len(wider_net_ids - exclusively_non_cs_ids)}")
    print(f"  Exclusively non-CS papers: {len(exclusively_non_cs_ids)}")
    if not_in_snapshot:
        print(f"  Not found in snapshot: {len(not_in_snapshot)}")

    # 4. Load CSV metadata for titles and dates
    csv_meta = {}
    if CSV_FILE.exists():
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_meta[row["paper_id"]] = {
                    "title": row.get("title", "Unknown Title"),
                    "date": row.get("latest_date", "Unknown Date"),
                }
    
    # 5. Generate report
    sorted_ids = sorted(wider_net_ids, reverse=True)
    
    lines = ["# Picked Up with Wider Net\n"]
    lines.append("Papers about religious bias in LLMs that include non-CS arXiv categories, indicating")
    lines.append("they were cross-listed or primarily categorized outside Computer Science.\n")
    lines.append(f"**Total wider-net papers: {len(sorted_ids)}** out of {len(paper_ids)} total papers "
                 f"({len(exclusively_non_cs_ids)} exclusively non-CS, "
                 f"{len(wider_net_ids - exclusively_non_cs_ids)} cross-listed with CS).\n")
    lines.append("")

    # Non-CS category breakdown
    non_cs_cats = Counter()
    for pid in sorted_ids:
        for cat in get_non_cs_categories(categories[pid]):
            non_cs_cats[cat] += 1
    
    if non_cs_cats:
        lines.append("## Non-CS Category Breakdown\n")
        lines.append("| Category | Count | Description |")
        lines.append("|---|---|---|")
        cat_descriptions = {
            "stat.ML": "Machine Learning (Statistics)",
            "stat.ME": "Methodology (Statistics)",
            "stat.AP": "Applications (Statistics)",
            "physics.soc-ph": "Physics and Society",
            "econ.TH": "Theoretical Economics",
            "econ.GN": "General Economics",
            "eess.AS": "Audio and Speech Processing",
            "math.IT": "Information Theory",
            "cs.IT": "Information Theory (CS)",
            "q-bio.NC": "Neurons and Cognition",
            "q-fin.EC": "Economics (Quantitative Finance)",
        }
        for cat, count in non_cs_cats.most_common():
            desc = cat_descriptions.get(cat, "")
            lines.append(f"| `{cat}` | {count} | {desc} |")
        lines.append("")
        lines.append("")

    # Paper entries
    for pid in sorted_ids:
        meta = csv_meta.get(pid, {})
        title = meta.get("title", "Unknown Title")
        date = meta.get("date", "Unknown Date")
        arxiv_url = get_arxiv_url(pid)
        all_cats = categories[pid]
        non_cs = get_non_cs_categories(categories[pid])

        # Load stage 4 data for summary
        s4 = load_stage4_data(pid)
        measurement_desc = s4.get("measurement_description", "") or s4.get("benchmark_measurement", "")
        findings = s4.get("findings", "")
        combined = f"{measurement_desc} {findings}".strip()

        mormon_tag = " #Mormon" if check_mormon_mention(s4) else ""

        lines.append(f"## {title}{mormon_tag}\n")
        lines.append(f"[{arxiv_url}]({arxiv_url})\n")
        lines.append(f"**Date:** {date}\n")
        lines.append(f"**Categories:** {all_cats}\n")
        lines.append(f"**Non-CS Categories:** {', '.join(non_cs)}\n")
        lines.append(f"{combined}\n")
        lines.append("")

    # Write output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nReport written to {OUTPUT_FILE}")
    print(f"  {len(sorted_ids)} wider-net papers documented")


if __name__ == "__main__":
    main()
