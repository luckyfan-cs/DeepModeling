#!/usr/bin/env bash
# Batch inference on selected full Kaggle-style MLE benchmark tasks

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
  aptos2019-blindness-detection
  plant-pathology-2020-fgvc7
  us-patent-phrase-to-phrase-matching
  new-york-city-taxi-fare-prediction
  tabular-playground-series-dec-2021
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
