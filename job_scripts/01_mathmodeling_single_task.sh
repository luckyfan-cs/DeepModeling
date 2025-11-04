#!/bin/bash
################################################################################
# Example 1: Mathematical Modeling - Single Task
################################################################################
# This script demonstrates running a single mathematical modeling problem
# Task: Business optimization problem (BWOR dataset)
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
TASK="bwor-0"

echo "============================================================"
echo "DeepModeling Example: Mathematical Modeling Single Task"
echo "============================================================"
echo "Task: $TASK"
echo "Model: $LLM_MODEL"
echo "Data: $DATA_DIR"
echo "============================================================"
echo ""

# Run the task
python main.py \
  --workflow "$WORKFLOW" \
  --benchmark "$BENCHMARK" \
  --data-dir "$DATA_DIR" \
  --llm-model "$LLM_MODEL" \
  --task "$TASK"

echo ""
echo "============================================================"
echo "Task completed! Check results in:"
echo "  runs/benchmark_results/${WORKFLOW}_on_${BENCHMARK}/"
echo "============================================================"
