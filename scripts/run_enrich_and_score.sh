#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

export PATH="$HOME/.local/bin:$PATH"
export TQDM_DISABLE=1
unset GEMINI_API_KEY || true

LOG_DIR="${ARXIV_BENCH_LOG_DIR:-$HOME/.local/state/arxiv_bench/logs}"
mkdir -p "$LOG_DIR"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG_FILE="$LOG_DIR/enrich_and_score_${TS}.log"
PID_FILE="$LOG_DIR/enrich_and_score.pid"
echo "$$" > "$PID_FILE"

if [ -t 1 ]; then
    exec > >(tee -a "$LOG_FILE") 2>&1
else
    exec >> "$LOG_FILE" 2>&1
fi

ENRICH_DELAY="${ENRICH_DELAY:-2.5}"
SCORE_RUBRIC="${SCORE_RUBRIC:-rubrics/gap_analysis_core_v1.yaml}"
SCORE_CONTEXT="${SCORE_CONTEXT:-card}"
SCORE_WORKERS="${SCORE_WORKERS:-32}"
SCORE_CHUNK_SIZE="${SCORE_CHUNK_SIZE:-1000}"
SCORE_MAX_RPM="${SCORE_MAX_RPM:-1500}"
SCORE_MAX_COST_USD="${SCORE_MAX_COST_USD:-25}"
SCORE_PROGRESS_EVERY="${SCORE_PROGRESS_EVERY:-500}"

echo "=== Enrich + Stage 3 Score Pipeline Started: ${TS} (pid=$$) ==="
echo "Log: ${LOG_FILE}"
echo "Config: enrich_delay=${ENRICH_DELAY}s rubric=${SCORE_RUBRIC} context=${SCORE_CONTEXT} workers=${SCORE_WORKERS} max_rpm=${SCORE_MAX_RPM} chunk_size=${SCORE_CHUNK_SIZE} max_cost_usd=${SCORE_MAX_COST_USD}"

echo ""
echo "=== [Step 1] Semantic Scholar Batch Enrichment ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ==="
enrich_rc=0
uv run arxiv-bench enrich \
    --delay "$ENRICH_DELAY" \
    --progress-every 5 \
    --run-id "enrich_${TS}" || enrich_rc=$?
echo "=== [Step 1] Initial enrich pass exited with code ${enrich_rc} ==="

if [ "$enrich_rc" -eq 0 ]; then
    # Quick cleanup pass in case any single batch had a transient S2 error
    echo ""
    echo "=== [Step 1b] Semantic Scholar retry pass for any transient failed batches ==="
    uv run arxiv-bench enrich \
        --delay 4.0 \
        --progress-every 2 \
        --run-id "enrich_${TS}_retry" || true
fi

echo ""
echo "=== [Step 2] Stage 3 Gap-Rubric Scoring ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ==="
score_rc=0
uv run arxiv-bench score \
    --rubric "$SCORE_RUBRIC" \
    --context "$SCORE_CONTEXT" \
    --workers "$SCORE_WORKERS" \
    --chunk-size "$SCORE_CHUNK_SIZE" \
    --max-rpm "$SCORE_MAX_RPM" \
    --max-cost-usd "$SCORE_MAX_COST_USD" \
    --progress-every "$SCORE_PROGRESS_EVERY" \
    --run-id "score_${TS}" || score_rc=$?
echo "=== [Step 2] Stage 3 score exited with code ${score_rc} (0=complete, 2=stopped cleanly on quota/budget/guard) ==="

echo ""
echo "=== [Step 3] Creating final restore-verified backup (local NVMe + NFS + GCS) ==="
uv run arxiv-bench backup --verify-restore

echo ""
echo "=== Final Pipeline Status ==="
uv run arxiv-bench status
echo "=== Enrich + Stage 3 Score Pipeline Finished: $(date -u +%Y-%m-%dT%H:%M:%SZ) (enrich_rc=${enrich_rc}, score_rc=${score_rc}) ==="
