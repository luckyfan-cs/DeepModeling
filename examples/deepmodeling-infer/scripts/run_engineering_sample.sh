#!/usr/bin/env bash
# Batch inference on representative Engineering benchmark tasks

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
APP_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)
REPO_ROOT=$(cd "${APP_ROOT}/../.." && pwd)

API_ENDPOINT=${API_ENDPOINT:-"http://localhost:8000"}
MODEL_PATH=${MODEL_PATH:-"/home/aiops/liufan/projects/models/dm-sft-Qwen2.5-7B-Instruct/merged"}
DATA_DIR=${ENGINEERING_DATA_DIR:-"${REPO_ROOT}/data/engineering-bench/competitions"}
OUTPUT_DIR=${OUTPUT_DIR:-"${APP_ROOT}/results"}
WORKSPACE_DIR=${WORKSPACE_DIR:-"${APP_ROOT}/workspace_infer"}
MAX_TURNS=${MAX_TURNS:-10}
TEMPERATURE=${TEMPERATURE:-0.0}

TASKS=(
  industry-0  industry-3  industry-6  industry-9  industry-12  industry-15
  industry-18 industry-21 industry-24 industry-27 industry-30 industry-33
  industry-36 industry-39 industry-42 industry-45 industry-48 industry-51
  industry-54 industry-57 industry-60 industry-63 industry-66 industry-69
  industry-72 industry-75 industry-78 industry-81 industry-84 industry-87
)

python -m src.infer \
  --api-endpoint "${API_ENDPOINT}" \
  --model-path "${MODEL_PATH}" \
  --data-dir "${DATA_DIR}" \
  --benchmark engineering \
  --competitions "${TASKS[@]}" \
  --output-dir "${OUTPUT_DIR}" \
  --workspace-dir "${WORKSPACE_DIR}" \
  --max-turns "${MAX_TURNS}" \
  --temperature "${TEMPERATURE}"
