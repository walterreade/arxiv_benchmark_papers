#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

export PATH="$HOME/.local/bin:$PATH"
export TQDM_DISABLE=1
# Avoid dual-key SDK notice when GOOGLE_API_KEY is already configured in .env / shell
unset GEMINI_API_KEY || true

LOG_DIR="${ARXIV_BENCH_LOG_DIR:-$HOME/.local/state/arxiv_bench/logs}"
mkdir -p "$LOG_DIR"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG_FILE="$LOG_DIR/extract_backfill_${TS}.log"
PID_FILE="$LOG_DIR/extract_backfill.pid"
echo "$$" > "$PID_FILE"

if [ -t 1 ]; then
    exec > >(tee -a "$LOG_FILE") 2>&1
else
    exec >> "$LOG_FILE" 2>&1
fi

THRESHOLD="${EXTRACT_THRESHOLD:-0.70}"
SINCE="${EXTRACT_SINCE:-2024-01-01}"
UNTIL="${EXTRACT_UNTIL:-}"
WORKERS="${EXTRACT_WORKERS:-36}"
MAX_RPM="${EXTRACT_MAX_RPM:-100}"
CHUNK_SIZE="${EXTRACT_CHUNK_SIZE:-500}"
THINKING_BUDGET="${EXTRACT_THINKING_BUDGET:-0}"
LEG_LIMIT="${EXTRACT_LEG_LIMIT:-5000}"
LEG_MAX_COST="${EXTRACT_LEG_MAX_COST_USD:-60}"
PROGRESS_EVERY="${EXTRACT_PROGRESS_EVERY:-50}"
RUN_FINAL_RETRY="${EXTRACT_RUN_FINAL_RETRY:-1}"
RETRY_MAX_COST="${EXTRACT_RETRY_MAX_COST_USD:-25}"

COMMON_ARGS=(--threshold "$THRESHOLD")
if [ -n "$SINCE" ]; then
    COMMON_ARGS+=(--since "$SINCE")
fi
if [ -n "$UNTIL" ]; then
    COMMON_ARGS+=(--until "$UNTIL")
fi
if [ -n "$THINKING_BUDGET" ]; then
    COMMON_ARGS+=(--thinking-budget "$THINKING_BUDGET")
fi

echo "=== Stage 2 PDF Extraction Backfill Started: ${TS} (pid=$$) ==="
echo "Log: ${LOG_FILE}"
echo "Config: threshold=${THRESHOLD} since=${SINCE:-none} until=${UNTIL:-none} workers=${WORKERS} max_rpm=${MAX_RPM} chunk_size=${CHUNK_SIZE} thinking_budget=${THINKING_BUDGET:-default} leg_limit=${LEG_LIMIT} leg_max_cost_usd=${LEG_MAX_COST}"

leg=0
while true; do
    leg=$((leg + 1))
    RUN_ID="extract_backfill_${TS}_leg${leg}"
    echo ""
    echo "=== [Leg ${leg}] Starting run_id=${RUN_ID} ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ==="

    SUMMARY_JSON="$(mktemp)"
    rc=0
    uv run arxiv-bench extract \
        "${COMMON_ARGS[@]}" \
        --workers "$WORKERS" \
        --chunk-size "$CHUNK_SIZE" \
        --max-rpm "$MAX_RPM" \
        --limit "$LEG_LIMIT" \
        --max-cost-usd "$LEG_MAX_COST" \
        --progress-every "$PROGRESS_EVERY" \
        --run-id "$RUN_ID" \
        > "$SUMMARY_JSON" || rc=$?
    cat "$SUMMARY_JSON"

    if [ "$rc" -ne 0 ]; then
        echo "=== [Leg ${leg}] Stopped with exit code ${rc}; halting backfill cleanly ==="
        rm -f "$SUMMARY_JSON"
        exit "$rc"
    fi

    read -r ATTEMPTED SUCCEEDED FAILED COST_USD < <(
        uv run python -c "
import json, sys
d = json.load(open(sys.argv[1]))
print(d['attempted'], d['succeeded'], d['failed'], d['estimated_cost_usd'])
" "$SUMMARY_JSON"
    )
    rm -f "$SUMMARY_JSON"

    echo "=== [Leg ${leg}] Completed: attempted=${ATTEMPTED}, succeeded=${SUCCEEDED}, failed=${FAILED}, est_cost_usd=${COST_USD} ==="

    if [ "$ATTEMPTED" -eq 0 ]; then
        echo "=== Zero pending papers left; exiting leg loop ==="
        break
    fi

    if [ "$ATTEMPTED" -lt "$LEG_LIMIT" ]; then
        echo "=== Final partial leg complete (attempted=${ATTEMPTED} < leg_limit=${LEG_LIMIT}); exiting leg loop ==="
        break
    fi

    echo "=== [Leg ${leg}] Running local NVMe checkpoint backup ==="
    uv run arxiv-bench backup --no-gcs --no-nfs
done

if [ "$RUN_FINAL_RETRY" = "1" ]; then
    echo ""
    echo "=== Final --retry-failed pass for any transient errors ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ==="
    retry_rc=0
    uv run arxiv-bench extract \
        "${COMMON_ARGS[@]}" \
        --retry-failed \
        --workers 12 \
        --chunk-size 100 \
        --max-rpm 35 \
        --max-cost-usd "$RETRY_MAX_COST" \
        --progress-every 25 \
        --run-id "extract_backfill_${TS}_retry" || retry_rc=$?
    echo "=== Final --retry-failed pass finished with exit code ${retry_rc} ==="
fi

echo ""
echo "=== Creating final restore-verified backup (local NVMe + NFS + GCS) ==="
uv run arxiv-bench backup --verify-restore

echo ""
echo "=== Final Pipeline Status ==="
uv run arxiv-bench status
echo "=== Stage 2 PDF Extraction Backfill Finished: $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
