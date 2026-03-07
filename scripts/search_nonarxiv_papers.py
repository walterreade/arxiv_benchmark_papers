#!/usr/bin/env python3
"""
Search for peer-reviewed journal papers on religious bias in LLMs
that are NOT on arXiv, using the OpenAlex API. Then filter them with
Gemini to keep only those that genuinely deal with religious bias
in LLMs / NLP / AI.

Usage:
    uv run scripts/search_nonarxiv_papers.py [--min-citations N] [--output FILE]

The script:
  1. Searches OpenAlex for papers matching religious bias + LLM keywords.
  2. Filters to journal articles only (excludes preprints/repositories).
  3. Excludes papers already in the local JSON dataset.
  4. Uses Gemini to classify each candidate and keep only relevant papers.
  5. Outputs results sorted by citation count, with DOI links.
"""

import argparse
import glob
import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()
# Suppress the dual API key warning
if os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
    del os.environ["GEMINI_API_KEY"]

from google import genai
from google.genai import types


OPENALEX_WORKS_URL = "https://api.openalex.org/works"
ARXIV_SOURCE_ID = "S4306400194"  # OpenAlex ID for arXiv
GEMINI_MODEL = "gemini-3-flash-preview"
GEMINI_BATCH_SIZE = 20  # Papers per Gemini call

# Multiple search queries to cast a wide net.
# OpenAlex "search" uses full-text + title + abstract matching.
SEARCH_QUERIES = [
    "religious bias large language model",
    "religion bias LLM",
    "religious stereotypes language model",
    "Islamophobia AI language model",
    "anti-Muslim bias NLP",
    "religious fairness machine learning",
    "faith bias generative AI",
    "religious discrimination natural language processing",
    "religion stereotypes NLP bias",
    "Islam bias GPT",
    "Hindu Muslim bias text generation",
    "religious hate speech detection",
]

# OpenAlex work types to search (article = journal article, review = review paper)
ARTICLE_TYPES = ["article", "review"]

FILTER_PROMPT = """\
You are an expert academic researcher specializing in bias and fairness in AI/NLP.

I will give you a numbered list of papers (title + abstract). For each paper,
decide whether it **primarily or substantially** deals with **religious bias,
religious stereotypes, or religious fairness in Large Language Models (LLMs),
Natural Language Processing (NLP), text generation, or AI systems**.

Papers that qualify include those that:
- Measure, detect, or benchmark religious bias in language models or AI
- Propose methods to mitigate religious bias in NLP/AI
- Study how LLMs or text generation systems represent religions
- Analyze religious stereotypes in word embeddings or language models
- Detect religious hate speech using NLP/ML methods
- Examine fairness across religions in AI decision-making systems

Papers that do NOT qualify include those that:
- Only mention religion as one of many demographic variables without focusing on it
- Are about religion or bias in general but NOT about AI/NLP/LLMs
- Are about AI/ML but only mention religious bias in passing
- Are about social media, public health, COVID, or policy without an AI/NLP focus
- Are about hate speech detection without a specific religious focus

Return ONLY a JSON object with a single key "relevant_ids" containing an array
of the ID numbers (integers) of papers that qualify. If none qualify, return
{"relevant_ids": []}.

Here are the papers:

"""


def reconstruct_abstract(inverted_index: dict | None) -> str:
    """Reconstruct abstract text from OpenAlex's inverted abstract index."""
    if not inverted_index:
        return ""

    # Build a position -> word mapping
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))

    # Sort by position and join
    word_positions.sort(key=lambda x: x[0])
    return " ".join(w for _, w in word_positions)


def get_existing_paper_titles(json_dirs: list[Path]) -> set[str]:
    """Collect titles from existing JSON files to avoid duplicates."""
    titles = set()
    for json_dir in json_dirs:
        for filepath in glob.glob(str(json_dir / "*.json")):
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                title = data.get("title", "").strip().lower()
                if title:
                    titles.add(title)
            except Exception:
                pass
    return titles


