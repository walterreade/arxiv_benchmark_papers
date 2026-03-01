# ArXiv Benchmark Papers Analysis

A pipeline for downloading, analyzing, and summarizing academic papers from arXiv that relate to religious bias evaluation in Large Language Models (LLMs).

## Overview

This project provides tools to:
1. Download papers from arXiv based on search criteria
2. Perform a first-pass analysis to identify faith/ethics-related papers
3. Perform a deep-dive second-pass analysis on relevant papers
4. Generate summary statistics and learnings from the analysis

## Project Structure

```
├── scripts/                    # Python analysis scripts
│   ├── download_arxiv_papers.py
│   ├── 1st_pass_analyze_papers.py
│   ├── 2nd_pass_analyze_papers.py
│   ├── 3rd_pass_analyze_papers.py
│   ├── generate_full_analysis.py
│   ├── check_lds_mentions.py
│   ├── generate_daily_update.py
│   └── run_daily_update.sh
├── json/                       # JSON analysis output
│   ├── 1st_pass_json/
│   ├── 2nd_pass_json/
│   └── 3rd_pass_json/
├── analysis/                   # Generated markdown reports
│   ├── benchmark_analysis.md
│   ├── benchmark_learnings.md
│   ├── benchmark_summary.md
│   ├── daily_updates/          # Timestamped daily update files
│   └── versions/               # Versioned copies with timestamps
├── csv/                        # CSV data files
│   ├── 1st_pass_results.csv
│   ├── 1st_pass_failures.csv
│   ├── 2nd_pass_failures.csv
│   └── 3rd_pass_failures.csv
└── pdf/                        # Downloaded PDF papers
```

## Scripts

### `scripts/download_arxiv_papers.py`
Queries the last 1000 CS papers from arXiv, classifies them with Gemini for bias in NLP/LLMs, and downloads qualifying papers.

### `scripts/1st_pass_analyze_papers.py`
Performs initial analysis on downloaded PDFs using the Gemini API to determine:
- Whether the paper is benchmark-related
- Whether it's LLM-related
- Whether it discusses bias
- Whether it's faith/ethics-related

**Output:** `1st_pass_results.csv`

### `scripts/2nd_pass_analyze_papers.py`
Extracts bias targets from papers that are both LLM-related and bias-related. Extracts:
- Bias targets with methodology descriptions
- Primary bias target

**Usage:**
```bash
uv run scripts/2nd_pass_analyze_papers.py [--rpm 20] [--workers 10] [--model gemini-3.1-pro-preview] [--reprocess]
```

**Output:** JSON files in `json/2nd_pass_json/`

### `scripts/3rd_pass_analyze_papers.py`
Performs deep-dive analysis on religion/faith aspects of bias papers. Extracts:
- Religious groups studied
- Models tested
- Benchmark measurements and findings
- Languages evaluated
- Response types (short/long)
- Religion component (major/minor focus)
- Base benchmarks used
- References cited
- Whether testing is continuous

**Usage:**
```bash
uv run scripts/3rd_pass_analyze_papers.py [--rpm 50] [--workers 10] [--model gemini-2.5-pro] [--reprocess]
```

**Output:** JSON files in `json/3rd_pass_json/`

### `scripts/generate_full_analysis.py`
Processes the JSON analysis files and generates markdown summaries.

**Usage:**
```bash
uv run scripts/generate_full_analysis.py
```

**Outputs:**
- `analysis/benchmark_analysis.md` - Statistical tables (religious groups, models, benchmarks, languages, etc.)
- `analysis/benchmark_learnings.md` - Individual paper entries with findings
- `analysis/benchmark_summary.md` - AI-generated summary of the state of religious bias measurement in LLMs

### `scripts/check_lds_mentions.py`
Utility script to check for Latter-day Saint/Mormon mentions in analyzed papers.

### `scripts/run_daily_update.sh`
Automated pipeline that runs the full analysis workflow:
1. Downloads new papers from arXiv
2. Runs 1st pass analysis
3. Runs 2nd pass analysis for qualifying papers
4. Generates a timestamped update file for newly analyzed papers

```bash
./scripts/run_daily_update.sh
```

### `scripts/generate_daily_update.py`
Helper script to generate timestamped update markdown files for specific papers.

### `scripts/extract_talk_facts.py`
Extracts impactful, quotable facts for talks/papers about religious bias in LLMs.

```bash
uv run python scripts/extract_talk_facts.py
```

**Features:**
- Extracts 15-20 high-impact facts from analysis files
- Filters for recent papers (default: last 24 months) to avoid stale information
- Verifies key facts against original PDFs for accuracy
- Categorizes facts (quantitative, surprising, bias patterns, methodology, gaps, trends)
- Outputs concise, presentation-ready statements

**Options:**
- `--months N` - Include papers from last N months (default: 24)
- `--no-verify` - Skip PDF verification (faster but less accurate)
- `--format json` - Output as JSON instead of markdown

## Output Files

| File | Description |
|------|-------------|
| `csv/1st_pass_results.csv` | Results from initial paper screening |
| `csv/1st_pass_failures.csv` | Papers that failed first-pass analysis |
| `json/2nd_pass_json/` | Bias target extraction results for each paper |
| `csv/2nd_pass_failures.csv` | Papers that failed second-pass analysis |
| `json/3rd_pass_json/` | Religion deep-dive analysis for each paper |
| `csv/3rd_pass_failures.csv` | Papers that failed third-pass analysis |
| `analysis/benchmark_analysis.md` | Summary tables with counts of religious groups, models, benchmarks, etc. |
| `analysis/benchmark_learnings.md` | Detailed findings from each analyzed paper |
| `analysis/benchmark_summary.md` | AI-generated comprehensive summary of the field |
| `analysis/daily_updates/` | Timestamped update files from `run_daily_update.sh` runs |
| `analysis/versions/` | Versioned copies of analysis files with timestamps |
| `analysis/talk_facts.md` | Extracted impactful facts for presentations |

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
