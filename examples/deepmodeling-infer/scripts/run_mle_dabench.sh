#!/usr/bin/env bash
# Batch inference on representative DA-Bench (MLE) tasks

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
APP_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)
REPO_ROOT=$(cd "${APP_ROOT}/../.." && pwd)

API_ENDPOINT=${API_ENDPOINT:-"http://localhost:8000"}
MODEL_PATH=${MODEL_PATH:-"/home/aiops/liufan/projects/models/dm-sft-Qwen2.5-7B-Instruct/merged"}
DATA_DIR=${MLE_DATA_DIR:-"${REPO_ROOT}/benchmarks/mlebench/competitions"}
OUTPUT_DIR=${OUTPUT_DIR:-"${APP_ROOT}/results"}
WORKSPACE_DIR=${WORKSPACE_DIR:-"${APP_ROOT}/workspace_infer"}
MAX_TURNS=${MAX_TURNS:-10}
TEMPERATURE=${TEMPERATURE:-0.0}

TASKS=(
  dabench-0-mean-fare
  dabench-11-correlation-coefficient-between
  dabench-27-identify-outliers-charges
  dabench-55-what-mean-number
  dabench-69-feature-engineering-creating
  dabench-108-generate-feature-called
  dabench-124-there-significant-difference
  dabench-139-question-percentage-votes
  dabench-178-comprehensive-data-preprocessing
  dabench-216-mean-standard-deviation
  dabench-243-what-mean-batting
  dabench-268-meanpot-values-normally
  dabench-282-correlation-analysis-given
  dabench-320-what-mean-eventmsgtype
  dabench-351-determine-correlation-coefficient
  dabench-372-find-mean-median
  dabench-412-feature-called-familysize
  dabench-424-develop-machine-learning
  dabench-446-what-mean-wind
  dabench-466-there-correlation-between
  dabench-495-outlier-detection-percentage
  dabench-516-fare-distribution-skewed
  dabench-527-what-average-male
  dabench-551-what-mean-column
  dabench-578-what-average-trading
  dabench-604-identify-remove-outliers
  dabench-651-there-outliers-coordinate
  dabench-663-scatter-plot-high
  dabench-674-build-machine-learning
  dabench-716-data-preprocessing-dropping
  dabench-727-machine-learning-techniques
  dabench-738-distribution-column-credit
  dabench-759-median-range-maximum
)

python -m src.infer \
  --api-endpoint "${API_ENDPOINT}" \
  --model-path "${MODEL_PATH}" \
  --data-dir "${DATA_DIR}" \
  --benchmark mle \
  --competitions "${TASKS[@]}" \
  --output-dir "${OUTPUT_DIR}" \
  --workspace-dir "${WORKSPACE_DIR}" \
  --max-turns "${MAX_TURNS}" \
  --temperature "${TEMPERATURE}"
