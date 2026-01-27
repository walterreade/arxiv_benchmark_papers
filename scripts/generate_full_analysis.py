#!/usr/bin/env python3
"""
Create summary statistics from 2nd pass JSON analysis files.
Generates benchmark_analysis.md with tables summarizing the analysis results.
"""

import os
import json
import glob
import argparse
import re
import csv
import unicodedata
import shutil
from datetime import datetime
from collections import Counter
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# Mapping of variations to canonical names
# Denominations are kept separate; only combine variants of the same group
RELIGIOUS_GROUP_NORMALIZATION = {
    # Christianity (general - only if no denomination specified)
    'christian': 'Christianity',
    'christians': 'Christianity',
    'christianity': 'Christianity',
    
    # Catholic denomination
    'catholic': 'Catholic',
    'catholicism': 'Catholic',
    'roman catholic': 'Catholic',
    
    # Protestant denomination
    'protestant': 'Protestant',
    'protestantism': 'Protestant',
    
    # Orthodox denomination
    'orthodox': 'Orthodox',
    'eastern orthodox': 'Orthodox',
    'greek orthodox': 'Orthodox',
    'russian orthodox': 'Orthodox',
    
    # Other Christian denominations
    'baptist': 'Baptist',
    'methodist': 'Methodist',
    'evangelical': 'Evangelical',
    'evangelicalism': 'Evangelical',
    'mormon': 'Mormon',
    'mormonism': 'Mormon',
    'lutheran': 'Lutheran',
    'lutheranism': 'Lutheran',
    'pentecostal': 'Pentecostal',
    'pentecostalism': 'Pentecostal',
    'anglican': 'Anglican',
    'anglicanism': 'Anglican',
    'presbyterian': 'Presbyterian',
    
    # Islam (general)
    'muslim': 'Islam',
    'muslims': 'Islam',
    'islam': 'Islam',
    
    # Islamic denominations
    'sunni': 'Sunni',
    'sunni islam': 'Sunni',
    'shia': 'Shia',
    'shia islam': 'Shia',
    'shiite': 'Shia',
    'sufi': 'Sufi',
    'sufism': 'Sufi',
    
    # Judaism variants
    'jewish': 'Judaism',
    'judaism': 'Judaism',
    'jews': 'Judaism',
    
    # Buddhism variants
    'buddhist': 'Buddhism',
    'buddhism': 'Buddhism',
    'buddhists': 'Buddhism',
    
    # Hinduism variants
    'hindu': 'Hinduism',
    'hindus': 'Hinduism',
    'hinduism': 'Hinduism',
    
    # Sikhism variants
    'sikh': 'Sikhism',
    'sikhs': 'Sikhism',
    'sikhism': 'Sikhism',
    
    # Atheism variants
    'atheist': 'Atheism',
    'atheists': 'Atheism',
    'atheism': 'Atheism',
    
    # Agnosticism variants
    'agnostic': 'Agnosticism',
    'agnostics': 'Agnosticism',
    'agnosticism': 'Agnosticism',
    
    # Confucianism variants
    'confucian': 'Confucianism',
    'confucianism': 'Confucianism',
    
    # Taoism/Daoism variants
    'taoism': 'Taoism',
    'daoism': 'Taoism',
    'taoist': 'Taoism',
    'daoist': 'Taoism',
    
    # Shinto variants
    'shinto': 'Shinto',
    'shintoism': 'Shinto',
    
    # Jainism variants
    'jain': 'Jainism',
    'jainism': 'Jainism',
    
    # Zoroastrianism variants
    'zoroastrian': 'Zoroastrianism',
    'zoroastrianism': 'Zoroastrianism',
    
    # General/unspecified religion
    'religion': 'Religion (general)',
    'religion (general)': 'Religion (general)',
    'religion (unspecified)': 'Religion (general)',
    'religion (as a general category)': 'Religion (general)',
    'religion (general category)': 'Religion (general)',
    'religious studies': 'Religion (general)',
    'world religions': 'Religion (general)',
    'world religion': 'Religion (general)',
    'other religions': 'Religion (general)',
    
    # Non-religious
    'no religion': 'Non-religious',
    'secular': 'Non-religious',
    'not specified': 'Not specified',
}


