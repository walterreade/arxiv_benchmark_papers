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


def categorize_papers(paper_ids: set[str], categories: dict[str, str]) -> tuple[set, set, set, set]:
    """Categorize papers into cs-only, wider-net, exclusively-non-cs, not-in-snapshot."""
    cs_only = set()
    wider_net = set()
    exclusively_non_cs = set()

    for pid in paper_ids:
        if pid not in categories:
            continue
        cats = categories[pid].split()
        has_cs = any(c.startswith("cs.") for c in cats)
        has_non_cs = any(not c.startswith("cs.") for c in cats)

        if has_non_cs and not has_cs:
            exclusively_non_cs.add(pid)
            wider_net.add(pid)
        elif has_non_cs and has_cs:
            wider_net.add(pid)
        else:
            cs_only.add(pid)

    not_in_snapshot = paper_ids - set(categories.keys())
    return cs_only, wider_net, exclusively_non_cs, not_in_snapshot


def main():
    # 1. Get all processed paper IDs (religious bias subset)
    religious_paper_ids = get_stage4_paper_ids()
    print(f"Total religious bias papers in stage 4: {len(religious_paper_ids)}")

    # 2. Load ALL bias-in-LLM paper IDs from the CSV
    all_bias_ids = set()
    csv_meta = {}
    if CSV_FILE.exists():
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pid = row["paper_id"]
                all_bias_ids.add(pid)
                csv_meta[pid] = {
                    "title": row.get("title", "Unknown Title"),
                    "date": row.get("latest_date", "Unknown Date"),
                }
    print(f"Total bias-in-LLM papers in CSV: {len(all_bias_ids)}")

    # 3. Load categories from snapshot for ALL papers (single pass)
    all_needed_ids = all_bias_ids | religious_paper_ids
    categories = load_snapshot_categories(all_needed_ids)

    # 4. Categorize both sets
    r_cs_only, r_wider, r_excl_non_cs, r_not_found = categorize_papers(religious_paper_ids, categories)
    a_cs_only, a_wider, a_excl_non_cs, a_not_found = categorize_papers(all_bias_ids, categories)

    print(f"\n--- Religious Bias Papers ---")
    print(f"  CS-only: {len(r_cs_only)}")
    print(f"  Cross-listed (CS + other): {len(r_wider - r_excl_non_cs)}")
    print(f"  Exclusively non-CS: {len(r_excl_non_cs)}")
    if r_not_found:
        print(f"  Not in snapshot: {len(r_not_found)}")

    print(f"\n--- All Bias-in-LLM Papers ---")
    print(f"  CS-only: {len(a_cs_only)}")
    print(f"  Cross-listed (CS + other): {len(a_wider - a_excl_non_cs)}")
    print(f"  Exclusively non-CS: {len(a_excl_non_cs)}")
    if a_not_found:
        print(f"  Not in snapshot: {len(a_not_found)}")

    # 5. Generate report
    sorted_religious_ids = sorted(r_wider, reverse=True)
    
    lines = ["# Picked Up with Wider Net\n"]
    lines.append("Papers that include non-CS arXiv categories, indicating they were cross-listed or")
    lines.append("primarily categorized outside Computer Science.\n")

    # --- Broader bias-in-LLM summary statistics ---
    lines.append("## All Bias-in-LLM Papers (Summary Statistics)\n")
    lines.append(f"Out of **{len(all_bias_ids):,}** total bias-in-LLM papers in the pipeline:\n")
    lines.append(f"| Category | Count | % |")
    lines.append(f"|---|---|---|")
    lines.append(f"| CS-only | {len(a_cs_only):,} | {len(a_cs_only)/len(all_bias_ids)*100:.1f}% |")
    lines.append(f"| Cross-listed (CS + other) | {len(a_wider - a_excl_non_cs):,} | {(len(a_wider - a_excl_non_cs))/len(all_bias_ids)*100:.1f}% |")
    lines.append(f"| Exclusively non-CS | {len(a_excl_non_cs):,} | {len(a_excl_non_cs)/len(all_bias_ids)*100:.1f}% |")
    lines.append(f"| Not in snapshot | {len(a_not_found):,} | {len(a_not_found)/len(all_bias_ids)*100:.1f}% |")
    lines.append("")

    # Non-CS category breakdown for ALL bias papers
    all_non_cs_cats = Counter()
    for pid in a_wider:
        for cat in get_non_cs_categories(categories[pid]):
            all_non_cs_cats[cat] += 1
    
    if all_non_cs_cats:
        lines.append("### Non-CS Categories Across All Bias Papers\n")
        lines.append("| Category | Count | Description |")
        lines.append("|---|---|---|")
        cat_descriptions = {
            "stat.ML": "Machine Learning (Statistics)",
            "stat.ME": "Methodology (Statistics)",
            "stat.AP": "Applications (Statistics)",
            "stat.TH": "Statistics Theory",
            "stat.CO": "Computation (Statistics)",
            "physics.soc-ph": "Physics and Society",
            "econ.TH": "Theoretical Economics",
            "econ.GN": "General Economics",
            "eess.AS": "Audio and Speech Processing",
            "eess.SP": "Signal Processing",
            "eess.IV": "Image and Video Processing",
            "math.IT": "Information Theory",
            "math.ST": "Statistics Theory (Math)",
            "math.OC": "Optimization and Control",
            "q-bio.NC": "Neurons and Cognition",
            "q-bio.QM": "Quantitative Methods (Q-Bio)",
            "q-fin.EC": "Economics (Quantitative Finance)",
            "I.2.7": "Natural Language Processing (Legacy)",
        }
        for cat, count in all_non_cs_cats.most_common():
            desc = cat_descriptions.get(cat, "")
            lines.append(f"| `{cat}` | {count} | {desc} |")
        lines.append("")
    lines.append("")

    # --- Religious bias papers section ---
    lines.append("## Religious Bias Papers with Non-CS Categories\n")
    lines.append(f"**Total: {len(sorted_religious_ids)}** out of {len(religious_paper_ids)} religious bias papers "
                 f"({len(r_excl_non_cs)} exclusively non-CS, "
                 f"{len(r_wider - r_excl_non_cs)} cross-listed with CS).\n")
    lines.append("")

    # Non-CS category breakdown for religious bias papers
    religious_non_cs_cats = Counter()
    for pid in sorted_religious_ids:
        for cat in get_non_cs_categories(categories[pid]):
            religious_non_cs_cats[cat] += 1
    
    if religious_non_cs_cats:
        lines.append("### Category Breakdown\n")
        lines.append("| Category | Count | Description |")
        lines.append("|---|---|---|")
        for cat, count in religious_non_cs_cats.most_common():
            desc = cat_descriptions.get(cat, "")
            lines.append(f"| `{cat}` | {count} | {desc} |")
        lines.append("")
        lines.append("")

    # Paper entries (religious bias only)
    for pid in sorted_religious_ids:
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
    print(f"  {len(sorted_religious_ids)} wider-net papers documented")


if __name__ == "__main__":
    main()
