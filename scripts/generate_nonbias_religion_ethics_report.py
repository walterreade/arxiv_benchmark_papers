#!/usr/bin/env python3
"""
Generate a report of LLM-related papers that are NOT bias-related but are tagged
with religion, ethics, moral_reasoning, or bias_and_fairness in stage 2 metadata.

These are papers about LLMs that touch on religion/ethics topics without measuring bias.
"""

import csv
import json
import glob
import os
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from shared import get_arxiv_url, unsanitize_arxiv_id

STAGE2_DIR = PROJECT_DIR / "json" / "2_paper_metadata"
CSV_FILE = PROJECT_DIR / "utility_files" / "llm_bias_papers.csv"
OUTPUT_FILE = PROJECT_DIR / "reports" / "Non-Bias Religion and Ethics Papers.md"

TAGS = ["religion", "ethics", "moral_reasoning", "bias_and_fairness"]


def load_csv_metadata() -> dict[str, dict]:
    """Load paper metadata from CSV."""
    meta = {}
    if CSV_FILE.exists():
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                meta[row["paper_id"]] = {
                    "title": row.get("title", "Unknown Title"),
                    "date": row.get("latest_date", "Unknown Date"),
                }
    return meta


def main():
    # Scan all stage 2 JSONs
    papers = []
    tag_counts = Counter()
    combo_counts = Counter()

    for fp in glob.iglob(str(STAGE2_DIR / "*.json")):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                d = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue

        if not d.get("is_llm_related") or d.get("is_bias_related"):
            continue

        # Check for any relevant tag
        active_tags = [t for t in TAGS if d.get(t)]
        if not active_tags:
            continue

        pid = Path(fp).stem
        for t in active_tags:
            tag_counts[t] += 1
        combo_counts[tuple(sorted(active_tags))] += 1

        papers.append({
            "id": pid,
            "title": d.get("title", "Unknown Title"),
            "date": d.get("date", ""),
            "reasoning": d.get("reasoning", ""),
            "tags": active_tags,
        })

    print(f"Found {len(papers)} non-bias religion/ethics papers")
    for t, c in tag_counts.most_common():
        print(f"  {t}: {c}")

    # Load CSV metadata for better dates
    csv_meta = load_csv_metadata()

    # Sort by date (newest first), then by ID
    def sort_key(p):
        date = csv_meta.get(p["id"], {}).get("date", p["date"]) or ""
        return date

    papers.sort(key=sort_key, reverse=True)

    # Generate report
    lines = ["# Non-Bias Religion and Ethics Papers\n"]
    lines.append("LLM-related papers that are **not** classified as bias-related, but are tagged with")
    lines.append("religion, ethics, moral reasoning, or bias & fairness topics.\n")
    lines.append(f"**Total papers: {len(papers)}**\n")
    lines.append("")

    # Tag breakdown
    lines.append("## Tag Distribution\n")
    lines.append("| Tag | Count |")
    lines.append("|---|---|")
    for t, c in tag_counts.most_common():
        lines.append(f"| {t} | {c} |")
    lines.append("")

    # Tag combination breakdown
    lines.append("### Tag Combinations\n")
    lines.append("| Combination | Count |")
    lines.append("|---|---|")
    for combo, c in combo_counts.most_common(15):
        combo_str = " + ".join(combo)
        lines.append(f"| {combo_str} | {c} |")
    lines.append("")
    lines.append("")

    # Paper entries
    for p in papers:
        pid = p["id"]
        meta = csv_meta.get(pid, {})
        title = meta.get("title", p["title"]) or p["title"] or "Unknown Title"
        date = meta.get("date", p["date"]) or p["date"] or "Unknown Date"
        arxiv_url = get_arxiv_url(pid)
        tags_str = ", ".join(p["tags"])
        reasoning = p["reasoning"]

        lines.append(f"## {title}\n")
        lines.append(f"[{arxiv_url}]({arxiv_url})\n")
        lines.append(f"**Date:** {date}\n")
        lines.append(f"**Tags:** {tags_str}\n")
        if reasoning:
            lines.append(f"{reasoning}\n")
        lines.append("")

    # Write output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nReport written to {OUTPUT_FILE}")
    print(f"  {len(papers)} papers documented")


if __name__ == "__main__":
    main()
