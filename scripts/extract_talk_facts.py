#!/usr/bin/env python3
"""
Extract impactful facts about religious bias in LLMs for use in talks/papers.
Reads from analysis files and refers back to original PDFs for accuracy and context.
Filters for recency to avoid presenting outdated information.
"""

import os
import csv
import json
import glob
import argparse
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

from shared import genai, load_csv_metadata


def load_analysis_files(analysis_dir: str) -> dict:
    """Load all analysis markdown files."""
    files = {}
    for name in ['benchmark_analysis.md', 'benchmark_learnings.md', 'benchmark_summary.md']:
        path = os.path.join(analysis_dir, name)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                files[name] = f.read()
    return files


def load_json_data(json_dir: str) -> list[dict]:
    """Load all 2nd pass JSON files with paper details."""
    data = []
    if not os.path.exists(json_dir):
        return data
    
    for json_path in glob.glob(os.path.join(json_dir, "*.json")):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                paper = json.load(f)
                paper['_filename'] = Path(json_path).name
                paper['_json_path'] = json_path
                data.append(paper)
        except (json.JSONDecodeError, IOError):
            continue
    return data




def filter_recent_papers(papers: list[dict], csv_metadata: dict, months: int = 24) -> list[dict]:
    """Filter papers to only include those from the last N months."""
    cutoff = datetime.now() - timedelta(days=months * 30)
    recent = []
    
    for paper in papers:
        filename = paper.get('_filename', '').replace('.json', '.pdf')
        meta = csv_metadata.get(filename, {})
        date_str = meta.get('date', '')
        
        if date_str:
            parsed = False
            for fmt in ['%Y-%m-%d', '%Y-%m', '%Y']:
                try:
                    paper_date = datetime.strptime(date_str, fmt)
                    if paper_date >= cutoff:
                        paper['_date'] = date_str
                        paper['_title'] = meta.get('title', 'Unknown')
                        recent.append(paper)
                    parsed = True
                    break
                except ValueError:
                    continue
            if not parsed:
                # If date parsing fails, include it anyway
                paper['_date'] = date_str
                paper['_title'] = meta.get('title', 'Unknown')
                recent.append(paper)
        else:
            # No date - include with caution flag
            paper['_date'] = 'Unknown'
            paper['_title'] = meta.get('title', 'Unknown')
            recent.append(paper)
    
    return recent


def get_pdf_context(pdf_path: str, query: str, api_key: str, model_name: str) -> str:
    """Query a specific PDF for better context on a fact."""
    if not os.path.exists(pdf_path):
        return ""
    
    client = genai.Client(api_key=api_key)
    
    try:
        # Upload the PDF
        sample_file = client.files.upload(file=pdf_path)
        
        # Wait for processing
        while sample_file.state.name == "PROCESSING":
            time.sleep(1)
            sample_file = client.files.get(name=sample_file.name)
        
        if sample_file.state.name == "FAILED":
            return ""
        
        prompt = f"""Based on this paper, provide a precise, quotable statement about the following topic. 
Include specific numbers, percentages, or findings where available.
Be concise (1-2 sentences max) and accurate.

Topic: {query}

If this paper doesn't contain relevant information about this topic, respond with "NOT_FOUND"."""

        response = client.models.generate_content(
            model=model_name,
            contents=[sample_file, prompt]
        )
        
        result = response.text.strip()
        if result == "NOT_FOUND":
            return ""
        return result
        
    except Exception as e:
        print(f"  Warning: Could not query PDF {pdf_path}: {e}")
        return ""


