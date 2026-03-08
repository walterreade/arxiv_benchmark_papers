#!/bin/bash
# Update Analysis Pipeline
# Downloads new papers, performs multi-pass analysis, and generates update file.
# Robust to interruptions: uses persistent state files so re-running resumes safely.

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# --- Parse flags ---
FULL_ANALYSIS=false
for arg in "$@"; do
    case $arg in
        --full) FULL_ANALYSIS=true ;;
    esac
done

# --- State tracking ---
# Use persistent files instead of mktemp so state survives crashes.
STATE_DIR="utility_files"
SNAPSHOT_FILE="$STATE_DIR/.pipeline_2nd_pass_snapshot.txt"

echo "========================================"
echo "Starting Analysis Update Pipeline"
echo "========================================"
echo ""

# --- Stage 1: Download new papers ---
echo "Stage 1: Downloading new papers from arXiv..."
echo "----------------------------------------"
if uv run python scripts/1_classify_and_download_arxiv_papers.py; then
    echo "Stage 1 complete."
else
    echo "WARNING: Stage 1 (download) failed. Continuing with existing papers..."
fi
echo ""

# --- Stage 2: First pass analysis ---
echo "Stage 2: Running 1st pass analysis..."
echo "----------------------------------------"
if uv run python scripts/2_extract_paper_metadata.py; then
    echo "Stage 2 complete."
else
    echo "WARNING: Stage 2 (1st pass) failed. Continuing with existing results..."
fi
echo ""

# --- Stage 3: Second pass analysis ---
# Snapshot existing 2nd pass files BEFORE running, but only if no snapshot exists.
# This way, if the script is interrupted and re-run, we don't lose track of what's new.
if [ ! -f "$SNAPSHOT_FILE" ]; then
    if [ -d "json/3_paper_bias_targets" ]; then
        find json/3_paper_bias_targets -name "*.json" -type f | sort > "$SNAPSHOT_FILE"
    else
        touch "$SNAPSHOT_FILE"
    fi
    echo "(Created 2nd pass snapshot for tracking new papers)"
fi

echo "Stage 3: Running 2nd pass analysis..."
echo "----------------------------------------"
if uv run python scripts/3_extract_bias_targets.py; then
    echo "Stage 3 complete."
else
    echo "WARNING: Stage 3 (2nd pass) failed. Continuing with existing results..."
fi
echo ""

# --- Stage 4: Third pass analysis ---
echo "Stage 4: Running 3rd pass analysis..."
echo "----------------------------------------"
if uv run python scripts/4_extract_paper_details.py; then
    echo "Stage 4 complete."
else
    echo "WARNING: Stage 4 (3rd pass) failed. Continuing with existing results..."
fi
echo ""

# --- Stage 5: Identify new papers ---
echo "Stage 5: Checking for new papers..."
echo "----------------------------------------"

if [ -d "json/3_paper_bias_targets" ]; then
    CURRENT_FILES=$(find json/3_paper_bias_targets -name "*.json" -type f | sort)
    NEW_PAPERS=$(comm -23 <(echo "$CURRENT_FILES") <(cat "$SNAPSHOT_FILE"))
else
    NEW_PAPERS=""
fi

if [ -z "$NEW_PAPERS" ] && [ "$FULL_ANALYSIS" != true ]; then
    echo "No new papers were analyzed in 2nd pass."
    # Clean up snapshot since pipeline completed successfully
    rm -f "$SNAPSHOT_FILE"
    echo ""
    echo "========================================"
    echo "Pipeline Complete (no updates)"
    echo "========================================"
    exit 0
fi

if [ -z "$NEW_PAPERS" ] && [ "$FULL_ANALYSIS" = true ]; then
    echo "No new papers, but --full flag set. Regenerating reports..."
    echo ""
fi

if [ -n "$NEW_PAPERS" ]; then
    NEW_COUNT=$(echo "$NEW_PAPERS" | wc -l | tr -d ' ')
else
    NEW_COUNT=0
fi
echo "Found $NEW_COUNT new papers for update file."
echo ""

# --- Stage 6: Generate update file ---
echo "Stage 6: Generating update file..."
echo "----------------------------------------"

mkdir -p reports/daily_updates
TIMESTAMP=$(date +%Y%m%d)
OUTPUT_FILE="reports/daily_updates/${TIMESTAMP}_daily_update.md"

if [ -n "$NEW_PAPERS" ]; then
    if echo "$NEW_PAPERS" | xargs uv run python scripts/generate_daily_update.py --output "$OUTPUT_FILE" --json-files; then
        if [ -f "$OUTPUT_FILE" ]; then
            echo "Daily update generated: $OUTPUT_FILE"
        else
            echo "No papers passed the religion filter for the daily update."
        fi
    else
        echo "WARNING: Daily update generation failed."
    fi
fi

# --- Stage 7: Full analysis (optional) ---
if [ "$FULL_ANALYSIS" = true ]; then
    echo ""
    echo "Stage 7: Generating full analysis and talk facts..."
    echo "----------------------------------------"
    uv run python scripts/generate_full_analysis.py || echo "WARNING: Full analysis generation failed."
    uv run python scripts/generate_talk_facts.py || echo "WARNING: Talk facts generation failed."
fi

# --- Stage 8: Update README with latest daily update link ---
echo ""
echo "Stage 8: Updating README.md..."
echo "----------------------------------------"
LATEST_UPDATE=$(ls -1 reports/daily_updates/*_daily_update.md 2>/dev/null | sort | tail -1)
if [ -n "$LATEST_UPDATE" ]; then
    LATEST_BASENAME=$(basename "$LATEST_UPDATE")
    ENCODED_PATH="reports/daily_updates/${LATEST_BASENAME}"
    sed -i '' "s|\[Religious Papers - Latest Daily Update\](reports/daily_updates/[^)]*)|[Religious Papers - Latest Daily Update](${ENCODED_PATH})|" README.md
    echo "Updated README to link to: $ENCODED_PATH"
fi

# --- Stage 9: Upload and commit ---
echo ""
echo "Stage 9: Uploading PDFs and committing changes..."
echo "----------------------------------------"

# Copy new pdf files to GCS (skip existing with -n)
if gcloud storage cp -r -n pdf gs://inversion; then
    echo "GCS upload complete."
else
    echo "WARNING: GCS upload failed. Changes will still be committed."
fi

# Commit and push changes to git
git add -A
if git diff --cached --quiet; then
    echo "No changes to commit."
else
    git commit -m "Update: ${TIMESTAMP}"
    git pull --rebase
    git push
fi

# Clean up snapshot — pipeline completed successfully
rm -f "$SNAPSHOT_FILE"

echo ""
echo "========================================"
echo "Pipeline Complete!"
echo "========================================"
if [ -n "$NEW_PAPERS" ]; then
    echo "New papers analyzed: $NEW_COUNT"
fi
if [ -f "$OUTPUT_FILE" ]; then
    echo "Update file: $OUTPUT_FILE"
fi
echo "========================================"