def load_filter_cache(cache_path: Path) -> dict:
    """Load the Gemini filter cache from disk."""
    if cache_path.exists():
        try:
            with open(cache_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_filter_cache(cache_path: Path, cache: dict):
    """Save the Gemini filter cache to disk."""
    with open(cache_path, "w") as f:
        json.dump(cache, f, indent=2)


def search_openalex(
    query: str, article_type: str = "article", per_page: int = 100, max_pages: int = 3
) -> list[dict]:
    """
    Search OpenAlex for works matching a query.
    Filters:
      - type: article or review (peer-reviewed)
      - primary_location.source.id: NOT arXiv
      - from_publication_date: 2017-01-01 (modern LLM era)
    """
    all_results = []

    for page in range(1, max_pages + 1):
        params = {
            "search": query,
            "filter": (
                f"type:{article_type},"
                f"primary_location.source.id:!{ARXIV_SOURCE_ID},"
                "from_publication_date:2017-01-01"
            ),
            "sort": "cited_by_count:desc",
            "per_page": per_page,
            "page": page,
            "mailto": "research@example.com",  # polite pool
        }

        try:
            response = requests.get(OPENALEX_WORKS_URL, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if not results:
                    break
                all_results.extend(results)

                # Stop if we've gotten all results
                total = data.get("meta", {}).get("count", 0)
                if page * per_page >= total:
                    break
            else:
                print(f"  Warning: HTTP {response.status_code} for query '{query}' page {page}")
                break
        except Exception as e:
            print(f"  Error: {e}")
            break

        time.sleep(0.5)  # Be polite with rate limits

    return all_results


def extract_paper_info(work: dict) -> dict:
    """Extract relevant information from an OpenAlex work object."""
    # Get DOI
    doi = work.get("doi", "")
    if doi and doi.startswith("https://doi.org/"):
        doi_short = doi.replace("https://doi.org/", "")
    else:
        doi_short = doi or ""

    # Get primary source (journal name)
    primary_location = work.get("primary_location", {}) or {}
    source = primary_location.get("source", {}) or {}
    journal = source.get("display_name", "Unknown Journal")

    # Get the URL for the paper (prefer DOI, then OA URL)
    url = doi or ""
    oa_url = (work.get("open_access", {}) or {}).get("oa_url", "")
    if not url and oa_url:
        url = oa_url

    # Reconstruct abstract from inverted index
    abstract_inverted = work.get("abstract_inverted_index", None)
    abstract = reconstruct_abstract(abstract_inverted)

    # Check if it has any arXiv location
    has_arxiv = False
    for loc in work.get("locations", []):
        loc_source = (loc or {}).get("source", {}) or {}
        if loc_source.get("id", "").endswith(ARXIV_SOURCE_ID):
            has_arxiv = True
            break

    return {
        "title": work.get("title", "Unknown Title"),
        "doi": doi_short,
        "url": url,
        "journal": journal,
        "year": work.get("publication_year", 0),
        "citations": work.get("cited_by_count", 0),
        "has_arxiv": has_arxiv,
        "openalex_id": work.get("id", ""),
        "abstract": abstract,
    }


def filter_with_gemini(
    papers: list[dict], cache: dict, cache_path: Path, max_retries: int = 3
) -> list[dict]:
    """
    Use Gemini to filter papers, keeping only those about religious bias in LLMs.
    Papers are processed in batches. Results are cached by OpenAlex ID.
    """
    client = genai.Client()

    # Separate cached vs uncached papers
    uncached_papers = []
    cached_relevant_ids = set()

    for p in papers:
        oa_id = p["openalex_id"]
        if oa_id in cache:
            if cache[oa_id]:  # True = relevant
                cached_relevant_ids.add(oa_id)
        else:
            uncached_papers.append(p)

    print(f"\n  Gemini filter: {len(papers)} total, "
          f"{len(papers) - len(uncached_papers)} cached, "
          f"{len(uncached_papers)} to classify")

    if not uncached_papers:
        return [p for p in papers if p["openalex_id"] in cached_relevant_ids]

    # Process uncached papers in batches
    newly_relevant_ids = set()
    total_batches = (len(uncached_papers) + GEMINI_BATCH_SIZE - 1) // GEMINI_BATCH_SIZE

    for batch_idx in range(total_batches):
        start = batch_idx * GEMINI_BATCH_SIZE
        end = min(start + GEMINI_BATCH_SIZE, len(uncached_papers))
        batch = uncached_papers[start:end]

        print(f"  Batch {batch_idx + 1}/{total_batches} "
              f"({len(batch)} papers)...", end="", flush=True)

        # Build the prompt with numbered papers
        paper_text = ""
        for i, p in enumerate(batch, 1):
            title = p["title"] or "Unknown Title"
            abstract = p.get("abstract", "")
            if abstract:
                # Truncate to ~500 chars
                abstract = abstract[:500] + ("..." if len(abstract) > 500 else "")
            else:
                abstract = "(no abstract available)"
            paper_text += f"\n{i}. Title: {title}\n   Abstract: {abstract}\n"

        prompt = FILTER_PROMPT + paper_text

        # Call Gemini with retry
        relevant_batch_indices = set()
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=[types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=prompt)],
                    )],
                    config=types.GenerateContentConfig(
                        temperature=0.0,
                        max_output_tokens=1024,
                    ),
                )

                response_text = response.text.strip()

                # Clean up response if wrapped in markdown
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.startswith("```"):
                    response_text = response_text[3:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()

                result = json.loads(response_text)
                relevant_batch_indices = set(result.get("relevant_ids", []))
                break  # Success

            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str or "resource exhausted" in error_str:
                    wait = (attempt + 1) * 5
                    print(f" rate limited, waiting {wait}s...", end="", flush=True)
                    time.sleep(wait)
                elif attempt < max_retries - 1:
                    print(f" error ({e}), retrying...", end="", flush=True)
                    time.sleep(2)
                else:
                    print(f" FAILED: {e}")
                    # Mark all as not relevant on failure to be safe
                    break

        # Update cache with results
        for i, p in enumerate(batch, 1):
            oa_id = p["openalex_id"]
            is_relevant = i in relevant_batch_indices
            cache[oa_id] = is_relevant
            if is_relevant:
                newly_relevant_ids.add(oa_id)

        relevant_count = len(relevant_batch_indices)
        print(f" {relevant_count}/{len(batch)} relevant")

        # Save cache after each batch
        save_filter_cache(cache_path, cache)

        # Rate limit between batches
        time.sleep(1)

    all_relevant_ids = cached_relevant_ids | newly_relevant_ids
    print(f"  Total relevant papers: {len(all_relevant_ids)}")

    return [p for p in papers if p["openalex_id"] in all_relevant_ids]


def main():
    parser = argparse.ArgumentParser(
        description="Search for peer-reviewed papers on religious bias in LLMs (non-arXiv)"
    )
    parser.add_argument(
        "--min-citations", type=int, default=0,
        help="Minimum citation count to include (default: 0)"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output markdown file path (default: print to stdout)"
    )
    parser.add_argument(
        "--max-pages", type=int, default=3,
        help="Max pages per search query (default: 3, 100 results/page)"
    )
    parser.add_argument(
        "--no-gemini", action="store_true",
        help="Skip Gemini filtering (output all OpenAlex results)"
    )
    args = parser.parse_args()

    script_dir = Path(__file__).parent.parent
    json_dirs = [
        script_dir / "json" / "1st_pass_json",
        script_dir / "json" / "2nd_pass_json",
        script_dir / "json" / "3rd_pass_json",
    ]
    cache_path = script_dir / "gemini_filter_cache.json"

    # Load existing paper titles for dedup
    print("Loading existing paper titles...")
    existing_titles = get_existing_paper_titles(json_dirs)
    print(f"  Found {len(existing_titles)} existing papers in local dataset.")

    # Load Gemini filter cache
    filter_cache = load_filter_cache(cache_path)
    print(f"  Loaded {len(filter_cache)} cached Gemini classifications.")

    # Search across all queries and article types
    seen_ids = set()
    all_papers = []
    total_searches = len(SEARCH_QUERIES) * len(ARTICLE_TYPES)
    search_num = 0

    for article_type in ARTICLE_TYPES:
        for query in SEARCH_QUERIES:
            search_num += 1
            print(f"\n[{search_num}/{total_searches}] ({article_type}) '{query}'...")
            results = search_openalex(query, article_type=article_type, max_pages=args.max_pages)
            new_count = 0

            for work in results:
                oa_id = work.get("id", "")
                if oa_id in seen_ids:
                    continue
                seen_ids.add(oa_id)

                info = extract_paper_info(work)

                # Skip if it has an arXiv version (we already have those)
                if info["has_arxiv"]:
                    continue

                # Skip if title matches an existing paper
                title_lower = (info["title"] or "").strip().lower()
                if title_lower in existing_titles:
                    continue

                # Skip below citation threshold
                if info["citations"] < args.min_citations:
                    continue

                all_papers.append(info)
                new_count += 1

            print(f"  Found {len(results)} results, {new_count} new unique papers")

    # Deduplicate by title (case-insensitive)
    deduped_papers = []
    seen_titles = set()
    for p in all_papers:
        t = (p["title"] or "").strip().lower()
        if t not in seen_titles:
            seen_titles.add(t)
            deduped_papers.append(p)

    print(f"\n{'='*60}")
    print(f"Total unique non-arXiv papers from OpenAlex: {len(deduped_papers)}")
    print(f"{'='*60}")

    # Filter with Gemini
    if args.no_gemini:
        final_papers = deduped_papers
        print("Skipping Gemini filtering (--no-gemini)")
    else:
        print("\nFiltering with Gemini...")
        final_papers = filter_with_gemini(deduped_papers, filter_cache, cache_path)

    # Sort by citation count descending
    final_papers.sort(key=lambda x: (-x["citations"], x["title"] or ""))

    print(f"\n{'='*60}")
    print(f"Final papers after filtering: {len(final_papers)}")
    print(f"{'='*60}\n")

    # Format output
    lines = [
        "# Non-arXiv Peer-Reviewed Papers on Religious Bias in LLMs",
        "",
        f"**Total papers found:** {len(final_papers)}",
        f"**Search date:** {time.strftime('%Y-%m-%d')}",
        f"**Minimum citations:** {args.min_citations}",
        f"**Filtered by:** Gemini ({GEMINI_MODEL})" if not args.no_gemini else "**Filtered by:** None",
        "",
        "---",
        "",
    ]

    for p in final_papers:
        title = p["title"] or "Unknown Title"
        cites = p["citations"]
        journal = p["journal"]
        year = p["year"]
        url = p["url"]

        if url:
            line = f"- [{title}]({url}) (citations: {cites}) — *{journal}* ({year})"
        else:
            line = f"- {title} (citations: {cites}) — *{journal}* ({year})"

        lines.append(line)

    output_text = "\n".join(lines) + "\n"

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w") as f:
            f.write(output_text)
        print(f"Results saved to {output_path}")
    else:
        print(output_text)


if __name__ == "__main__":
    main()