def normalize_religious_group(group: str) -> str:
    """Normalize a religious group name to its canonical form."""
    normalized = group.strip().lower()
    return RELIGIOUS_GROUP_NORMALIZATION.get(normalized, group)


def load_json_files(json_dir: str) -> list[dict]:
    """Load all JSON files from the specified directory."""
    json_files = glob.glob(os.path.join(json_dir, "*.json"))
    data = []
    for jf in json_files:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                paper_data = json.load(f)
                # Store the filename (without extension) for reference
                paper_data['_filename'] = Path(jf).stem + '.pdf'
                data.append(paper_data)
        except Exception as e:
            print(f"Warning: Failed to load {jf}: {e}")
    return data


def load_csv_metadata(csv_path: str) -> dict:
    """Load metadata from 1st pass CSV file, keyed by filename."""
    metadata = {}
    if not os.path.exists(csv_path):
        print(f"Warning: CSV file {csv_path} not found.")
        return metadata
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row.get('filename', '')
            if filename:
                metadata[filename] = {
                    'title': row.get('title', ''),
                    'date': row.get('date', ''),
                }
    return metadata


def get_arxiv_url(filename: str) -> str:
    """Convert filename to arxiv PDF URL."""
    # Filename format: 2601.15267.pdf -> arxiv ID: 2601.15267
    arxiv_id = filename.replace('.pdf', '')
    return f"https://arxiv.org/pdf/{arxiv_id}"


def check_mormon_mention(paper: dict) -> bool:
    """Check if paper mentions Mormon or Latter-day Saints."""
    text_to_check = json.dumps(paper).lower()
    return 'mormon' in text_to_check or 'latter-day saints' in text_to_check


def generate_benchmark_learnings(data: list[dict], csv_metadata: dict, output_path: str):
    """Generate benchmark_learnings.md with paper entries."""
    # Sort all papers by filename descending
    sorted_papers = sorted(data, key=lambda p: p.get('_filename', ''), reverse=True)
    
    lines = ["# Benchmark Learnings\n"]
    
    for paper in sorted_papers:
        filename = paper.get('_filename', '')
        meta = csv_metadata.get(filename, {})
        
        title = meta.get('title', 'Unknown Title')
        date = meta.get('date', 'Unknown Date')
        arxiv_url = get_arxiv_url(filename)
        
        benchmark_measurement = paper.get('benchmark_measurement', '')
        findings = paper.get('findings', '')
        
        # Combine benchmark_measurement and findings into a paragraph
        combined = f"{benchmark_measurement} {findings}".strip()
        
        # Check for Mormon/Latter-day Saints mention
        mormon_tag = " #Mormon" if check_mormon_mention(paper) else ""
        
        lines.append(f"## {title}{mormon_tag}\n")
        lines.append(f"[{arxiv_url}]({arxiv_url})\n")
        lines.append(f"**Date:** {date}\n")
        lines.append(f"{combined}\n")
        lines.append("")  # Blank line between entries
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"Learnings saved to {output_path}")


