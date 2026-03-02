#!/usr/bin/env python3
import json
import os
import glob
from collections import Counter
from pathlib import Path
import sys
import requests
import time
from datetime import datetime, timedelta

def fetch_citation_counts(arxiv_ids: list[str]) -> dict:
    """Fetch citation counts from Semantic Scholar API using arXiv IDs, caching results for 7 days."""
    if not arxiv_ids:
        return {}
        
    cache_file = Path("citations_cache.json")
    cache = {}
    if cache_file.exists():
        try:
            with open(cache_file, "r") as f:
                cache = json.load(f)
        except Exception:
            pass

    now = datetime.now()
    import re
    
    citations = {}
    ids_to_fetch = []
    
    # regex to strip version suffix (e.g., "v1", "v2") from the end of string
    version_pattern = re.compile(r'v\d+$')

    for original_aid in arxiv_ids:
        # Some IDs might include a version suffix like v1, v2
        clean_aid = version_pattern.sub('', original_aid)
        
        if clean_aid in cache:
            cached_data = cache[clean_aid]
            try:
                cached_time = datetime.fromisoformat(cached_data["timestamp"])
                if now - cached_time < timedelta(days=7):
                    citations[original_aid] = cached_data["count"]
                    continue
            except Exception:
                pass
        ids_to_fetch.append({"original": original_aid, "clean": clean_aid})

    if not ids_to_fetch:
        return citations
        
    url = "https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount"
    
    # Process in batches of 100
    batch_size = 100
    for i in range(0, len(ids_to_fetch), batch_size):
        batch = ids_to_fetch[i:i + batch_size]
        payload = {"ids": [f"arXiv:{item['clean']}" for item in batch]}
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(url, json=payload, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    for j, paper_data in enumerate(data):
                        item = batch[j]
                        original_aid = item['original']
                        clean_aid = item['clean']
                        
                        if paper_data is not None and 'citationCount' in paper_data:
                            count = paper_data['citationCount']
                            citations[original_aid] = count
                            cache[clean_aid] = {"count": count, "timestamp": now.isoformat()}
                        else:
                            citations[original_aid] = 0
                            cache[clean_aid] = {"count": 0, "timestamp": now.isoformat()}
                    break # Success, break out of retry loop
                elif response.status_code == 429:
                    if attempt < max_retries - 1:
                        time.sleep((attempt + 1) * 3) # Wait 3s, 6s...
                        continue
                    else:
                        for item in batch:
                            citations[item['original']] = 0
                else:
                    for item in batch:
                        citations[item['original']] = 0
                    break # Don't retry other errors
            except Exception:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                else:
                    for item in batch:
                        citations[item['original']] = 0
                    
        # Rate limit delay for unauthenticated endpoint
        time.sleep(1.5)
        
    try:
        with open(cache_file, "w") as f:
            json.dump(cache, f, indent=2)
    except Exception:
        pass
        
    return citations

# Setup imports
script_dir = Path(__file__).parent
if script_dir.name != 'scripts':
    sys.path.insert(0, str(script_dir / 'scripts'))

import scripts.analyze_bias_targets as abt
import scripts.generate_full_analysis as gfa

def main():
    json_dir_1st = script_dir / 'json' / '1st_pass_json'
    json_dir_2nd = script_dir / 'json' / '2nd_pass_json'
    json_dir_3rd = script_dir / 'json' / '3rd_pass_json'
    
    restricted_paper_ids = []
    
    # 1. Find restricted papers (is_llm_related and is_bias_related are True)
    for filepath in glob.glob(str(json_dir_1st / '*.json')):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            if data.get('is_llm_related') and data.get('is_bias_related'):
                restricted_paper_ids.append(Path(filepath).stem)
        except Exception:
            pass
            
    out_lines = [
        "# Full Pipeline Analysis",
        "",
        f"**Count of LLM-Bias papers:** {len(restricted_paper_ids)}",
        "<!-- SUMMARY_COUNTS -->",
        ""
    ]
    
    # 2. Bias targets statistics from 2nd pass
    papers_2nd_data = []
    all_targets = []
    singleton_targets = []
    primary_targets = Counter()
    religious_bias_paper_ids = set()
    
    for paper_id in restricted_paper_ids:
        try:
            filepath = json_dir_2nd / f"{paper_id}.json"
            if not filepath.exists():
                continue
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if 'bias_targets' not in data:
                continue
            
            raw_targets = data['bias_targets']
            normalized = []
            for entry in raw_targets:
                if isinstance(entry, dict):
                    normalized.append(abt.normalize_target(entry.get('target', '')))
                else:
                    normalized.append(abt.normalize_target(entry))
                    
            primary = data.get('primary_bias_target', '')
            if primary:
                primary = abt.normalize_target(primary)
                
            papers_2nd_data.append({
                'arxiv_id': paper_id,
                'title': data.get('title', ''),
                'normalized_targets': normalized,
                'primary_bias_target': primary,
                'count': len(normalized)
            })
            
            all_targets.extend(normalized)
            if len(normalized) == 1:
                singleton_targets.append(normalized[0])
            if primary:
                primary_targets[primary] += 1
                
            if "Religious bias" in normalized:
                religious_bias_paper_ids.add(paper_id)
                
        except Exception as e:
            pass

    all_counter = Counter(all_targets)
    singleton_counter = Counter(singleton_targets)
    
    out_lines.append("## Bias Targets Measured (LLM-Bias papers)")
    out_lines.append(gfa.generate_markdown_table(all_counter, "Top 25 Bias Targets", "Target", "Count", 25, len(restricted_paper_ids)))


    
    focused_counter = Counter()
    for paper in papers_2nd_data:
        targets = set(paper['normalized_targets'])
        primary = paper['primary_bias_target']
        is_exclusive = len(targets) == 1
        for t in targets:
            if is_exclusive or t == primary:
                focused_counter[t] += 1
                
    out_lines.append(gfa.generate_markdown_table(focused_counter, "Focus Analysis (Primary or Exclusive focus)", "Target", "Count", 25, len(restricted_paper_ids)))
    
    # 3. Analyze how religious bias has been measured
    out_lines.append("## Religious Bias Measurement (LLM-Bias papers)")
    
    papers_3rd_data = []
    papers_with_religious_primary = []
    
    for paper_id in restricted_paper_ids:
        try:
            filepath = json_dir_3rd / f"{paper_id}.json"
            if not filepath.exists():
                continue
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            component = data.get('religion_component', '').lower()
            if component in ('major', 'minor'):
                papers_3rd_data.append(data)
                religious_bias_paper_ids.add(paper_id)
                
                # Check 2nd pass target
                for p2 in papers_2nd_data:
                    if p2['arxiv_id'] == paper_id:
                        if p2['primary_bias_target'] == "Religious bias":
                            papers_with_religious_primary.append(data)
                        break
                
        except Exception:
            pass

    # Insert counts at the top of the report
    try:
        summary_idx = out_lines.index("<!-- SUMMARY_COUNTS -->")
        out_lines[summary_idx] = f"**Count of papers measuring religious bias:** {len(papers_3rd_data)}\n**Count of papers where religious bias is the primary focus:** {len(papers_with_religious_primary)}"
    except ValueError:
        pass

    if papers_3rd_data:

        out_lines.append(gfa.generate_markdown_table(gfa.count_religious_groups(papers_3rd_data), "Religious Groups", "Group", "Count", 25, len(papers_3rd_data)))
        out_lines.append(gfa.generate_markdown_table(gfa.count_models_tested(papers_3rd_data), "Models Tested", "Model", "Count", 25, len(papers_3rd_data)))
        out_lines.append(gfa.generate_markdown_table(gfa.count_base_benchmarks(papers_3rd_data), "Base Benchmarks", "Benchmark", "Count", 25, len(papers_3rd_data)))
        out_lines.append(gfa.generate_markdown_table(gfa.count_languages_evaluated(papers_3rd_data), "Languages Evaluated", "Language", "Count", 25, len(papers_3rd_data)))
        out_lines.append(gfa.generate_markdown_table(gfa.count_response_type(papers_3rd_data), "Response Type", "Type", "Count", None, len(papers_3rd_data)))
        out_lines.append(gfa.generate_markdown_table(gfa.count_continuous_testing(papers_3rd_data), "Continuous Testing", "Status", "Count", None, len(papers_3rd_data)))
        out_lines.append(gfa.generate_markdown_table_references(gfa.count_references(papers_3rd_data), "Most Cited References in Religious Bias Papers", 25))
    
    out_lines.append("## Papers Primarily Measuring Religious Bias")
    
    religious_primary_info = []
    for paper in papers_with_religious_primary:
        paper_id = paper.get('filename', '').replace('.pdf', '')
        if not paper_id:
            paper_id = paper.get('_filename', '').replace('.pdf', '')
        title = paper.get('title', 'Unknown Title')
        url = f"https://arxiv.org/pdf/{paper_id}"
        religious_primary_info.append((paper_id, title, url))
        
    # Fetch citations
    primary_citations = fetch_citation_counts([p[0] for p in religious_primary_info])
    
    # Sort by citation count (descending), then title
    religious_primary_info.sort(key=lambda x: (-primary_citations.get(x[0], 0), x[1]))
    
    for pid, title, url in religious_primary_info:
        cites = primary_citations.get(pid, 0)
        out_lines.append(f"- {pid} (citations: {cites}): [{title}]({url})")
        
    out_lines.append("")
    out_lines.append("## All Papers Measuring Religious Bias")
    
    religious_bias_papers_info = []
    # Collect titles
    for paper_id in religious_bias_paper_ids:
        title = "Unknown Title"
        # Try finding title in 3rd pass first
        for p3 in papers_3rd_data:
            if p3.get("filename", "").startswith(paper_id) or p3.get("_filename", "").startswith(paper_id):
                title = p3.get("title", title)
                break
        
        if title == "Unknown Title":
            for p2 in papers_2nd_data:
                if p2['arxiv_id'] == paper_id:
                    title = p2['title']
                    break
                    
        url = f"https://arxiv.org/pdf/{paper_id}"
        religious_bias_papers_info.append((paper_id, title, url))
        
    # Fetch citations
    bias_citations = fetch_citation_counts([p[0] for p in religious_bias_papers_info])
    
    # Sort by citation count (descending), then title
    religious_bias_papers_info.sort(key=lambda x: (-bias_citations.get(x[0], 0), x[1]))
        
    for pid, title, url in religious_bias_papers_info:
        cites = bias_citations.get(pid, 0)
        out_lines.append(f"- {pid} (citations: {cites}): [{title}]({url})")
        
    out_md_path = script_dir / 'full_pipeline_analysis.md'
    with open(out_md_path, 'w') as f:
        f.write("\n".join(out_lines))
        
    print(f"Done! Analysis saved to {out_md_path}")

if __name__ == '__main__':
    main()
