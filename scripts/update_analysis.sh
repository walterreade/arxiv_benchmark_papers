#!/bin/bash
# Update Analysis Pipeline
# Downloads new papers, performs 1st and 2nd pass analysis, and generates update file

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "========================================"
echo "Starting Analysis Update Pipeline"
echo "========================================"
echo ""

# Record existing 2nd pass JSON files before running
EXISTING_2ND_PASS=$(mktemp)
if [ -d "json/2nd_pass_json" ]; then
    find json/2nd_pass_json -name "*.json" -type f > "$EXISTING_2ND_PASS"
else
    touch "$EXISTING_2ND_PASS"
fi

# Step 1: Download new papers
echo "Step 1: Downloading new papers from arXiv..."
echo "----------------------------------------"
uv run python scripts/download_arxiv_benchmark_papers.py
echo ""

# Step 2: First pass analysis
echo "Step 2: Running 1st pass analysis..."
echo "----------------------------------------"
uv run python scripts/1st_pass_analyze_papers.py
echo ""

# Step 3: Second pass analysis (for papers meeting criteria)
echo "Step 3: Running 2nd pass analysis..."
echo "----------------------------------------"
uv run python scripts/2nd_pass_analyze_papers.py
echo ""

# Step 4: Check for new 2nd pass JSON files
echo "Step 4: Checking for new papers..."
echo "----------------------------------------"

NEW_JSON_FILES=$(mktemp)
if [ -d "json/2nd_pass_json" ]; then
    find json/2nd_pass_json -name "*.json" -type f > "$NEW_JSON_FILES"
    
    # Find files that are in NEW but not in EXISTING
    NEW_PAPERS=$(comm -23 <(sort "$NEW_JSON_FILES") <(sort "$EXISTING_2ND_PASS"))
else
    NEW_PAPERS=""
fi

# Clean up temp files
rm -f "$EXISTING_2ND_PASS" "$NEW_JSON_FILES"

if [ -z "$NEW_PAPERS" ]; then
    echo "No new papers were analyzed in 2nd pass."
    echo ""
    echo "========================================"
    echo "Pipeline Complete (no updates)"
    echo "========================================"
    exit 0
fi

# Count new papers
NEW_COUNT=$(echo "$NEW_PAPERS" | wc -l | tr -d ' ')
echo "Found $NEW_COUNT new papers for update file."
echo ""

# Step 5: Generate timestamped update file
echo "Step 5: Generating update file..."
echo "----------------------------------------"

# Create updates directory if needed
mkdir -p analysis/updates

# Generate the update file
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="analysis/updates/update_${TIMESTAMP}.md"

# Pass the new JSON files to the generate_update script
echo "$NEW_PAPERS" | xargs uv run python scripts/generate_update.py --json-files --output "$OUTPUT_FILE"

echo ""
echo "========================================"
echo "Pipeline Complete!"
echo "========================================"
echo "New papers analyzed: $NEW_COUNT"
echo "Update file: $OUTPUT_FILE"
echo "========================================"
