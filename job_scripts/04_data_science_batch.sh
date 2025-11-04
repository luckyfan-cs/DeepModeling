#!/bin/bash
################################################################################
# Example 4: Data Science (MLE-Bench) - Batch Evaluation
################################################################################
# This script demonstrates batch evaluation of multiple Kaggle competitions
# covering different modalities: tabular, time series, NLP, CV
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

echo "============================================================"
echo "DeepModeling Example: Data Science Batch Evaluation"
echo "============================================================"
echo "Benchmark: MLE-Bench (Kaggle Competitions)"
echo "Model: $LLM_MODEL"
echo "Data: $DATA_DIR"
echo "============================================================"
echo ""
echo "Sample config.yaml content:"
echo "---"
echo "mle_competitions:"
echo "  - spaceship-titanic              # Tabular: Binary classification"
echo "  - house-prices-advanced-regression-techniques  # Tabular: Regression"
echo "  - digit-recognizer               # Computer Vision: Image classification"
echo "  - nlp-getting-started            # NLP: Text classification"
echo "  - store-sales-time-series-forecasting  # Time Series: Forecasting"
echo "---"
echo ""
echo "Starting multi-modal batch evaluation..."
echo ""

# Run batch evaluation
python main.py \
  --workflow "$WORKFLOW" \
  --benchmark "$BENCHMARK" \
  --data-dir "$DATA_DIR" \
  --llm-model "$LLM_MODEL"

echo ""
echo "============================================================"
echo "Multi-modal batch evaluation completed!"
echo "Results: runs/benchmark_results/${WORKFLOW}_on_${BENCHMARK}/"
echo ""
echo "Summary:"
echo "  - Tabular data tasks processed"
echo "  - Time series forecasts generated"
echo "  - Computer vision predictions created"
echo "  - NLP classifications completed"
echo "============================================================"