def extract_facts(analysis_files: dict, papers: list[dict], api_key: str, model_name: str, 
                  pdf_dir: str, verify_with_pdf: bool = True) -> list[dict]:
    """Extract impactful facts using LLM analysis."""
    client = genai.Client(api_key=api_key)
    
    # Combine analysis content
    combined_content = "\n\n---\n\n".join([
        f"## {name}\n\n{content}" 
        for name, content in analysis_files.items()
    ])
    
    # First pass: identify key facts from analysis
    extract_prompt = """You are helping prepare a talk about religious bias in Large Language Models (LLMs).

Based on the following analysis of benchmark papers, identify 15-20 impactful facts that would be valuable for an academic presentation. Focus on:

1. **Quantitative findings** - specific numbers, percentages, or measurements
2. **Surprising discoveries** - counter-intuitive results
3. **Bias patterns** - which religions are favored/disfavored and how
4. **Methodological insights** - effective ways to measure religious bias
5. **Gaps in research** - underrepresented religions or approaches
6. **Recent trends** - how the field is evolving

For each fact, provide:
- A concise, quotable statement (1-2 sentences)
- The source paper(s) if identifiable from the content
- A category (quantitative/surprising/bias_pattern/methodology/gap/trend)
- An impact score (1-5, where 5 is most impactful for a talk)

Format as JSON array:
[
  {
    "statement": "concise quotable fact",
    "source_hint": "paper title or arxiv id if mentioned",
    "category": "category_name",
    "impact_score": 4,
    "needs_verification": true/false
  }
]

Focus on accuracy over sensationalism. Flag any facts that seem uncertain and need verification.

Analysis content:
---
""" + combined_content

    print("Extracting key facts from analysis...")
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[extract_prompt]
        )
        
        # Parse JSON from response
        text = response.text
        # Find JSON array in response
        json_match = re.search(r'\[[\s\S]*\]', text)
        if json_match:
            facts = json.loads(json_match.group())
        else:
            print("Warning: Could not parse facts from LLM response")
            return []
            
    except Exception as e:
        print(f"Error extracting facts: {e}")
        return []
    
    # Second pass: verify/enhance facts needing verification using PDFs
    if verify_with_pdf and pdf_dir:
        print(f"\nVerifying facts against original PDFs...")
        
        for i, fact in enumerate(facts):
            if fact.get('needs_verification', False) or fact.get('impact_score', 0) >= 4:
                source_hint = fact.get('source_hint', '')
                
                # Try to find matching PDF
                pdf_path = None
                if source_hint:
                    # Check if it's an arxiv ID
                    arxiv_match = re.search(r'(\d{4}\.\d+)', source_hint)
                    if arxiv_match:
                        potential_path = os.path.join(pdf_dir, f"{arxiv_match.group(1)}.pdf")
                        if os.path.exists(potential_path):
                            pdf_path = potential_path
                
                if pdf_path:
                    print(f"  Verifying fact {i+1} against {Path(pdf_path).name}...")
                    enhanced = get_pdf_context(pdf_path, fact['statement'], api_key, model_name)
                    if enhanced:
                        fact['verified_statement'] = enhanced
                        fact['verified'] = True
                    else:
                        fact['verified'] = False
                else:
                    fact['verified'] = False
    
    return facts


