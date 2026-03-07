#!/usr/bin/env python3
"""
Analyze bias targets from 3rd pass analysis.

This script:
1. Normalizes bias target categories (handles case, synonyms)
2. Reports how often each bias target is measured
3. Reports how often each target is measured in isolation (singleton)
4. Reports how often each target is the primary bias target
5. For religious bias, uses Gemini to group methodologies into strategies
"""

import json
import os
from pathlib import Path
from collections import Counter

from shared import genai

DEFAULT_MODEL = "gemini-3-pro-preview"

# Directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
JSON_DIR = PROJECT_DIR / "json" / "2nd_pass_json"


# Normalization mappings - maps variations to canonical form
NORMALIZATION_MAP = {
    # Gender
    "gender bias": "Gender bias",
    "gender": "Gender bias",
    "sex bias": "Gender bias",
    "sex/gender bias": "Gender bias",
    "sexism": "Gender bias",
    "sexism and gender bias": "Gender bias",
    "misogyny and gender bias": "Gender bias",
    "gender bias (sexism)": "Gender bias",
    "gender bias (misogyny)": "Gender bias",
    "gender identity bias": "Gender bias",
    
    # Racial/Ethnic
    "racial bias": "Racial/Ethnic bias",
    "race bias": "Racial/Ethnic bias",
    "racism": "Racial/Ethnic bias",
    "ethnic bias": "Racial/Ethnic bias",
    "ethnicity bias": "Racial/Ethnic bias",
    "racial/ethnic bias": "Racial/Ethnic bias",
    "racial and ethnic bias": "Racial/Ethnic bias",
    "racial, ethnic, and nationality bias": "Racial/Ethnic bias",
    "racial/ethnicity bias": "Racial/Ethnic bias",
    "racial and ethnicity bias": "Racial/Ethnic bias",
    "racial and nationality bias": "Racial/Ethnic bias",
    "skin tone bias": "Racial/Ethnic bias",
    "skin color bias": "Racial/Ethnic bias",
    
    # Religious
    "religious bias": "Religious bias",
    "religion bias": "Religious bias",
    "cultural and religious bias": "Religious bias",
    
    # Age
    "age bias": "Age bias",
    "ageism": "Age bias",
    
    # Political/Ideological
    "political bias": "Political bias",
    "politics bias": "Political bias",
    "geopolitical bias": "Political bias",
    "ideological and political bias": "Political bias",
    "socio-political bias": "Political bias",
    "ideological bias": "Political bias",
    "political and ideological bias": "Political bias",
    "political/ideological bias": "Political bias",
    "viewpoint bias": "Political bias",
    "stance bias": "Political bias",
    
    # Nationality
    "nationality bias": "Nationality bias",
    "national bias": "Nationality bias",
    "country bias": "Nationality bias",
    
    # Cultural
    "cultural bias": "Cultural bias",
    "culture bias": "Cultural bias",
    "geo-cultural bias": "Cultural bias",
    "cultural and language bias": "Cultural bias",
    "cultural and linguistic bias": "Cultural bias",
    "cultural and nationality bias": "Cultural bias",
    "language and cultural bias": "Cultural bias",
    
    # Geographic
    "geographic bias": "Geographic bias",
    "geographical bias": "Geographic bias",
    "geographic/nationality bias": "Geographic bias",
    "geographic and cultural bias": "Geographic bias",
    "location bias": "Geographic bias",
    "geospatial bias": "Geographic bias",
    "spatial bias": "Geographic bias",
    
    # Language/Linguistic
    "language bias": "Language bias",
    "linguistic bias": "Language bias",
    "dialect bias": "Language bias",
    "dialect/language bias": "Language bias",
    "language and dialect bias": "Language bias",
    "language/dialect bias": "Language bias",
    "dialectal bias": "Language bias",
    "accent bias": "Language bias",
    "lexical bias": "Language bias",
    
    # Position/Positional
    "position bias": "Position bias",
    "positional bias": "Position bias",
    
    # Sexual orientation / LGBTQ+
    "sexual orientation bias": "Sexual orientation bias",
    "lgbtq+ bias": "Sexual orientation bias",
    "lgbtq bias": "Sexual orientation bias",
    "homophobia": "Sexual orientation bias",
    "gender and sexual orientation bias": "Sexual orientation bias",
    "gender/sexual orientation bias": "Sexual orientation bias",
    "orientation bias": "Sexual orientation bias",
    "sexual orientation and gender identity bias": "Sexual orientation bias",
    
    # Socioeconomic
    "socioeconomic bias": "Socioeconomic bias",
    "socio-economic bias": "Socioeconomic bias",
    "economic bias": "Socioeconomic bias",
    "class bias": "Socioeconomic bias",
    "class and socioeconomic bias": "Socioeconomic bias",
    "socioeconomic status bias": "Socioeconomic bias",
    
    # Disability
    "disability bias": "Disability bias",
    "ableism": "Disability bias",
    "ability bias": "Disability bias",
    
    # Physical appearance
    "physical appearance bias": "Physical appearance bias",
    "appearance bias": "Physical appearance bias",
    "body type bias": "Physical appearance bias",
    "weight bias": "Physical appearance bias",
    
    # Occupational
    "occupational bias": "Occupational bias",
    "profession bias": "Occupational bias",
    "occupational/socioeconomic bias": "Occupational bias",
    "occupation bias": "Occupational bias",
    "professional bias": "Occupational bias",
    
    # Hate speech / Toxicity
    "hate speech detection": "Hate speech/Toxicity",
    "hate speech detection (general toxic or hateful content)": "Hate speech/Toxicity",
    "toxic content": "Hate speech/Toxicity",
    "toxicity": "Hate speech/Toxicity",
    "toxicity bias": "Hate speech/Toxicity",
    "hate speech": "Hate speech/Toxicity",
    "toxicity and hate speech": "Hate speech/Toxicity",
    
    # Stereotyping
    "stereotyping": "Stereotyping",
    "stereotype bias": "Stereotyping",
    "stereotypes": "Stereotyping",
    "social bias": "Stereotyping",
    "stereotypical bias": "Stereotyping",
    
    # Fairness
    "fairness in outcomes": "Fairness",
    "fairness": "Fairness",
    "outcome fairness": "Fairness",
    
    # Length / Verbosity
    "length bias": "Length bias",
    "verbosity bias": "Length bias",
    "length bias (verbosity bias)": "Length bias",
    
    # Self-preference / Self-bias
    "self-preference bias": "Self-preference bias",
    "self preference bias": "Self-preference bias",
    "self-enhancement bias": "Self-preference bias",
    "self-bias": "Self-preference bias",
    "self-evaluation bias": "Self-preference bias",
    
    # Regional
    "regional bias": "Regional bias",
    "regional language bias": "Regional bias",
    
    # Annotation/Annotator
    "annotator bias": "Annotator bias",
    "annotation bias": "Annotator bias",
    
    # Educational
    "educational bias": "Educational bias",
    "education bias": "Educational bias",
    "educational background bias": "Educational bias",
    
    # Sycophancy
    "sycophancy bias": "Sycophancy bias",
    "sycophancy": "Sycophancy bias",
    "sycophantic bias": "Sycophancy bias",
    
    # Cognitive
    "cognitive bias": "Cognitive bias",
    "cognitive biases": "Cognitive bias",
    "confirmation bias": "Cognitive bias",
    "anchoring bias": "Cognitive bias",
    "recency bias": "Cognitive bias",
    "authority bias": "Cognitive bias",
    "conformity bias": "Cognitive bias",
    
    # Demographic (broad)
    "demographic bias": "Demographic bias",
    "sociodemographic bias": "Demographic bias",
    "social and demographic bias": "Demographic bias",
    
    # Intersectional
    "intersectional bias": "Intersectional bias",
    "intergroup bias": "Intersectional bias",
    
    # Moral/Ethical
    "moral bias": "Moral/Ethical bias",
    "ethical and moral bias": "Moral/Ethical bias",
    "moral and ethical bias": "Moral/Ethical bias",
    
    # Sentiment
    "sentiment bias": "Sentiment bias",
    "positivity bias": "Sentiment bias",
    "social desirability bias": "Sentiment bias",
    
    # Caste
    "caste bias": "Caste bias",
    
    # Mental health
    "mental health bias": "Mental health bias",
    "health status bias": "Mental health bias",
    
    # Marital/Family status
    "marital status bias": "Marital status bias",
    "immigration status bias": "Marital status bias",
    
    # Media
    "media bias": "Media bias",
    "reporting bias": "Media bias",
    "framing bias": "Media bias",
    
    # Evaluation/Scoring
    "evaluation bias": "Evaluation bias",
    "evaluator bias": "Evaluation bias",
    "scoring bias": "Evaluation bias",
    "evaluation metric bias": "Evaluation bias",
    "llm evaluator bias": "Evaluation bias",
    
    # Dataset/Methodological
    "dataset bias": "Dataset bias",
    "dataset artifact bias": "Dataset bias",
    "dataset bias (annotation artifacts)": "Dataset bias",
    "dataset bias (spurious correlations)": "Dataset bias",
    "spurious correlation bias": "Dataset bias",
    "spurious bias": "Dataset bias",
    "class imbalance bias": "Dataset bias",
    "data contamination bias": "Dataset bias",
    "sampling bias": "Dataset bias",
    "selection bias": "Dataset bias",
    "label bias": "Dataset bias",
    "historical bias": "Dataset bias",
    
    # Modality
    "modality bias": "Modality bias",
    "visual bias": "Modality bias",
    
    # Popularity
    "popularity bias": "Popularity bias",
    "brand bias": "Popularity bias",
    
    # Domain
    "domain bias": "Domain bias",
    "topic bias": "Domain bias",
    
    # Representation
    "representation bias": "Representation bias",
    "representational bias": "Representation bias",
    
    # Algorithmic
    "algorithmic bias": "Algorithmic bias",
    "general algorithmic bias": "Algorithmic bias",
    "automation bias": "Algorithmic bias",
    "inductive bias": "Algorithmic bias",
    
    # Identity
    "identity bias": "Identity bias",
    "name bias": "Identity bias",
    
    # Style/Response
    "response bias": "Response bias",
    "stylistic bias": "Response bias",
    "style bias": "Response bias",
    
    # General / Other
    "general bias": "General bias",
    "general social bias": "General bias",
    "societal bias": "General bias",
    
    # Primary target normalization
    "none": "No Primary Bias Target",
    "no primary bias target": "No Primary Bias Target",
    "n/a": "No Primary Bias Target",
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
    """Load all bias target data from 3rd pass JSON files."""
    papers_data = []
    
    for json_file in JSON_DIR.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            if 'bias_targets' not in data:
                continue
            
            raw_targets = data['bias_targets']
            # Handle both object format [{target, methodology}] and legacy string format
            normalized = []
            methodologies = []
            for entry in raw_targets:
                if isinstance(entry, dict):
                    normalized.append(normalize_target(entry.get('target', '')))
                    methodologies.append(entry.get('methodology', ''))
                else:
                    normalized.append(normalize_target(entry))
                    methodologies.append('')
            
            primary = data.get('primary_bias_target', '')
            if primary:
                primary = normalize_target(primary)
            
            papers_data.append({
                'arxiv_id': json_file.stem,
                'title': data.get('title', ''),
                'normalized_targets': normalized,
                'methodologies': methodologies,
                'primary_bias_target': primary,
                'count': len(normalized)
            })
        except (json.JSONDecodeError, IOError):
            continue
    
    return papers_data


def classify_methodologies(methodologies: list[tuple[str, str, str]],
                           model_name: str = DEFAULT_MODEL) -> dict:
    """Use Gemini to classify raw methodology descriptions into strategy categories.
    
    Args:
        methodologies: list of (methodology, arxiv_id, title) tuples
        model_name: Gemini model to use
    
    Returns:
        dict mapping strategy name to list of (methodology, arxiv_id, title) tuples
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Warning: GOOGLE_API_KEY not set, skipping methodology classification.")
        return {}
    
    # Build the list of methodology descriptions
    method_texts = [m for m, _, _ in methodologies]
    
    prompt = f"""Below is a list of {len(method_texts)} methodology descriptions for how academic papers measure religious bias in Large Language Models.

Classify each methodology into ONE of these high-level measurement strategy categories. Assign the category that best fits the core approach.

Categories:
- "Sentiment/Regard Analysis" - Measuring sentiment, regard, or toxicity scores across religious groups
- "Stereotype Association Tests" - Using sentence pairs or word associations to test stereotypical associations (e.g., StereoSet, CrowS-Pairs)
- "Question Answering / BBQ" - Multiple-choice or QA-based evaluation of biased reasoning (e.g., BBQ benchmark)
- "Counterfactual / Template Substitution" - Swapping religious identity terms in templates or prompts and comparing outputs
- "Open-Ended Generation Analysis" - Analyzing free-form text generated by models for bias signals
- "Embedding / Representation Analysis" - Measuring bias in word embeddings or internal representations
- "Downstream Task Fairness" - Measuring performance disparities across groups on tasks like classification, detection, etc.
- "Benchmark Suite / Multi-Method" - Papers using established multi-method benchmark suites
- "Survey / Literature Review" - Reviewing or surveying existing bias measurement approaches
- "Red Teaming / Adversarial" - Using adversarial prompts, jailbreaks, or red-teaming to elicit biased outputs
- "Human Evaluation" - Using human annotators to assess bias in outputs
- "Other" - Anything that doesn't fit the above categories

Return a JSON array where each element is a string — the category name for the corresponding methodology (same order as input). Output ONLY the JSON array.

Methodologies:
{json.dumps(method_texts, indent=2)}
"""
    
    client = genai.Client(api_key=api_key)
    
    # Chunk if too many (each chunk ≤ 200 to stay within context limits)
    CHUNK_SIZE = 200
    all_labels = []
    
    for i in range(0, len(method_texts), CHUNK_SIZE):
        chunk = method_texts[i:i + CHUNK_SIZE]
        chunk_prompt = f"""Below is a list of {len(chunk)} methodology descriptions for how academic papers measure religious bias in Large Language Models.

Classify each methodology into ONE of these high-level measurement strategy categories. Assign the category that best fits the core approach.

Categories:
- "Sentiment/Regard Analysis" - Measuring sentiment, regard, or toxicity scores across religious groups
- "Stereotype Association Tests" - Using sentence pairs or word associations to test stereotypical associations (e.g., StereoSet, CrowS-Pairs)
- "Question Answering / BBQ" - Multiple-choice or QA-based evaluation of biased reasoning (e.g., BBQ benchmark)
- "Counterfactual / Template Substitution" - Swapping religious identity terms in templates or prompts and comparing outputs
- "Open-Ended Generation Analysis" - Analyzing free-form text generated by models for bias signals
- "Embedding / Representation Analysis" - Measuring bias in word embeddings or internal representations
- "Downstream Task Fairness" - Measuring performance disparities across groups on tasks like classification, detection, etc.
- "Benchmark Suite / Multi-Method" - Papers using established multi-method benchmark suites
- "Survey / Literature Review" - Reviewing or surveying existing bias measurement approaches
- "Red Teaming / Adversarial" - Using adversarial prompts, jailbreaks, or red-teaming to elicit biased outputs
- "Human Evaluation" - Using human annotators to assess bias in outputs
- "Other" - Anything that doesn't fit the above categories

Return a JSON array where each element is a string — the category name for the corresponding methodology (same order as input). Output ONLY the JSON array.

Methodologies:
{json.dumps(chunk, indent=2)}
"""
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[chunk_prompt],
                config={"response_mime_type": "application/json"}
            )
            labels = json.loads(response.text)
            if len(labels) != len(chunk):
                print(f"  Warning: Got {len(labels)} labels for {len(chunk)} methods in chunk {i//CHUNK_SIZE + 1}")
                # Pad or truncate
                labels = (labels + ["Other"] * len(chunk))[:len(chunk)]
            all_labels.extend(labels)
        except Exception as e:
            print(f"  Error classifying chunk {i//CHUNK_SIZE + 1}: {e}")
            all_labels.extend(["Other"] * len(chunk))
    
    # Group by strategy
    strategies = {}
    for label, (method, arxiv_id, title) in zip(all_labels, methodologies):
        strategies.setdefault(label, []).append((method, arxiv_id, title))
    
    return strategies


def print_co_measurement(target: str, papers_data: list):
    """Print a histogram of biases co-measured alongside the given target."""
    co_counter = Counter()
    target_paper_count = 0
    
    for paper in papers_data:
        targets = set(paper['normalized_targets'])
        if target in targets:
            target_paper_count += 1
            for t in targets:
                if t != target:
                    co_counter[t] += 1
    
    if not target_paper_count:
        print(f"\n No papers measure {target}.")
        return
    
    print(f"\n{'=' * 80}")
    print(f" CO-MEASUREMENT: What else is measured alongside {target}?")
    print(f" ({target_paper_count} papers measure {target})")
    print(f"{'=' * 80}")
    print(f"\n {'Rank':>4}  {'Count':>5}  {'%':>6}  Category")
    print(f" {'':->4}  {'':->5}  {'':->6}  {'':->40}")
    for i, (cat, count) in enumerate(co_counter.most_common(25), 1):
        pct = count / target_paper_count * 100
        bar = '#' * max(1, int(pct / 2))
        print(f" {i:4d}  {count:5d}  {pct:5.1f}%  {cat}  {bar}")
    print()


def print_focus_table(papers_data: list, all_counter: Counter):
    """Print top 25 bias targets sorted by % that are exclusive or primary focus."""
    total_counter = Counter()
    focused_counter = Counter()
    
    for paper in papers_data:
        targets = set(paper['normalized_targets'])
        primary = paper['primary_bias_target']
        is_exclusive = len(targets) == 1
        
        for t in targets:
            total_counter[t] += 1
            if is_exclusive or t == primary:
                focused_counter[t] += 1
    
    top25 = all_counter.most_common(25)
    rows = []
    for cat, total in top25:
        focus = focused_counter.get(cat, 0)
        pct = focus / total * 100 if total else 0
        rows.append((cat, total, focus, pct))
    
    rows.sort(key=lambda r: -r[3])
    
    print(f"\n{'=' * 80}")
    print(f" FOCUS ANALYSIS: Top 25 targets by % exclusive or primary")
    print(f" (Focus = paper studies this target exclusively OR as its primary target)")
    print(f"{'=' * 80}")
    print(f"\n {'Rank':>4}  {'Total':>5}  {'Focus':>5}  {'% Focus':>7}  Category")
    print(f" {'':->4}  {'':->5}  {'':->5}  {'':->7}  {'':->35}")
    for i, (cat, total, focus, pct) in enumerate(rows, 1):
        bar = '#' * max(1, int(pct / 2)) if focus > 0 else '.'
        print(f" {i:4d}  {total:5d}  {focus:5d}  {pct:6.1f}%  {cat}  {bar}")
    print()


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
        print(f" {i:<{col1_width}} | {count:<{col2_width}} | {category}")
    
    print()


def main():
    print("\n" + "=" * 60)
    print(" BIAS TARGET ANALYSIS (3rd Pass)")
    print("=" * 60)
    
    # Load data
    papers_data = load_bias_data()
    
    if not papers_data:
        print("No papers with bias_targets found.")
        return
    
    # Collect all normalized targets, singletons, primaries, and religious methodologies
    all_targets = []
    singleton_targets = []
    primary_targets = Counter()
    list_lengths = []
    religious_methodologies = []  # (methodology, arxiv_id, title)
    
    for paper in papers_data:
        targets = paper['normalized_targets']
        methods = paper['methodologies']
        all_targets.extend(targets)
        list_lengths.append(paper['count'])
        
        if len(targets) == 1:
            singleton_targets.append(targets[0])
        
        primary = paper['primary_bias_target']
        if primary:
            primary_targets[primary] += 1
        
        # Collect religious bias methodologies
        for target, method in zip(targets, methods):
            if target == "Religious bias" and method:
                religious_methodologies.append((
                    method,
                    paper['arxiv_id'],
                    paper['title']
                ))
    
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
        print(f"   {length:2d} targets: {count:4d} papers")
    
    # Top 25 overall
    top_25_all = all_counter.most_common(25)
    print_table("TOP 25 BIAS TARGETS (How often measured)", top_25_all)
    
    # Top 25 singletons
    top_25_singleton = singleton_counter.most_common(25)
    print_table("TOP 25 SINGLETON BIAS TARGETS (Measured in isolation)", top_25_singleton)
    
    # Top 25 primary targets
    top_25_primary = primary_targets.most_common(25)
    print_table("TOP 25 PRIMARY BIAS TARGETS", top_25_primary)
    
    # Focus analysis (exclusive or primary, sorted by %)
    print_focus_table(papers_data, all_counter)
    
    # Co-measurement histograms
    print_co_measurement("Gender bias", papers_data)
    print_co_measurement("Religious bias", papers_data)
    
    # Religious bias specific stats
    religious_count = all_counter.get("Religious bias", 0)
    religious_singleton = singleton_counter.get("Religious bias", 0)
    religious_primary = primary_targets.get("Religious bias", 0)
    religious_rank = next(
        (i for i, (cat, _) in enumerate(all_counter.most_common(), 1) if cat == "Religious bias"),
        None
    )
    print("=" * 80)
    print(" RELIGIOUS BIAS FOCUS")
    print("=" * 80)
    print(f" Total mentions:         {religious_count}")
    print(f" As singleton:           {religious_singleton}")
    print(f" As primary target:      {religious_primary}")
    print(f" Rank (overall):         {religious_rank if religious_rank else 'N/A'}")
    
    # Religious bias methodology report
    if religious_methodologies:
        print()
        print("=" * 80)
        print(f" RELIGIOUS BIAS MEASUREMENT STRATEGIES ({len(religious_methodologies)} papers)")
        print("=" * 80)
        print()
        print(" Classifying methodologies using Gemini...")
        strategies = classify_methodologies(religious_methodologies)
        
        if strategies:
            # Sort strategies by count
            sorted_strategies = sorted(strategies.items(), key=lambda x: -len(x[1]))
            
            for strategy, entries in sorted_strategies:
                count = len(entries)
                pct = count / len(religious_methodologies) * 100
                print(f"\n {'-' * 76}")
                print(f" {strategy}: {count} papers ({pct:.1f}%)")
                print(f" {'-' * 76}")
                # Show up to 3 example methodologies
                for method, arxiv_id, title in entries[:3]:
                    print(f"   - [{arxiv_id}] {method[:120]}")
                if count > 3:
                    print(f"   ... and {count - 3} more")
    
    # List papers with Religious bias as primary or singleton
    religious_primary_papers = []
    religious_singleton_papers = []
    for paper in papers_data:
        is_primary = paper['primary_bias_target'] == "Religious bias"
        is_singleton = len(paper['normalized_targets']) == 1 and "Religious bias" in paper['normalized_targets']
        if is_primary:
            religious_primary_papers.append(paper)
        if is_singleton and not is_primary:
            religious_singleton_papers.append(paper)
    
    print()
    print("=" * 80)
    print(" PAPERS WITH RELIGIOUS BIAS AS PRIMARY TARGET OR SINGLETON")
    print("=" * 80)
    
    if religious_primary_papers:
        print(f"\n Primary target ({len(religious_primary_papers)} papers):")
        for paper in sorted(religious_primary_papers, key=lambda p: p['arxiv_id']):
            title = paper['title'] or 'Unknown'
            print(f"   {paper['arxiv_id']:20s}  {title}")
    
    if religious_singleton_papers:
        print(f"\n Singleton only ({len(religious_singleton_papers)} papers):")
        for paper in sorted(religious_singleton_papers, key=lambda p: p['arxiv_id']):
            title = paper['title'] or 'Unknown'
            print(f"   {paper['arxiv_id']:20s}  {title}")
    
    if not religious_primary_papers and not religious_singleton_papers:
        print("\n No papers found.")
    
    print()


if __name__ == "__main__":
    main()