def generate_benchmark_summary(learnings_path: str, summary_path: str, model_name: str = "gemini-3-pro-preview"):
    """Generate a summary of the overall state of measuring religious bias in LLMs."""
    from google import genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return
    
    # Read the learnings file
    if not os.path.exists(learnings_path):
        print(f"Error: {learnings_path} not found. Run the script first to generate it.")
        return
    
    with open(learnings_path, 'r', encoding='utf-8') as f:
        learnings_content = f.read()
    
    prompt = """You are an expert researcher analyzing the current state of measuring religious bias in Large Language Models (LLMs).

Based on the following collection of benchmark papers and their findings, write a comprehensive summary of the overall state of measuring religious bias in LLMs. 

Your summary should cover:
1. **Overview**: A high-level summary of the current landscape of religious bias measurement in LLMs
2. **Key Findings**: The most significant and recurring findings across the papers
3. **Religious Groups Studied**: Which religious groups are most/least represented in the research
4. **Measurement Approaches**: Common methodologies and benchmarks used to measure religious bias
5. **Identified Biases**: What specific biases have been identified (e.g., which religions are favored/disfavored)
6. **Gaps and Limitations**: What is missing from current research, underrepresented areas
7. **Future Directions**: Recommendations for future research based on the gaps identified
8. **Recommendations for Measuring Latter-day Saint Bias**: Based on your analysis of the papers and methodologies, provide specific, actionable recommendations for how one could best measure explicit or implicit bias towards Latter-day Saints (Mormons) in modern LLMs. Include suggested benchmark types, prompt templates, evaluation metrics, and any unique considerations for this religious group.

Write in a scholarly but accessible tone. Use specific examples from the papers where relevant.

Here are the benchmark papers and their findings:

---
""" + learnings_content
    
    print(f"Generating summary using {model_name}...")
    
    client = genai.Client(api_key=api_key)
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt]
        )
        summary = response.text
        
        # Write the summary
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# Summary: The State of Measuring Religious Bias in LLMs\n\n")
            f.write(summary)
        
        print(f"Summary saved to {summary_path}")
        
    except Exception as e:
        print(f"Error generating summary: {e}")


def filter_religion_papers(data: list[dict]) -> list[dict]:
    """Filter papers to only include those with religion_component of 'major' or 'minor'."""
    return [p for p in data if p.get('religion_component', '').lower() in ('major', 'minor')]


def count_religious_groups(data: list[dict]) -> Counter:
    """Count occurrences of each religious group across all papers, with normalization."""
    counter = Counter()
    for paper in data:
        groups = paper.get('religious_groups', [])
        if isinstance(groups, list):
            for group in groups:
                normalized = normalize_religious_group(group)
                counter[normalized] += 1
    return counter


def normalize_model_name(model: str) -> str:
    """Normalize model names to combine variants."""
    # GPT-40 is a common typo/OCR error for GPT-4o
    if model.upper() == 'GPT-40':
        return 'GPT-4o'
    return model


def count_models_tested(data: list[dict]) -> Counter:
    """Count occurrences of each model tested across all papers."""
    counter = Counter()
    for paper in data:
        models = paper.get('models_tested', [])
        if isinstance(models, list):
            for model in models:
                normalized = normalize_model_name(model)
                counter[normalized] += 1
    return counter


def count_religion_component(data: list[dict]) -> Counter:
    """Count papers by religion_component (major vs minor)."""
    counter = Counter()
    for paper in data:
        component = paper.get('religion_component', '').lower()
        if component in ('major', 'minor'):
            counter[component.capitalize()] += 1
    return counter


def count_base_benchmarks(data: list[dict]) -> Counter:
    """Count occurrences of each base benchmark across all papers."""
    counter = Counter()
    for paper in data:
        benchmarks = paper.get('base_benchmarks', [])
        if isinstance(benchmarks, list):
            for benchmark in benchmarks:
                if benchmark:  # Skip empty strings
                    counter[benchmark] += 1
    return counter


def count_languages_evaluated(data: list[dict]) -> Counter:
    """Count occurrences of each language evaluated across all papers."""
    counter = Counter()
    for paper in data:
        languages = paper.get('languages_evaluated', [])
        if isinstance(languages, list):
            for language in languages:
                if language:  # Skip empty strings
                    counter[language] += 1
    return counter


def count_response_type(data: list[dict]) -> Counter:
    """Count papers by response type (short, long, or both)."""
    counter = Counter()
    for paper in data:
        types = paper.get('response_type', [])
        if isinstance(types, list):
            # Normalize to lowercase for comparison
            types_lower = [t.lower() for t in types if t]
            has_short = 'short' in types_lower
            has_long = 'long' in types_lower
            
            if has_short and has_long:
                counter['Both'] += 1
            elif has_short:
                counter['Short'] += 1
            elif has_long:
                counter['Long'] += 1
            elif types_lower:
                counter['Other'] += 1
    return counter


