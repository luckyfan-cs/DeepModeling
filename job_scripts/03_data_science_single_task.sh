#!/bin/bash
################################################################################
# Example 3: Data Science (MLE-Bench) - Single Task
################################################################################
# This script demonstrates running a single Kaggle-style ML competition
# Task: Spaceship Titanic (binary classification)
################################################################################

set -e  # Exit on error

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Configuration
WORKFLOW="scientific"
BENCHMARK="mle"
DATA_DIR="./data/mlebench"
LLM_MODEL="gpt-4o-mini"
TASK="spaceship-titanic"

echo "============================================================"
echo "DeepModeling Example: Data Science Single Task"
echo "============================================================"
echo "Competition: $TASK"
echo "Model: $LLM_MODEL"
echo "Data: $DATA_DIR"
echo "Type: Binary Classification (Kaggle)"
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
echo "Predictions saved in: runs/modeling_run_${TASK}_*/submission.csv"
echo "============================================================"
