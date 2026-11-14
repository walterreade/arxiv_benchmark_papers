---
name: find-citations
description: Find the reference paper that supports a specific claim from the paper draft and generate a BibTeX entry.
argument-hint: <claim text>
allowed-tools: [Read, Bash, WebFetch]
---

# Find Citation

Given a claim or quote from a paper draft, find the source paper that supports it across both the expanded all-AI benchmark corpus and the religious-bias corpus, then produce a verified BibTeX entry.

## Input

The user provides a claim or question that needs a citation.

## Procedure

### Step 1: Query local NVMe SQLite FTS5 via `arxiv-bench`

Run sanitized full-text searches using `uv run arxiv-bench search` (which safely handles hyphenated benchmark names like `SWE-bench` and `MMLU-Pro`):

```bash
# Search across all AI benchmark papers and religious-bias papers
uv run arxiv-bench search "<claim keywords>" --limit 15 --format json

# Scope strictly to the religious-bias corpus when writing a religious-bias draft
uv run arxiv-bench search "<claim keywords>" --religion-only --limit 15 --format json

# Generate BibTeX entries directly for top matches
uv run arxiv-bench search "<claim keywords>" --limit 5 --format bibtex
```

Run multiple keyword variations in parallel (distinctive metrics, benchmark names, model names, or phenomenon terms).

If additional qualitative context is needed for religious-bias claims, fall back to grepping:
1. **`reports/Religious Bias Papers - Summaries.md`**
2. **`reports/Religious Bias Papers - Interesting Findings.md`**

### Step 2: Identify the best match

Compare candidate papers returned from SQLite (`title`, `published_date`, `venue`, `citation_count`, `evidence_card`, and religious-bias findings):
- Does the paper's summary or Evidence Card describe the same phenomenon?
- Do quantitative details (percentages, models, benchmarks) match?
- Is the methodology consistent with the claim?

Report to the user:
- The paper title, arXiv link, venue, and citation count
- The relevant excerpt from the Evidence Card or summary supporting the claim
- Confidence level and reasoning

### Step 3: Fetch full author list if needed

Use `WebFetch` on `https://arxiv.org/abs/<arxiv_id>` only if full author names or DOI are missing from the generated BibTeX entry.

### Step 4: Output

Present:
1. The identified paper (title, authors, arXiv link)
2. The supporting evidence excerpt
3. The complete BibTeX entry as a code block
