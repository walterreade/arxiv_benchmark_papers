# Religious Bias in LLMs — Paper Analysis Pipeline

A pipeline for downloading, analyzing, and summarizing academic papers from arXiv that relate to religious bias evaluation in Large Language Models (LLMs).

## Overview

This project provides tools to:
1. Download papers from arXiv based on search criteria related to bias in NLP/LLMs
2. Extract paper metadata and classify papers (1st pass)
3. Extract bias targets from LLM-related bias papers (2nd pass)
4. Perform deep-dive analysis on papers with religious bias components (3rd pass)
5. Generate summary reports, statistics, and daily updates

## Reports

| Report | Description |
|--------|-------------|
| [Religious Bias Research Summary](reports/Religious%20Bias%20Research%20Summary.md) | Summary of the state of religious bias measurement in LLMs |
| [Religious Bias Papers - Summaries](reports/Religious%20Bias%20Papers%20-%20Summaries.md) | Findings from each analyzed paper, in descending order  |
| [Religious Bias Papers - Statistics and Links](reports/Religious%20Bias%20Papers%20-%20Statistics%20and%20Links.md) | Statistical tables with counts of religious groups, models, benchmarks, etc., and links to papers sorted by citation count |
| [Religious Bias Papers - Interesting Findings](reports/Religious%20Bias%20Papers%20-%20Interesting%20Findings.md) | Extracted impactful facts for presentations |
| [LLM Bias Papers - Statistics](reports/LLM%20Bias%20Papers%20-%20Statistics.md) | Bias target distribution across all analyzed LLM-bias papers |
| [Religious Papers - Latest Daily Update](reports/daily_updates/20260820_daily_update.md) | Most recent papers analyzed |

## Claude Code Skills

This project includes [Claude Code](https://claude.ai/claude-code) skills that automate common research tasks.

### `/find-citations`

Given a claim or quote from the paper draft, searches the project's data sources to find the supporting paper and generates a BibTeX entry.

**Usage:** Type `/find-citations` followed by the claim text, e.g.:

```
/find-citations "Models disproportionately use Chain-of-Thought reasoning to justify attributing blame to the marginalized religious group."
```

**What it does:**
1. Searches `reports/Religious Bias Papers - Summaries.md`, `reports/Religious Bias Papers - Interesting Findings.md`, and `utility_files/llm_bias_papers.csv` for matching papers
2. Fetches full metadata from arxiv (authors, venue, year)
3. Generates a complete BibTeX entry

See [`.claude/skills/find-citations/SKILL.md`](.claude/skills/find-citations/SKILL.md) for the full procedure.

## Project Structure

```
├── scripts/                           # Python analysis scripts
│   ├── 1_classify_and_download_arxiv_papers.py
│   ├── 2_extract_paper_metadata.py
│   ├── 3_extract_bias_targets.py
│   ├── 4_extract_paper_details.py
│   ├── generate_full_analysis.py
│   ├── generate_daily_update.py
│   ├── generate_talk_facts.py
│   ├── analyze_bias_targets.py
│   ├── clean_up_pipeline_data.py
│   └── shared.py
├── json/                              # JSON analysis output
│   ├── 2_paper_metadata/
│   ├── 3_paper_bias_targets/
│   └── 4_religious_bias_analysis/
├── reports/                          # Generated markdown reports
│   ├── Religious Bias Research Summary.md
│   ├── Religious Bias Papers - Summaries.md
│   ├── Religious Bias Papers - Statistics and Links.md
│   ├── Religious Bias Papers - Interesting Findings.md
│   ├── daily_updates/                 # Daily update files (YYYYMMDD_daily_update.md)
│   └── versions/                      # Date-stamped copies of reports
├── utility_files/                     # CSV data and state files
│   ├── 1st_pass_results.csv
│   └── *.failures.csv
├── pdf/                               # Downloaded PDF papers
└── run_update.sh                      # Automated daily pipeline
```

## Pipeline

### Automated (recommended)

Run the full pipeline with:

```bash
./run_update.sh
```

This will download new papers, run all analysis passes, generate a daily update, upload PDFs to GCS, and commit/push changes.

To also regenerate the full analysis reports and talk facts:

```bash
./run_update.sh --full
```

### Manual Scripts

#### Step 1: `scripts/1_classify_and_download_arxiv_papers.py`
Queries recent CS papers from arXiv, classifies them with Gemini for bias in NLP/LLMs, and downloads qualifying papers.

#### Step 2: `scripts/2_extract_paper_metadata.py`
Extracts metadata from downloaded PDFs — determines whether each paper is LLM-related, bias-related, and faith/ethics-related.

#### Step 3: `scripts/3_extract_bias_targets.py`
Extracts bias targets from papers that are both LLM-related and bias-related.

#### Step 4: `scripts/4_extract_paper_details.py`
Performs deep-dive analysis on papers with religious bias targets — extracts religious groups studied, models tested, benchmark measurements, findings, and more.

#### Report Generation

```bash
# Generate full analysis reports (statistics, summaries, AI-generated research summary)
uv run python scripts/generate_full_analysis.py

# Generate interesting findings for presentations
uv run python scripts/generate_talk_facts.py

# Generate a daily update for specific JSON files
uv run python scripts/generate_daily_update.py --json-files file1.json file2.json
```

### Utility Scripts

- **`scripts/clean_up_pipeline_data.py`** — Validates pipeline data integrity and cleans up invalid/orphaned JSON files. Dry run by default; use `--apply` to execute changes.
- **`scripts/analyze_bias_targets.py`** — Analyzes bias target distributions across the corpus.

## Setup

1. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

## Requirements

- Python 3.10+
- Google Gemini API access
- Dependencies managed via `uv` (see `pyproject.toml`)