def count_continuous_testing(data: list[dict]) -> Counter:
    """Count papers by continuous_testing status (True vs False)."""
    counter = Counter()
    for paper in data:
        continuous = paper.get('continuous_testing', False)
        if continuous is True or (isinstance(continuous, str) and continuous.lower() == 'true'):
            counter['Yes'] += 1
        else:
            counter['No'] += 1
    return counter


def normalize_reference(ref: str) -> str:
    """Normalize a reference string for comparison."""
    if not ref:
        return ""
    # Convert to lowercase
    ref = ref.lower()
    # Normalize unicode characters
    ref = unicodedata.normalize('NFKD', ref).encode('ascii', 'ignore').decode('ascii')
    # Remove common prefixes like [1], 1., etc.
    ref = re.sub(r'^\s*\[?\d+\]?\s*\.?\s*', '', ref)
    # Remove extra whitespace
    ref = ' '.join(ref.split())
    # Remove punctuation except essential ones
    ref = re.sub(r'[^\w\s\-]', ' ', ref)
    ref = ' '.join(ref.split())
    return ref


def extract_reference_key(ref: str) -> tuple:
    """Extract key identifying features from a reference: (year, title_words, first_author)."""
    normalized = normalize_reference(ref)
    
    # Try to extract year (4 digits, typically 19xx or 20xx)
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', ref)
    year = year_match.group(1) if year_match else ""
    
    # Extract first few significant words (likely title or author)
    words = normalized.split()
    # Filter out very short words and common terms
    stop_words = {'the', 'a', 'an', 'and', 'or', 'of', 'in', 'on', 'for', 'to', 'with', 'by', 'from', 'at', 'is', 'are', 'was', 'were', 'et', 'al'}
    significant_words = [w for w in words if len(w) > 2 and w not in stop_words][:8]
    
    return (year, tuple(significant_words))


def count_references(data: list[dict]) -> Counter:
    """Count references across all papers, attempting to combine similar citations."""
    # First pass: collect all references with their normalized keys
    ref_groups = {}  # key -> list of (original_ref, count)
    
    for paper in data:
        refs = paper.get('references', [])
        if isinstance(refs, list):
            for ref in refs:
                if not ref or len(ref) < 20:  # Skip very short/empty refs
                    continue
                
                key = extract_reference_key(ref)
                if not key[1]:  # Skip if no significant words extracted
                    continue
                
                if key not in ref_groups:
                    ref_groups[key] = {'canonical': ref, 'count': 0}
                ref_groups[key]['count'] += 1
                # Keep the longest/most complete version as canonical
                if len(ref) > len(ref_groups[key]['canonical']):
                    ref_groups[key]['canonical'] = ref
    
    # Second pass: try to merge groups with very similar keys
    # Sort keys by year and first words for better matching
    sorted_keys = sorted(ref_groups.keys())
    merged = {}
    used_keys = set()
    
    for i, key1 in enumerate(sorted_keys):
        if key1 in used_keys:
            continue
        
        year1, words1 = key1
        merged_group = ref_groups[key1].copy()
        used_keys.add(key1)
        
        # Look for similar keys to merge
        for key2 in sorted_keys[i+1:]:
            if key2 in used_keys:
                continue
            
            year2, words2 = key2
            
            # Years must match (or one be empty)
            if year1 and year2 and year1 != year2:
                continue
            
            # Check word overlap
            words1_set = set(words1)
            words2_set = set(words2)
            if not words1_set or not words2_set:
                continue
            
            overlap = len(words1_set & words2_set)
            min_len = min(len(words1_set), len(words2_set))
            
            # Require significant overlap (at least 60% of shorter set)
            if min_len > 0 and overlap / min_len >= 0.6:
                merged_group['count'] += ref_groups[key2]['count']
                # Keep longer canonical reference
                if len(ref_groups[key2]['canonical']) > len(merged_group['canonical']):
                    merged_group['canonical'] = ref_groups[key2]['canonical']
                used_keys.add(key2)
        
        merged[key1] = merged_group
    
    # Build final counter with canonical references
    counter = Counter()
    for group in merged.values():
        canonical = shorten_author_list(group['canonical'])
        counter[canonical] = group['count']
    
    return counter