def format_output(facts: list[dict], output_format: str = 'markdown') -> str:
    """Format extracted facts for output."""
    if output_format == 'json':
        return json.dumps(facts, indent=2)
    
    # Markdown format
    lines = ["# Impactful Facts: Religious Bias in LLMs\n"]
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    lines.append("*Use these facts carefully - verify currency before presenting.*\n\n")
    
    # Group by category
    categories = {
        'quantitative': '📊 Quantitative Findings',
        'surprising': '💡 Surprising Discoveries', 
        'bias_pattern': '⚖️ Bias Patterns',
        'methodology': '🔬 Methodological Insights',
        'gap': '🔍 Research Gaps',
        'trend': '📈 Recent Trends'
    }
    
    for cat_key, cat_title in categories.items():
        cat_facts = [f for f in facts if f.get('category') == cat_key]
        if not cat_facts:
            continue
            
        lines.append(f"## {cat_title}\n")
        
        # Sort by impact score
        cat_facts.sort(key=lambda x: x.get('impact_score', 0), reverse=True)
        
        for fact in cat_facts:
            impact = '⭐' * fact.get('impact_score', 3)
            statement = fact.get('verified_statement', fact.get('statement', ''))
            source = fact.get('source_hint', '')
            verified = '✓' if fact.get('verified', False) else '?'
            
            lines.append(f"- **[{verified}]** {statement}")
            if source:
                lines.append(f"  - *Source: {source}*")
            lines.append(f"  - Impact: {impact}")
            lines.append("")
    
    # Add usage notes
    lines.append("\n---\n")
    lines.append("## Usage Notes\n")
    lines.append("- **[✓]** = Verified against original PDF")
    lines.append("- **[?]** = Extracted from analysis, recommend verification")
    lines.append("- Always check paper dates before citing - field evolves rapidly")
    lines.append("- Consider contacting original authors for latest findings")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract impactful facts about religious bias in LLMs.")
    parser.add_argument("--analysis-dir", default="analysis", help="Directory containing analysis markdown files")
    parser.add_argument("--json-dir", default="json/3rd_pass_json", help="Directory containing JSON analysis files")
    parser.add_argument("--csv", default="csv/1st_pass_results.csv", help="CSV file with paper metadata")
    parser.add_argument("--pdf-dir", default="pdf", help="Directory containing original PDFs")
    parser.add_argument("--output", default="analysis/talk_facts.md", help="Output file")
    parser.add_argument("--format", choices=['markdown', 'json'], default='markdown', help="Output format")
    parser.add_argument("--model", default="gemini-3-pro-preview", help="Model for fact extraction")
    parser.add_argument("--months", type=int, default=24, help="Only include papers from last N months")
    parser.add_argument("--no-verify", action="store_true", help="Skip PDF verification step")
    
    args = parser.parse_args()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return
    
    print("=" * 60)
    print("Extracting Talk Facts: Religious Bias in LLMs")
    print("=" * 60)
    
    # Load data
    print("\nLoading analysis files...")
    analysis_files = load_analysis_files(args.analysis_dir)
    if not analysis_files:
        print(f"Error: No analysis files found in {args.analysis_dir}")
        return
    print(f"  Loaded: {', '.join(analysis_files.keys())}")
    
    print("\nLoading paper metadata...")
    csv_metadata = load_csv_metadata(args.csv)
    print(f"  Found {len(csv_metadata)} papers in CSV")
    
    print("\nLoading JSON analysis data...")
    papers = load_json_data(args.json_dir)
    print(f"  Loaded {len(papers)} analyzed papers")
    
    # Filter for recency
    print(f"\nFiltering for papers from last {args.months} months...")
    recent_papers = filter_recent_papers(papers, csv_metadata, args.months)
    print(f"  {len(recent_papers)} recent papers")
    
    # Extract facts
    facts = extract_facts(
        analysis_files, 
        recent_papers, 
        api_key, 
        args.model,
        args.pdf_dir if not args.no_verify else None,
        verify_with_pdf=not args.no_verify
    )
    
    if not facts:
        print("No facts extracted.")
        return
    
    print(f"\nExtracted {len(facts)} facts")
    
    # Format and save output
    output = format_output(facts, args.format)
    
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"\nFacts saved to {args.output}")
    
    # Save timestamped version
    versions_dir = os.path.join(os.path.dirname(args.output) or '.', 'versions')
    os.makedirs(versions_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(os.path.basename(args.output))[0]
    ext = os.path.splitext(args.output)[1]
    versioned_path = os.path.join(versions_dir, f"{base_name}_{timestamp}{ext}")
    with open(versioned_path, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"Versioned copy saved to {versioned_path}")
    
    # Summary
    verified = sum(1 for f in facts if f.get('verified', False))
    high_impact = sum(1 for f in facts if f.get('impact_score', 0) >= 4)
    print(f"\nSummary:")
    print(f"  Total facts: {len(facts)}")
    print(f"  Verified against PDF: {verified}")
    print(f"  High impact (4-5): {high_impact}")
    print("=" * 60)


if __name__ == "__main__":
    main()
