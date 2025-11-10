#!/bin/bash
# Verify MLEBench Selected Tasks
# This script verifies that all selected MLEBench tasks exist

set -e

PROJECT_DIR="/home/aiops/liufan/projects/DeepModeling"
MLE_DIR="$PROJECT_DIR/benchmarks/mlebench/competitions"

echo "=========================================="
echo "Verifying MLEBench Selected Tasks"
echo "=========================================="
echo ""

TASKS=(
    "aptos2019-blindness-detection"
    "plant-pathology-2020-fgvc7"
    "us-patent-phrase-to-phrase-matching"
    "new-york-city-taxi-fare-prediction"
    "tabular-playground-series-dec-2021"
)

total=0
found=0
missing=0

for task in "${TASKS[@]}"; do
    total=$((total + 1))
    if [ -d "$MLE_DIR/$task" ]; then
        echo "✓ $task"
        found=$((found + 1))
    else
        echo "✗ $task (MISSING)"
        missing=$((missing + 1))
    fi
done

echo ""
echo "=========================================="
echo "Summary:"
echo "  Total: $total"
echo "  Found: $found"
echo "  Missing: $missing"
echo "=========================================="

if [ $missing -eq 0 ]; then
    echo "✓ All selected tasks verified successfully!"
    exit 0
else
    echo "✗ Some tasks are missing. Please check the task names."
    exit 1
fi