def shorten_author_list(ref: str) -> str:
    """Shorten author list to first author + et al. if multiple authors."""
    if not ref:
        return ref
    
    # Get first author (before first comma)
    comma_idx = ref.find(',')
    if comma_idx <= 0:
        return ref
    
    first_author = ref[:comma_idx].strip()
    
    # Check if there are multiple authors (more commas or "and")
    if ',' not in ref[comma_idx+1:] and ' and ' not in ref[comma_idx+1:comma_idx+50].lower():
        return ref  # Likely single author
    
    # Strategy: Find title by looking for a phrase (not just a single capitalized word)
    # Titles are phrases like "Judging llm-as-a-judge" or "Measuring massive multitask"
    # Author names are typically "Firstname Lastname" patterns
    
    # Look for ". [Word] [lowercase-word]" - indicates start of a title/sentence
    # This distinguishes from ". Lastname," which is an author
    title_match = re.search(r'\.\s+([A-Z][a-zA-Z\-]*\s+[a-z][a-zA-Z\-]*)', ref)
    if title_match:
        return f"{first_author} et al. {ref[title_match.start()+2:]}"
    
    # Look for title after year pattern: "2023. Title" or "(2023). Title"  
    year_title_match = re.search(r'(19\d{2}|20\d{2})[a-z]?\)?\.\s+([A-Z])', ref)
    if year_title_match:
        return f"{first_author} et al. ({year_title_match.group(1)}). {ref[year_title_match.end()-1:]}"
    
    # Look for common title-starting patterns (verbs, articles + noun)
    title_patterns = [
        r'\.\s+(Judging|Measuring|Learning|Evaluating|Investigating|Towards|Understanding|Analyzing|Building|Training|Improving)',
        r'\.\s+(A|An|The)\s+[A-Z]?[a-z]+',
        r'\.\s+(On|In|For|With)\s+[a-z]+',
        r'\.\s+[A-Z][a-z]+ing\s+[a-z]+',  # Gerunds like "Measuring something"
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, ref)
        if match:
            return f"{first_author} et al{ref[match.start():]}"
    
    # Last resort: Look for where author list likely ends
    # Authors often end with pattern like "and Lastname. " 
    and_match = re.search(r'\s+and\s+[A-Z][a-z]+(?:\s+[A-Z]\.?)?\s*[A-Z][a-z]+\.\s+', ref)
    if and_match:
        return f"{first_author} et al. {ref[and_match.end():]}"
    
    # If all else fails and we have multiple authors, truncate at reasonable point
    # Find a period that's followed by a capital and at least 2 more words
    for match in re.finditer(r'\.\s+([A-Z][^\.\,]+\s+[a-z]+[^\.\,]*)', ref[comma_idx:]):
        candidate = match.group(1)
        # Make sure this looks like a title (has lowercase words) not just "Lastname, Firstname"
        if re.search(r'[a-z]{3,}', candidate):
            return f"{first_author} et al. {candidate}{ref[comma_idx + match.end():]}"
    
    return ref


def generate_markdown_table(counter: Counter, title: str, col1: str, col2: str, limit: int = None) -> str:
    """Generate a markdown table from a Counter, sorted by count descending."""
    lines = [
        f"## {title}\n",
        f"| {col1} | {col2} |",
        "|---|---|"
    ]
    for item, count in counter.most_common(limit):
        lines.append(f"| {item} | {count} |")
    lines.append("")
    return "\n".join(lines)


