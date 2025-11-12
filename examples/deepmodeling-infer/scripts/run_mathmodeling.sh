#!/usr/bin/env bash
# Batch inference on representative MathModeling benchmark tasks

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
APP_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)
REPO_ROOT=$(cd "${APP_ROOT}/../.." && pwd)

API_ENDPOINT=${API_ENDPOINT:-"http://localhost:8000"}
MODEL_PATH=${MODEL_PATH:-"/home/aiops/liufan/projects/models/dm-sft-Qwen2.5-7B-Instruct/merged"}
DATA_DIR=${MATHMODELING_DATA_DIR:-"${REPO_ROOT}/data/mathmodeling-bench/competitions"}
OUTPUT_DIR=${OUTPUT_DIR:-"${APP_ROOT}/results"}
WORKSPACE_DIR=${WORKSPACE_DIR:-"${APP_ROOT}/workspace_infer"}
MAX_TURNS=${MAX_TURNS:-10}
TEMPERATURE=${TEMPERATURE:-0.0}

TASKS=(
  bwor-0  bwor-5  bwor-10  bwor-15  bwor-20  bwor-25  bwor-30  bwor-35  bwor-40  bwor-45
  bwor-50 bwor-55 bwor-60  bwor-65  bwor-70  bwor-75  bwor-80
  mamo-easy-0   mamo-easy-10  mamo-easy-20  mamo-easy-30  mamo-easy-40  mamo-easy-50  mamo-easy-60  mamo-easy-70  mamo-easy-80  mamo-easy-90
  mamo-easy-100 mamo-easy-110 mamo-easy-120 mamo-easy-130 mamo-easy-140 mamo-easy-150 mamo-easy-160 mamo-easy-170 mamo-easy-180 mamo-easy-190
  mamo-easy-200 mamo-easy-210 mamo-easy-220 mamo-easy-230 mamo-easy-240 mamo-easy-250 mamo-easy-260 mamo-easy-270 mamo-easy-280 mamo-easy-290
  mamo-easy-300 mamo-easy-310 mamo-easy-320 mamo-easy-330 mamo-easy-340 mamo-easy-350 mamo-easy-360 mamo-easy-370 mamo-easy-380 mamo-easy-390
  mamo-easy-400 mamo-easy-410 mamo-easy-420 mamo-easy-430 mamo-easy-440 mamo-easy-450 mamo-easy-460 mamo-easy-470 mamo-easy-480 mamo-easy-490
  mamo-easy-500 mamo-easy-510 mamo-easy-520 mamo-easy-530 mamo-easy-540 mamo-easy-550 mamo-easy-560 mamo-easy-570 mamo-easy-580 mamo-easy-590
  mamo-easy-600 mamo-easy-610 mamo-easy-620 mamo-easy-630 mamo-easy-640 mamo-easy-650
  mamo-complex-0   mamo-complex-8   mamo-complex-16  mamo-complex-24  mamo-complex-32  mamo-complex-40  mamo-complex-48  mamo-complex-56  mamo-complex-64  mamo-complex-72
  mamo-complex-80  mamo-complex-88  mamo-complex-96  mamo-complex-104 mamo-complex-112 mamo-complex-120 mamo-complex-128 mamo-complex-136 mamo-complex-144 mamo-complex-152
  mamo-complex-160 mamo-complex-168 mamo-complex-176 mamo-complex-184 mamo-complex-192 mamo-complex-200 mamo-complex-208
  mamo-ode-0   mamo-ode-10  mamo-ode-20  mamo-ode-30  mamo-ode-40  mamo-ode-50  mamo-ode-60  mamo-ode-70  mamo-ode-80  mamo-ode-90
  mamo-ode-100 mamo-ode-110 mamo-ode-120 mamo-ode-130 mamo-ode-140 mamo-ode-150 mamo-ode-160 mamo-ode-170 mamo-ode-180 mamo-ode-190
  mamo-ode-200 mamo-ode-210 mamo-ode-220 mamo-ode-230 mamo-ode-240 mamo-ode-250 mamo-ode-260 mamo-ode-270 mamo-ode-280 mamo-ode-290
  mamo-ode-300 mamo-ode-310 mamo-ode-320 mamo-ode-330 mamo-ode-340
)

python -m src.infer \
  --api-endpoint "${API_ENDPOINT}" \
  --model-path "${MODEL_PATH}" \
  --data-dir "${DATA_DIR}" \
  --benchmark mathmodeling \
  --competitions "${TASKS[@]}" \
  --output-dir "${OUTPUT_DIR}" \
  --workspace-dir "${WORKSPACE_DIR}" \
  --max-turns "${MAX_TURNS}" \
  --temperature "${TEMPERATURE}"
