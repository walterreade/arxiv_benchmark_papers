#!/usr/bin/env python3
"""
Analyze bias targets extracted from papers.

This script:
1. Normalizes bias target categories (handles case, synonyms)
2. Creates a table of top 25 most frequent bias targets
3. Creates a table of top 25 singleton targets (only target in list)
4. Provides statistics about list lengths, papers analyzed, etc.
"""

import json
from pathlib import Path
from collections import Counter
import re


# Directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
JSON_DIR = PROJECT_DIR / "json" / "1st_pass_json"


# Normalization mappings - maps variations to canonical form
NORMALIZATION_MAP = {
    # Gender
    "gender bias": "Gender bias",
    "gender": "Gender bias",
    "sex bias": "Gender bias",
    "sexism": "Gender bias",
    
    # Racial
    "racial bias": "Racial bias",
    "race bias": "Racial bias",
    "racism": "Racial bias",
    "ethnic bias": "Racial bias",
    "ethnicity bias": "Racial bias",
    
    # Religious
    "religious bias": "Religious bias",
    "religion bias": "Religious bias",
    
    # Age
    "age bias": "Age bias",
    "ageism": "Age bias",
    
    # Political
    "political bias": "Political bias",
    "politics bias": "Political bias",
    
    # Nationality
    "nationality bias": "Nationality bias",
    "national bias": "Nationality bias",
    "country bias": "Nationality bias",
    
    # Cultural
    "cultural bias": "Cultural bias",
    "culture bias": "Cultural bias",
    
    # Language/Linguistic
    "language bias": "Language bias",
    "linguistic bias": "Language bias",
    
    # Position/Positional
    "position bias": "Position bias",
    "positional bias": "Position bias",
    
    # Sexual orientation
    "sexual orientation bias": "Sexual orientation bias",
    "lgbtq+ bias": "Sexual orientation bias",
    "lgbtq bias": "Sexual orientation bias",
    "homophobia": "Sexual orientation bias",
    
    # Socioeconomic
    "socioeconomic bias": "Socioeconomic bias",
    "socio-economic bias": "Socioeconomic bias",
    "economic bias": "Socioeconomic bias",
    "class bias": "Socioeconomic bias",
    
    # Disability
    "disability bias": "Disability bias",
    "ableism": "Disability bias",
    
    # Hate speech
    "hate speech detection": "Hate speech",
    "hate speech detection (general toxic or hateful content)": "Hate speech",
    "toxic content": "Hate speech",
    "toxicity": "Hate speech",
    
    # Stereotyping
    "stereotyping": "Stereotyping",
    "stereotype bias": "Stereotyping",
    "stereotypes": "Stereotyping",
    
    # Fairness
    "fairness in outcomes": "Fairness",
    "fairness": "Fairness",
    "outcome fairness": "Fairness",
    
    # Length bias
    "length bias": "Length bias",
    "verbosity bias": "Length bias",
    
    # Self-preference
    "self-preference bias": "Self-preference bias",
    "self preference bias": "Self-preference bias",
}


def normalize_target(target: str) -> str:
    """Normalize a bias target to canonical form."""
    # First try exact match (case-insensitive)
    lower = target.lower().strip()
    if lower in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[lower]
    
    # If not in map, title case and return
    return target.strip().title() if target.strip() else target


def load_bias_data():
    """Load all bias target data from JSON files."""
    papers_data = []
    
    for json_file in JSON_DIR.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            if 'bias_targets' in data:
                raw_targets = data['bias_targets']
                normalized = [normalize_target(t) for t in raw_targets]
                papers_data.append({
                    'arxiv_id': json_file.stem,
                    'raw_targets': raw_targets,
                    'normalized_targets': normalized,
                    'count': len(normalized)
                })
        except (json.JSONDecodeError, IOError):
            continue
    
    return papers_data


def print_table(title: str, data: list, headers: tuple = ("Rank", "Count", "Category")):
    """Print a formatted table."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}")
    
    # Calculate column widths
    col1_width = max(len(headers[0]), 4)
    col2_width = max(len(headers[1]), 5)
    col3_width = max(len(headers[2]), max(len(str(row[1])) for row in data) if data else 10)
    
    # Header
    print(f" {headers[0]:<{col1_width}} | {headers[1]:<{col2_width}} | {headers[2]}")
    print(f" {'-' * col1_width}-+-{'-' * col2_width}-+-{'-' * 40}")
    
    # Data rows
    for i, (category, count) in enumerate(data, 1):
        bar_len = int((count / data[0][1]) * 20) if data else 0
        bar = "█" * bar_len
        print(f" {i:<{col1_width}} | {count:<{col2_width}} | {category} {bar}")
    
    print()


def main():
    print("\n" + "=" * 60)
    print(" BIAS TARGET ANALYSIS")
    print("=" * 60)
    
    # Load data
    papers_data = load_bias_data()
    
    if not papers_data:
        print("No papers with bias_targets found.")
        return
    
    # Collect all normalized targets
    all_targets = []
    singleton_targets = []
    list_lengths = []
    
    for paper in papers_data:
        targets = paper['normalized_targets']
        all_targets.extend(targets)
        list_lengths.append(paper['count'])
        
        if len(targets) == 1:
            singleton_targets.append(targets[0])
    
    # Count frequencies
    all_counter = Counter(all_targets)
    singleton_counter = Counter(singleton_targets)
    
    # Statistics
    print("\n" + "-" * 60)
    print(" STATISTICS")
    print("-" * 60)
    print(f" Total papers analyzed:           {len(papers_data)}")
    print(f" Total bias target mentions:      {len(all_targets)}")
    print(f" Unique categories (normalized):  {len(all_counter)}")
    print(f" Papers with singleton target:    {len(singleton_targets)}")
    print()
    print(" List Length Distribution:")
    print(f"   - Min:     {min(list_lengths)}")
    print(f"   - Max:     {max(list_lengths)}")
    print(f"   - Mean:    {sum(list_lengths) / len(list_lengths):.2f}")
    print(f"   - Median:  {sorted(list_lengths)[len(list_lengths) // 2]}")
    
    # List length histogram
    length_counter = Counter(list_lengths)
    print()
    print(" List Length Frequency:")
    for length in sorted(length_counter.keys()):
        count = length_counter[length]
        bar = "█" * min(count // 2, 40)
        print(f"   {length:2d} targets: {count:4d} papers {bar}")
    
    # Top 25 overall
    top_25_all = all_counter.most_common(25)
    print_table("TOP 25 BIAS TARGET CATEGORIES (Overall)", top_25_all)
    
    # Top 25 singletons
    top_25_singleton = singleton_counter.most_common(25)
    print_table("TOP 25 SINGLETON BIAS TARGETS (Only target in list)", top_25_singleton)
    
    # Religious bias specific stats
    religious_count = all_counter.get("Religious bias", 0)
    religious_singleton = singleton_counter.get("Religious bias", 0)
    print("-" * 60)
    print(" RELIGIOUS BIAS FOCUS")
    print("-" * 60)
    print(f" Total mentions:      {religious_count}")
    print(f" As singleton:        {religious_singleton}")
    print(f" Rank (overall):      {[i for i, (cat, _) in enumerate(all_counter.most_common(), 1) if cat == 'Religious bias'][0] if religious_count else 'N/A'}")
    print()


if __name__ == "__main__":
    main()