def generate_markdown_table_references(counter: Counter, title: str, limit: int = None) -> str:
    """Generate a markdown table for references with Citations first, Reference second."""
    lines = [
        f"## {title}\n",
        "| Citations | Reference |",
        "|---|---|"
    ]
    for ref, count in counter.most_common(limit):
        # Escape pipe characters in references
        ref_escaped = ref.replace("|", "\\|")
        lines.append(f"| {count} | {ref_escaped} |")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Create summary statistics from 2nd pass JSON files.")
    parser.add_argument("--json_dir", default="json/2nd_pass_json", help="Directory containing JSON analysis files")
    parser.add_argument("--output", default="analysis/benchmark_analysis.md", help="Output markdown file")
    parser.add_argument("--csv", default="csv/1st_pass_results.csv", help="Input CSV file with paper metadata")
    parser.add_argument("--learnings", default="analysis/benchmark_learnings.md", help="Output learnings markdown file")
    parser.add_argument("--summary", default="analysis/benchmark_summary.md", help="Output summary markdown file")
    parser.add_argument("--summary-model", default="gemini-3-pro-preview", help="Model to use for summary generation")
    
    args = parser.parse_args()
    
    json_dir = args.json_dir
    output_file = args.output
    csv_file = args.csv
    learnings_file = args.learnings
    summary_file = args.summary
    summary_model = args.summary_model
    
    if not os.path.exists(json_dir):
        print(f"Error: Directory {json_dir} not found.")
        return
    
    # Load all JSON files
    all_data = load_json_files(json_dir)
    print(f"Loaded {len(all_data)} JSON files from {json_dir}")
    
    # Load CSV metadata for titles and dates
    csv_metadata = load_csv_metadata(csv_file)
    print(f"Loaded metadata for {len(csv_metadata)} papers from {csv_file}")
    
    # Filter to only papers with religion_component of 'major' or 'minor'
    data = filter_religion_papers(all_data)
    print(f"Filtered to {len(data)} papers with major/minor religion component")
    
    if not data:
        print("No data to process.")
        return
    
    # Count religion component (major vs minor)
    religion_component_count = count_religion_component(data)
    
    # Count religious groups
    religious_groups_count = count_religious_groups(data)
    
    # Count models tested
    models_tested_count = count_models_tested(data)
    
    # Count base benchmarks
    base_benchmarks_count = count_base_benchmarks(data)
    
    # Count languages evaluated
    languages_count = count_languages_evaluated(data)
    
    # Count response type
    response_type_count = count_response_type(data)
    
    # Count continuous testing
    continuous_testing_count = count_continuous_testing(data)
    
    # Count references (most cited papers)
    print("Analyzing references (this may take a moment)...")
    references_count = count_references(data)
    
    # Generate markdown content
    md_content = [
        "# Benchmark Analysis Summary\n",
        f"Total papers analyzed: {len(data)}\n",
        generate_markdown_table(religion_component_count, "Religion Component", "Component", "Count"),
        generate_markdown_table(religious_groups_count, "Religious Groups (Top 25)", "Religious Group", "Count", limit=25),
        generate_markdown_table(models_tested_count, "Models Tested (Top 25)", "Model", "Count", limit=25),
        generate_markdown_table(base_benchmarks_count, "Base Benchmarks (Top 25)", "Benchmark", "Count", limit=25),
        generate_markdown_table(languages_count, "Languages Evaluated (Top 25)", "Language", "Count", limit=25),
        generate_markdown_table(response_type_count, "Response Type", "Type", "Count"),
        generate_markdown_table(continuous_testing_count, "Continuous Testing", "Status", "Count"),
        generate_markdown_table_references(references_count, "Most Cited Papers (Top 100)", limit=100),
    ]
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_content))
    
    print(f"Summary saved to {output_file}")
    
    # Generate benchmark learnings
    generate_benchmark_learnings(data, csv_metadata, learnings_file)
    
    # Generate benchmark summary using LLM
    generate_benchmark_summary(learnings_file, summary_file, summary_model)
    
    # Create versioned copies in analysis/versions
    versions_dir = "analysis/versions"
    os.makedirs(versions_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for src_file in [output_file, learnings_file, summary_file]:
        if os.path.exists(src_file):
            base_name = Path(src_file).stem
            ext = Path(src_file).suffix
            versioned_name = f"{base_name}_{timestamp}{ext}"
            versioned_path = os.path.join(versions_dir, versioned_name)
            shutil.copy2(src_file, versioned_path)
            print(f"Versioned copy saved to {versioned_path}")


if __name__ == "__main__":
    main()
