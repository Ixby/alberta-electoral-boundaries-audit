#!/bin/bash

# finalize_sentiment_intensity.sh
# Orchestrates: sentiment scoring completion verification → aggregation → section update

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_FILE="$PROJECT_ROOT/sentiment_intensity_run.log"
SCORES_CSV="$PROJECT_ROOT/data/outputs/sentiment_intensity_scores.csv"

echo "=== Sentiment Intensity Finalization Workflow ==="
echo "Project root: $PROJECT_ROOT"
echo ""

# Step 1: Verify sentiment scoring is complete
echo "[1/3] Checking sentiment intensity scoring status..."
if [ ! -f "$SCORES_CSV" ]; then
    echo "ERROR: $SCORES_CSV not found. Sentiment scoring may not have started."
    exit 1
fi

LINES=$(wc -l < "$SCORES_CSV")
ROWS=$((LINES - 1))  # Subtract header
echo "Current rows scored: $ROWS / 459"

if [ "$ROWS" -lt 459 ]; then
    echo "Sentiment scoring still in progress. Waiting..."
    while [ "$ROWS" -lt 459 ]; do
        sleep 30
        LINES=$(wc -l < "$SCORES_CSV")
        ROWS=$((LINES - 1))
        TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
        echo "[$TIMESTAMP] Progress: $ROWS / 459 rows"
    done
fi

echo "✓ Sentiment intensity scoring complete!"
echo ""

# Step 2: Aggregate intensity scores
echo "[2/3] Aggregating intensity scores by configuration..."
cd "$PROJECT_ROOT"
python "analysis/scripts/aggregate_sentiment_intensity.py"
echo ""

# Step 3: Update report section
echo "[3/3] Updating §5.9.4.6 in report_academic.md..."
python "analysis/scripts/update_intensity_section.py"
echo ""

echo "=== Workflow Complete ==="
echo "Next steps:"
echo "  1. Review the updated §5.9.4.6 section"
echo "  2. Run: git status"
echo "  3. Commit changes with: git add -A && git commit -m 'feat(intensity): LLM-scored weighted-net sentiment table integrated into §5.9.4.6'"
