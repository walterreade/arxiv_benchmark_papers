#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

export PATH="$HOME/.local/bin:$PATH"
export TQDM_DISABLE=1

LOG_DIR="${ARXIV_BENCH_LOG_DIR:-$HOME/.local/state/arxiv_bench/logs}"
mkdir -p "$LOG_DIR"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG_FILE="$LOG_DIR/triage_flash_backfill_${TS}.log"
PID_FILE="$LOG_DIR/triage_flash_backfill.pid"
echo "$$" > "$PID_FILE"

exec > >(tee -a "$LOG_FILE") 2>&1

WORKERS="${TRIAGE_WORKERS:-48}"
BATCH_SIZE="${TRIAGE_FLASH_BATCH_SIZE:-20}"
CHUNK_SIZE="${TRIAGE_CHUNK_SIZE:-2880}"
MAX_RPM="${TRIAGE_FLASH_MAX_RPM:-140}"
LEG_LIMIT="${TRIAGE_LEG_LIMIT:-150000}"
LEG_MAX_COST="${TRIAGE_LEG_MAX_COST_USD:-60}"
FLASH_MODEL="${TRIAGE_FLASH_MODEL:-gemini-3.8-flash}"

echo "=== Flash Stage 1 Triage Backfill Started: ${TS} (pid=$$) ==="
echo "Log: ${LOG_FILE}"
echo "Config: model=${FLASH_MODEL} workers=${WORKERS} batch_size=${BATCH_SIZE} chunk_size=${CHUNK_SIZE} max_rpm=${MAX_RPM} leg_limit=${LEG_LIMIT}"

leg=0
while true; do
    leg=$((leg + 1))
    RUN_ID="flash_backfill_${TS}_leg${leg}"
    echo ""
    echo "=== [Leg ${leg}] Starting run_id=${RUN_ID} ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ==="

    SUMMARY_JSON="$(mktemp)"
    rc=0
    uv run arxiv-bench triage \
        --backend flash \
        --flash-model "$FLASH_MODEL" \
        --workers "$WORKERS" \
        --flash-batch-size "$BATCH_SIZE" \
        --chunk-size "$CHUNK_SIZE" \
        --flash-max-rpm "$MAX_RPM" \
        --limit "$LEG_LIMIT" \
        --max-cost-usd "$LEG_MAX_COST" \
        --run-id "$RUN_ID" \
        > "$SUMMARY_JSON" || rc=$?
    cat "$SUMMARY_JSON"

    if [ "$rc" -ne 0 ]; then
        echo "=== [Leg ${leg}] Stopped with exit code ${rc}; halting backfill cleanly ==="
        rm -f "$SUMMARY_JSON"
        exit "$rc"
    fi

    ATTEMPTED="$(uv run python -c "import json, sys; print(json.load(open(sys.argv[1]))['attempted'])" "$SUMMARY_JSON")"
    SUCCEEDED="$(uv run python -c "import json, sys; print(json.load(open(sys.argv[1]))['succeeded'])" "$SUMMARY_JSON")"
    rm -f "$SUMMARY_JSON"

    echo "=== [Leg ${leg}] Completed: attempted=${ATTEMPTED}, succeeded=${SUCCEEDED} ==="

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

echo ""
echo "=== Final retry pass for any transient failures ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ==="
uv run arxiv-bench triage \
    --backend flash \
    --flash-model "$FLASH_MODEL" \
    --workers 24 \
    --flash-batch-size "$BATCH_SIZE" \
    --chunk-size 1000 \
    --flash-max-rpm 90 \
    --max-cost-usd 20 \
    --run-id "flash_backfill_${TS}_retry"

echo ""
echo "=== Creating final restore-verified local NVMe backup ==="
uv run arxiv-bench backup --verify-restore --no-gcs --no-nfs

echo ""
echo "=== Final Pipeline Status ==="
uv run arxiv-bench status
echo "=== Flash Stage 1 Triage Backfill Finished: $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
