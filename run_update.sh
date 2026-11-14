#!/usr/bin/env bash
set -euo pipefail

# Daily automated update for the all-arXiv AI benchmark corpus and religious-bias module.
# Runs from local NVMe (~/arxiv_benchmark_papers) and commits only reports/ and README.md.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

export PATH="$HOME/.local/bin:$PATH"

LOG_DIR="${ARXIV_BENCH_LOG_DIR:-$HOME/.local/state/arxiv_bench/logs}"
mkdir -p "$LOG_DIR"

DATE_STR="$(date -u +%Y%m%d)"
RUN_ID="daily_${DATE_STR}_$(date -u +%H%M%S)"
LOG_FILE="$LOG_DIR/${DATE_STR}_${RUN_ID}.log"

# Route non-TTY cron output cleanly to rotated per-run log files
if [ ! -t 1 ]; then
    exec > >(tee -a "$LOG_FILE") 2>&1
fi

# Prune daily logs older than 30 days
find "$LOG_DIR" -type f \( -name '*.log' -o -name '*.jsonl' \) -mtime +30 -delete 2>/dev/null || true

echo "=== arxiv-bench daily update: run_id=${RUN_ID} ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ==="

echo "[1/8] Syncing daily arXiv Atom delta..."
uv run arxiv-bench sync --mode daily --run-id "$RUN_ID"

echo "[2/8] Running Stage 1 Gemini Flash (gemini-3.8-flash) abstract triage..."
uv run arxiv-bench triage --run-id "$RUN_ID"

echo "[3/8] Running Stage 2 multimodal Gemini Flash benchmark extraction..."
uv run arxiv-bench extract --run-id "$RUN_ID"

echo "[4/8] Enriching citations and venues via Semantic Scholar batch API..."
uv run arxiv-bench enrich --run-id "$RUN_ID"

echo "[5/8] Running downstream religious-bias extraction..."
uv run arxiv-bench religion extract --run-id "$RUN_ID"

echo "[6/8] Generating daily religious-bias update report..."
uv run arxiv-bench religion daily-update --run-id "$RUN_ID"

echo "[7/8] Regenerating full religious-bias reports..."
uv run arxiv-bench religion full-report

echo "[8/8] Creating atomic SQLite backup (VACUUM INTO + zstd)..."
uv run arxiv-bench backup

echo "=== Pipeline status check ==="
uv run arxiv-bench status

# Commit ONLY curated Markdown reports and README.md; never run `git add -A`
if [ -n "$(git status --porcelain -- ':!reports/' ':!README.md')" ]; then
    echo "WARNING: Uncommitted edits detected outside reports/ and README.md; skipping automated Git commit."
    exit 0
fi

git add reports/ README.md
if git diff --cached --quiet; then
    echo "No report changes to commit."
else
    git commit -m "Update: ${DATE_STR}"
    git push origin "$(git rev-parse --abbrev-ref HEAD)"
fi
