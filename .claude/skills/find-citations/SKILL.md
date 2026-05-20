---
name: find-citations
description: Find the reference paper that supports a specific claim from the paper draft and generate a BibTeX entry.
argument-hint: <claim text>
allowed-tools: [Read, Bash, WebFetch]
---

# Find Citation

Given a claim or quote from the paper draft, find the source paper that supports it and produce a BibTeX entry.

## Input

The user provides a claim — typically a sentence or phrase from `paper_draft.md` that needs a citation.

## Procedure

### Step 1: Search project data sources

Search these files for content matching the claim's key concepts (use grep with multiple relevant keywords):

1. **`reports/Religious Bias Papers - Summaries.md`** — The richest source. Each entry has a paper title, arxiv link, date, and detailed findings. Search for keywords from the claim (e.g., "Chain-of-Thought", "ambiguous", "stereotype", "bias score").

2. **`reports/Religious Bias Papers - Interesting Findings.md`** — Curated findings with verification status and source paper links. Good for specific quantitative claims.

3. **`utility_files/llm_bias_papers.csv`** — Contains ~17K paper titles with arxiv IDs. Columns: `paper_id`, `latest_date`, `title`. Search titles for topic keywords.

Run multiple grep searches in parallel with different keyword combinations extracted from the claim. Cast a wide net — try both specific phrases and individual distinctive terms.

### Step 2: Identify the best match

From the search results, identify the paper whose findings most closely match the claim. Consider:
- Does the paper's summary describe the same phenomenon?
- Do the quantitative details match (numbers, percentages, model names)?
- Is the methodology consistent with what the claim describes?

Report to the user:
- The paper title and arxiv link
- The relevant excerpt from the summaries that supports the claim
- Your confidence level and reasoning

### Step 3: Fetch metadata from arxiv

Use WebFetch on the arxiv abstract page (`https://arxiv.org/abs/XXXX.XXXXX`) to get:
- Full author list
- Publication year
- Conference/venue (if published)
- DOI (if available)

### Step 4: Generate BibTeX

Produce a complete BibTeX entry. Use `@inproceedings` for conference papers, `@article` for journal papers, or `@misc` for preprints. Format:

```bibtex
@inproceedings{firstauthor_lastname_year_keyword,
  title={Full Paper Title},
  author={Last1, First1 and Last2, First2 and ...},
  booktitle={Conference Name},
  year={YYYY}
}
```

Use the first author's lowercase last name, the year, and a short keyword from the title as the citation key (e.g., `turpin2023language`).

## Output

Present:
1. The identified paper (title, authors, arxiv link)
2. The supporting evidence from the project's summaries
3. The BibTeX entry as a code block
