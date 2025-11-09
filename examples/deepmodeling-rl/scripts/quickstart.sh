#!/bin/bash
# examples/deepmodeling-rl/quickstart.sh
# Quick start script for DeepModeling RL training

set -e

echo "==================================="
echo "DeepModeling RL Quick Start"
echo "==================================="

# 1. Parse inputs / defaults
BENCHMARK="${1:-engineering}"
MODE="${2:-fast}"
REQUESTED_GPU_COUNT="${3:-}"
DEFAULT_GPUS_PER_NODE=8
WORKSPACE_DIR="${WORKSPACE_DIR:-../workspace}"
DATA_ROOT="${DATA_ROOT:-../../../data/engineering-bench/competitions}"

if [ -n "$REQUESTED_GPU_COUNT" ]; then
    GPUS_PER_NODE="$REQUESTED_GPU_COUNT"
elif [ -n "${DM_NUM_GPUS:-}" ]; then
    GPUS_PER_NODE="$DM_NUM_GPUS"
else
    GPUS_PER_NODE="$DEFAULT_GPUS_PER_NODE"
fi

if ! [[ "$GPUS_PER_NODE" =~ ^[0-9]+$ ]] || [ "$GPUS_PER_NODE" -lt 1 ]; then
    echo "GPUS_PER_NODE must be a positive integer (got '$GPUS_PER_NODE')." >&2
    exit 1
fi

build_gpu_list() {
    local count="$1"
    local list=""
    local idx
    for ((idx = 0; idx < count; idx++)); do
        if [ -n "$list" ]; then
            list+=","
        fi
        list+="$idx"
    done
    printf "%s" "$list"
}

if [ "${PRESERVE_CUDA_VISIBLE_DEVICES:-0}" != "1" ]; then
    export CUDA_VISIBLE_DEVICES="$(build_gpu_list "$GPUS_PER_NODE")"
fi

if [ -z "${CUDA_VISIBLE_DEVICES:-}" ]; then
    echo "CUDA_VISIBLE_DEVICES is empty even after initialization; aborting." >&2
    exit 1
fi

IFS=',' read -r -a _visible_gpu_array <<<"$CUDA_VISIBLE_DEVICES"
VISIBLE_GPU_COUNT="${#_visible_gpu_array[@]}"
if [ "$VISIBLE_GPU_COUNT" -ne "$GPUS_PER_NODE" ]; then
    echo "Configured GPUS_PER_NODE=$GPUS_PER_NODE but CUDA_VISIBLE_DEVICES exposes $VISIBLE_GPU_COUNT GPUs ($CUDA_VISIBLE_DEVICES)." >&2
    echo "Set PRESERVE_CUDA_VISIBLE_DEVICES=1 if you intentionally want a subset, or rerun without it to expose $GPUS_PER_NODE GPUs." >&2
    exit 1
fi

export DM_NUM_GPUS="$GPUS_PER_NODE"

if command -v nvidia-smi >/dev/null 2>&1; then
    echo ""
    echo "[1/4] Detected GPUs:"
    nvidia-smi -L || true
else
    echo ""
    echo "[1/4] nvidia-smi not found; skipping GPU listing."
fi

# 2. Check Python environment
echo ""
echo "[2/4] Checking Python environment..."
conda run -n dm-env python --version

echo ""
echo "[3/4] Configuration:"
echo "  Benchmark: $BENCHMARK"
echo "  Mode: $MODE"
echo "  Workspace: $WORKSPACE_DIR"
echo "  Data root: $DATA_ROOT"
echo "  GPUs per node: $GPUS_PER_NODE"
echo "  CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"

# 4. Run training
echo ""
echo "[4/4] Starting RL training..."
echo ""

export RAY_RUNTIME_ENV_AGENT_DISABLED=1
cd .. && python -m src.train "$MODE" \
    --benchmark "$BENCHMARK" \
    --split engineering_mini \
    --n-runners 1 \
    --max-turns 2 \
    --workspace-dir "$WORKSPACE_DIR" \
    --val-temperature 0.0

echo ""
echo "==================================="
echo "Training completed!"
echo "==================================="
