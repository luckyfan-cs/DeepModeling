#!/bin/bash
################################################################################
# Example 7: Multi-Modal Data - Time Series
################################################################################
# This script demonstrates handling time series data for forecasting
# Example: Store sales forecasting with temporal patterns
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
TASK="store-sales-time-series-forecasting"

echo "============================================================"
echo "DeepModeling Example: Time Series Forecasting"
echo "============================================================"
echo "Task: $TASK"
echo "Model: $LLM_MODEL"
echo "Data Modality: Time Series (Sequential temporal data)"
echo "Task Type: Multi-step ahead forecasting"
echo "============================================================"
echo ""
echo "Dataset Structure:"
echo "  data/mlebench/competitions/store-sales-time-series-forecasting/"
echo "    ├── train.csv             # Historical sales data"
echo "    │   └── Columns: date, store_id, item_id, sales"
echo "    ├── test.csv              # Future dates to predict"
echo "    ├── stores.csv            # Store metadata"
echo "    ├── items.csv             # Product information"
echo "    └── sample_submission.csv # Expected forecast format"
echo ""
echo "The framework will:"
echo "  1. Load and parse time series data (CSV/Parquet/HDF5)"
echo "  2. Perform temporal feature engineering"
echo "  3. Handle seasonality and trends"
echo "  4. Build forecasting model (ARIMA/LSTM/Prophet)"
echo "  5. Generate multi-step forecasts"
echo "  6. Create submission with predictions"
echo ""

# Run time series forecasting task
python main.py \
  --workflow "$WORKFLOW" \
  --benchmark "$BENCHMARK" \
  --data-dir "$DATA_DIR" \
  --llm-model "$LLM_MODEL" \
  --task "$TASK"

echo ""
echo "============================================================"
echo "Time series forecasting completed!"
echo ""
echo "Time Series Processing Pipeline:"
echo "  ✓ Automatic format detection (CSV/Parquet/HDF5)"
echo "  ✓ Temporal feature extraction"
echo "  ✓ Seasonality and trend decomposition"
echo "  ✓ Model selection (ARIMA/LSTM/Prophet/XGBoost)"
echo "  ✓ Multi-step ahead forecasting"
echo "  ✓ Submission file with timestamps"
echo ""
echo "Results: runs/modeling_run_${TASK}_*/submission.csv"
echo "============================================================"
