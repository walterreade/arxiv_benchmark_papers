# arXiv AI Benchmark Corpus & Religious-Bias Research Pipeline

Personal research database indexing **all AI benchmark papers on arXiv** across modalities and domains (language, vision, audio, video, multimodal, agents, robotics, code, tabular, and scientific/medical/legal/industrial AI) to identify gaps in industry evaluation coverage, while preserving the longitudinal **Religious Bias in LLMs** downstream module.

Design specification: [docs/designs/arxiv_ai_benchmarks_expansion.md](docs/designs/arxiv_ai_benchmarks_expansion.md)

## Architecture Summary

* **Corpus Boundary:** Includes papers whose contribution **introduces, extends, audits/critiques, or surveys** benchmarks, datasets, or evaluation methodologies. Empirical model papers (`uses_only`) are excluded from the general benchmark corpus unless routed orthogonally into the religious-bias module (`is_llm_bias_ethics_religion`).
* **Model Split (`google-genai >= 3.2.0`):**
  * **Stage 1 Abstract Triage (`gemini-3.8-flash`, default):** Batched structured JSON classification (`20` papers/request, `thinking_budget=0`, 4 orthogonal questions) via `arxiv-bench triage`. Optional `--backend decisions` (`gemini-decision-1`) remains available with automatic Flash fallback (`--fallback-to-flash`). Per-paper provenance is tracked in `triage_assessments.model_id`.
  * **Stage 2 Native Multimodal PDF Extraction (`gemini-3.8-flash`):** Single-pass inline `Part.from_bytes` (`<20 MB`, Files API fallback `>=20 MB`) into strict Pydantic schemas + structured Evidence Cards.
  * **Stage 3 On-Demand Gap-Rubric Sweeps (`gemini-decision-1`):** `POST /v1beta/decisions` over stored Evidence Cards + trimmed text (`arxiv-bench score`).
  * **Semantic Scholar Batch Graph API:** 500-paper batch citation, venue, and reference graph enrichment.
* **Storage Topology:**
  * **Git repo (NVMe `~/arxiv_benchmark_papers`):** Source code, migrations, YAML rubrics, tests, and curated Markdown reports (`reports/` and `README.md`).
  * **Operational SQLite (NVMe `~/.local/share/arxiv_bench/benchmarks.db`):** WAL-mode SQLite with mandatory startup NFS guard, normalized facet junction tables, external-content FTS5 (`papers_fts`), `decision_scores`, and `zstd`-compressed extracted text.
  * **Ephemeral PDF Staging & GCS Archive:** Bounded 10 GB NVMe staging deleted immediately after archival to `gs://inversion/pdf/<YYMM>/<safe_id>.pdf`; automated `VACUUM INTO` + `zstd` backups to `gs://inversion/backups/sqlite/` and `/mnt/filestore/.../backups/`.

## Quick Start (Local NVMe)

```bash
cd ~/arxiv_benchmark_papers
uv sync --python 3.12 --dev
uv run arxiv-bench --help
```

Configure `.env` (`chmod 600`):
```bash
GOOGLE_API_KEY=...
# Optional:
# S2_API_KEY=...
# GCP_REQUESTER_PAYS_PROJECT=kaggle-comps-162117
# ARXIV_BENCH_DB_PATH=~/.local/share/arxiv_bench/benchmarks.db
```

## Core CLI Commands

```bash
# Phase 1: Read-only idempotent legacy migration from /mnt/filestore
uv run arxiv-bench migrate-legacy --legacy-root /mnt/filestore/walter/lds_projects/arxiv_benchmark_papers

# Phase 2: Religious-bias parity check
uv run arxiv-bench religion full-report --output-dir /tmp/parity_check

# Phase 3: Stage 0 calibration gate (verify live /v1beta/decisions RPM & thresholds)
uv run arxiv-bench calibrate --sample-size 300

# Sync weekly snapshot or daily Atom delta
uv run arxiv-bench sync --snapshot --mode backfill
uv run arxiv-bench sync --mode daily

# Preview volume/cost and run pipeline stages
uv run arxiv-bench triage --dry-run
uv run arxiv-bench extract --dry-run
uv run arxiv-bench enrich
uv run arxiv-bench score --rubric rubrics/gap_analysis_core_v1.yaml --dry-run

# Exploratory gap analysis
uv run arxiv-bench search "SWE-bench" --modality code-software --format table
uv run arxiv-bench matrix --rows modality --cols domain --format md
uv run arxiv-bench alias list
uv run arxiv-bench alias merge <source_id> <target_id>

# Operational health & backups
uv run arxiv-bench status
uv run arxiv-bench backup --verify-restore
```

## Preserved Religious-Bias Reports

* `uv run arxiv-bench religion extract`
* `uv run arxiv-bench religion daily-update --run-id <run_id>`
* `uv run arxiv-bench religion full-report`
* `uv run arxiv-bench religion bias-targets`
* `uv run arxiv-bench religion non-bias-report`
* `uv run arxiv-bench religion wider-net`
* `uv run arxiv-bench religion talk-facts`

## Testing & Linting

```bash
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run pytest -v --cov=arxiv_bench --cov-report=term-missing
```
