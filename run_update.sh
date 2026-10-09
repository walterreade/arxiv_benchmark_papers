#!/bin/bash
# Update Analysis Pipeline
# Downloads new papers, performs multi-pass analysis, and generates update file.
# Robust to interruptions: uses persistent state files so re-running resumes safely.

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Add local bin and snap bin to PATH
export PATH="/home/inversion_google_com/.local/bin:/snap/bin:$PATH"

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
    sed -i "s|\[Religious Papers - Latest Daily Update\](reports/daily_updates/[^)]*)|[Religious Papers - Latest Daily Update](${ENCODED_PATH})|" README.md
    echo "Updated README to link to: $ENCODED_PATH"
fi

# --- Stage 9: Upload and commit ---
echo ""
echo "Stage 9: Uploading PDFs and committing changes..."
echo "----------------------------------------"

# Upload only PDFs that are not already in the bucket.
# One bucket listing + a name diff is far cheaper than `cp -n`, which issues a
# per-object existence check for every one of the ~79k local PDFs.
# Note: only the top level of pdf/ is compared. The legacy pdf/cs, pdf/math and
# pdf/cond-mat subdirectories are already uploaded and nothing new is written
# there (sanitize_arxiv_id flattens old-style IDs). To force a full sweep:
#   gcloud storage cp -r -n pdf gs://inversion
GCS_PDF_PREFIX="gs://inversion/pdf"
# The corp credential (inversion@google.com) intermittently fails the GCS IAM
# check with a spurious 403 "permission denied". It comes in bad windows rather
# than uniformly, but during one it is frequent enough that the ~80-page bucket
# listing never finishes -- a single failed page aborts the whole stage. The VM
# service account resolves cleanly, so prefer it.
GCS_READ_ACCOUNT="44551806893-compute@developer.gserviceaccount.com"

# Uploads can only use the service account if the instance carries a read-write
# storage scope; with devstorage.read_only the SA can list but every write comes
# back "Provided scope(s) are not authorized". Probe the live scopes instead of
# hardcoding the answer, so this promotes itself the moment the instance's
# access scopes are widened. Until then writes fall back to the corp account,
# where a failed write is at least per-object and self-healing -- the next run's
# diff retries it -- unlike a failed listing.
GCS_WRITE_ACCOUNT=$(gcloud config get-value account 2>/dev/null)
VM_SCOPES=$(curl -s -m 5 -H "Metadata-Flavor: Google" \
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes" 2>/dev/null)
case "$VM_SCOPES" in
    *devstorage.read_write*|*devstorage.full_control*|*auth/cloud-platform*)
        GCS_WRITE_ACCOUNT="$GCS_READ_ACCOUNT" ;;
esac
echo "GCS: reading as $GCS_READ_ACCOUNT, writing as $GCS_WRITE_ACCOUNT"

LOCAL_PDFS=$(mktemp)
REMOTE_PDFS=$(mktemp)
PDFS_TO_UPLOAD=$(mktemp)

ls -1 pdf | grep '\.pdf$' | sort > "$LOCAL_PDFS"

CLOUDSDK_CORE_ACCOUNT="$GCS_READ_ACCOUNT" \
    gcloud storage ls "$GCS_PDF_PREFIX/" > "$REMOTE_PDFS.raw" 2> "$REMOTE_PDFS.err"
LS_STATUS=$?
# An empty prefix also exits non-zero; that just means everything is new.
if [ $LS_STATUS -ne 0 ] && grep -q "matched no objects" "$REMOTE_PDFS.err"; then
    LS_STATUS=0
fi

if [ $LS_STATUS -eq 0 ]; then
    sed "s|^$GCS_PDF_PREFIX/||" "$REMOTE_PDFS.raw" | grep '\.pdf$' | sort > "$REMOTE_PDFS"
    comm -23 "$LOCAL_PDFS" "$REMOTE_PDFS" | sed 's|^|pdf/|' > "$PDFS_TO_UPLOAD"
    UPLOAD_COUNT=$(wc -l < "$PDFS_TO_UPLOAD" | tr -d ' ')

    if [ "$UPLOAD_COUNT" -eq 0 ]; then
        echo "GCS already has all $(wc -l < "$LOCAL_PDFS" | tr -d ' ') PDFs; nothing to upload."
    else
        # Retry to ride out a bad window. Deliberately a plain cp, not `cp -n`:
        # no-clobber checks the destination first, which would put the flaky
        # read permission back on the write path. Re-sending the handful of
        # PDFs an earlier attempt already landed is the cheaper trade.
        UPLOAD_OK=false
        for attempt in 1 2 3; do
            if CLOUDSDK_CORE_ACCOUNT="$GCS_WRITE_ACCOUNT" \
                gcloud storage cp -I "$GCS_PDF_PREFIX/" < "$PDFS_TO_UPLOAD"; then
                UPLOAD_OK=true
                break
            fi
            echo "GCS upload attempt $attempt failed; retrying in $((attempt * 20))s."
            sleep $((attempt * 20))
        done

        if [ "$UPLOAD_OK" = true ]; then
            echo "GCS upload complete ($UPLOAD_COUNT new PDFs)."
        else
            echo "WARNING: GCS upload failed after 3 attempts. Changes will still be committed."
        fi
    fi
else
    echo "WARNING: Could not list $GCS_PDF_PREFIX; skipping upload."
    cat "$REMOTE_PDFS.err"
fi

rm -f "$LOCAL_PDFS" "$REMOTE_PDFS" "$REMOTE_PDFS.raw" "$REMOTE_PDFS.err" "$PDFS_TO_UPLOAD"

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
