#!/usr/bin/env bash
# Batch inference on representative Science benchmark tasks

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
APP_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)
REPO_ROOT=$(cd "${APP_ROOT}/../.." && pwd)

API_ENDPOINT=${API_ENDPOINT:-"http://localhost:8000"}
MODEL_PATH=${MODEL_PATH:-"/home/aiops/liufan/projects/models/dm-sft-Qwen2.5-7B-Instruct/merged"}
DATA_DIR=${SCIENCE_DATA_DIR:-"${REPO_ROOT}/data/science-bench/competitions"}
OUTPUT_DIR=${OUTPUT_DIR:-"${APP_ROOT}/results"}
WORKSPACE_DIR=${WORKSPACE_DIR:-"${APP_ROOT}/workspace_infer"}
MAX_TURNS=${MAX_TURNS:-10}
TEMPERATURE=${TEMPERATURE:-0.0}

TASKS=(
  sciencebench-001-clintox-nn
  sciencebench-004-elk-new
  sciencebench-007-dkpes-visualization-2
  sciencebench-010-toronto-new
  sciencebench-013-drug-property-model
  sciencebench-016-compound-filter
  sciencebench-019-dili-models-ecfp-svm
  sciencebench-022-papyrus-filtering
  sciencebench-025-ecg-processing-vis2
  sciencebench-028-charge-density-difference
  sciencebench-031-plot-phonon-dos
  sciencebench-034-hrv-analyze
  sciencebench-037-cft
  sciencebench-040-md-rf
  sciencebench-043-eog-analyze
  sciencebench-046-mountainlion1
  sciencebench-049-eof-standard-hgt-plot
  sciencebench-052-aquatic-toxicity-qsar-vis
  sciencebench-055-plot-ocean-profiles
  sciencebench-058-nvc-gen-ind
  sciencebench-061-nvc-stackbar-plain-prediction
  sciencebench-064-plotting-flowline-mb-elevation
  sciencebench-067-cogsci-pattern-high-sim
  sciencebench-070-single-cell-analysis-de
  sciencebench-073-eeg2eeg-vis
  sciencebench-076-mineral-prospectivity-pred
  sciencebench-079-violin
  sciencebench-082-dendrogram
  sciencebench-085-saliva
  sciencebench-088-plot-collisions-map
  sciencebench-091-jnmf-plot-patterns
  sciencebench-094-polyverse-visualize-molecules
  sciencebench-097-formation-energy-prediction
  sciencebench-100-spatial-2
  sciencebench-102-refractive-index-prediction
)

python -m src.infer \
  --api-endpoint "${API_ENDPOINT}" \
  --model-path "${MODEL_PATH}" \
  --data-dir "${DATA_DIR}" \
  --benchmark science \
  --competitions "${TASKS[@]}" \
  --output-dir "${OUTPUT_DIR}" \
  --workspace-dir "${WORKSPACE_DIR}" \
  --max-turns "${MAX_TURNS}" \
  --temperature "${TEMPERATURE}"
