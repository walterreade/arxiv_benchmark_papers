#!/bin/bash
# Catchup Script
# Finds papers in 1st_pass_json where both is_llm_related and is_bias_related are true,
# then runs the 2nd and 3rd pass analysis for any that are missing.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "========================================"
echo "Catchup: Ensuring 2nd/3rd pass coverage"
echo "========================================"
echo ""

# Step 1: Identify eligible papers from 1st_pass_json
echo "Step 1: Scanning 1st_pass_json for papers with is_llm_related=true AND is_bias_related=true..."
echo "----------------------------------------"

ELIGIBLE=$(mktemp)
MISSING_2ND=$(mktemp)
MISSING_3RD=$(mktemp)

# Find all 1st pass JSONs where both flags are true
python3 -c "
import json, glob, os, sys
from pathlib import Path

eligible = []
for jf in sorted(glob.glob('json/1st_pass_json/*.json')):
    try:
        with open(jf) as f:
            data = json.load(f)
        if data.get('is_llm_related') is True and data.get('is_bias_related') is True:
            stem = Path(jf).stem
            eligible.append(stem)
    except (json.JSONDecodeError, IOError):
        continue

for s in eligible:
    print(s)
" > "$ELIGIBLE"

ELIGIBLE_COUNT=$(wc -l < "$ELIGIBLE" | tr -d ' ')
echo "Found $ELIGIBLE_COUNT eligible papers."
echo ""

# Step 2: Check which are missing from 2nd_pass_json
echo "Step 2: Checking for missing 2nd pass analyses..."
echo "----------------------------------------"

if [ -d "json/2nd_pass_json" ]; then
    ls json/2nd_pass_json/ | sed 's/\.json$//' | sort > /tmp/existing_2nd.txt
else
    touch /tmp/existing_2nd.txt
fi

sort "$ELIGIBLE" | comm -23 - /tmp/existing_2nd.txt > "$MISSING_2ND"
MISSING_2ND_COUNT=$(wc -l < "$MISSING_2ND" | tr -d ' ')
echo "Missing from 2nd_pass_json: $MISSING_2ND_COUNT"

# Step 3: Check which are missing from 3rd_pass_json
echo "Step 3: Checking for missing 3rd pass analyses..."
echo "----------------------------------------"

if [ -d "json/3rd_pass_json" ]; then
    ls json/3rd_pass_json/ | sed 's/\.json$//' | sort > /tmp/existing_3rd.txt
else
    touch /tmp/existing_3rd.txt
fi

sort "$ELIGIBLE" | comm -23 - /tmp/existing_3rd.txt > "$MISSING_3RD"
MISSING_3RD_COUNT=$(wc -l < "$MISSING_3RD" | tr -d ' ')
echo "Missing from 3rd_pass_json: $MISSING_3RD_COUNT"
echo ""

# Summary before running
echo "========================================"
echo "Summary"
echo "========================================"
echo "Eligible papers (is_llm_related + is_bias_related): $ELIGIBLE_COUNT"
echo "Missing from 2nd pass: $MISSING_2ND_COUNT"
echo "Missing from 3rd pass: $MISSING_3RD_COUNT"
echo "========================================"
echo ""

if [ "$MISSING_2ND_COUNT" -eq 0 ] && [ "$MISSING_3RD_COUNT" -eq 0 ]; then
    echo "All eligible papers already have 2nd and 3rd pass analyses. Nothing to do!"
    rm -f "$ELIGIBLE" "$MISSING_2ND" "$MISSING_3RD" /tmp/existing_2nd.txt /tmp/existing_3rd.txt
    exit 0
fi

# Ask for confirmation before running the expensive API calls
read -p "Proceed with running the missing analyses? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    rm -f "$ELIGIBLE" "$MISSING_2ND" "$MISSING_3RD" /tmp/existing_2nd.txt /tmp/existing_3rd.txt
    exit 0
fi

# Step 4: Run 2nd pass for missing papers
if [ "$MISSING_2ND_COUNT" -gt 0 ]; then
    echo ""
    echo "Step 4: Running 2nd pass analysis for $MISSING_2ND_COUNT missing papers..."
    echo "----------------------------------------"
    uv run python scripts/2nd_pass_analyze_papers.py
    echo ""
fi

# Step 5: Run 3rd pass for missing papers
if [ "$MISSING_3RD_COUNT" -gt 0 ]; then
    echo ""
    echo "Step 5: Running 3rd pass analysis for $MISSING_3RD_COUNT missing papers..."
    echo "----------------------------------------"
    uv run python scripts/3rd_pass_analyze_papers.py
    echo ""
fi

# Clean up temp files
rm -f "$ELIGIBLE" "$MISSING_2ND" "$MISSING_3RD" /tmp/existing_2nd.txt /tmp/existing_3rd.txt

echo ""
echo "========================================"
echo "Catchup Complete!"
echo "========================================"

# Show post-run status
echo ""
echo "Post-run coverage:"
FINAL_2ND=$(ls json/2nd_pass_json/ 2>/dev/null | wc -l | tr -d ' ')
FINAL_3RD=$(ls json/3rd_pass_json/ 2>/dev/null | wc -l | tr -d ' ')
echo "  2nd_pass_json: $FINAL_2ND files"
echo "  3rd_pass_json: $FINAL_3RD files"
echo "  Eligible papers: $ELIGIBLE_COUNT"
