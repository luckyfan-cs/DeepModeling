#!/bin/bash
################################################################################
# Example 2: Mathematical Modeling - Batch Evaluation
################################################################################
# This script demonstrates batch evaluation of multiple mathematical modeling
# problems. Tasks are configured in config.yaml
################################################################################

set -e  # Exit on error

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Configuration
WORKFLOW="scientific"
BENCHMARK="mathmodeling"
DATA_DIR="./data/mathmodeling-bench"
LLM_MODEL="gpt-4o-mini"

echo "============================================================"
echo "DeepModeling Example: Mathematical Modeling Batch"
echo "============================================================"
echo "Benchmark: $BENCHMARK"
echo "Model: $LLM_MODEL"
echo "Data: $DATA_DIR"
echo "Tasks: Configured in config.yaml"
echo "============================================================"
echo ""
echo "Sample config.yaml content:"
echo "---"
echo "mathmodeling_competitions:"
echo "  - bwor-0"
echo "  - industry-5"
echo "  - mamo-easy-10-resource-allocation"
echo "---"
echo ""
echo "Starting batch evaluation..."
echo ""

# Run batch evaluation
python main.py \
  --workflow "$WORKFLOW" \
  --benchmark "$BENCHMARK" \
  --data-dir "$DATA_DIR" \
  --llm-model "$LLM_MODEL"

echo ""
echo "============================================================"
echo "Batch evaluation completed!"
echo "Results saved in: runs/benchmark_results/${WORKFLOW}_on_${BENCHMARK}/"
echo "============================================================"
