#!/bin/bash
# Quick start script for testing inference

set -e

echo "============================================"
echo "DeepModeling Inference Quick Start"
echo "============================================"
echo ""

# Check if model path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <model_path> [task_id]"
    echo ""
    echo "Examples:"
    echo "  # Test on single task using API endpoint"
    echo "  $0 Qwen/Qwen2.5-7B-Instruct industry-0 --api-endpoint http://localhost:8000"
    echo ""
    echo "  # Test on single task using local model"
    echo "  $0 /path/to/model industry-0 --use-local-model"
    echo ""
    echo "  # Test on multiple tasks (limit 3)"
    echo "  $0 Qwen/Qwen2.5-7B-Instruct --task-limit 3"
    exit 1
fi

MODEL_PATH="$1"
TASK_ID="${2:-}"
shift 2 || shift 1

# Default configuration for quick testing
MAX_TURNS=5
TEMPERATURE=0.0
BENCHMARK="engineering"

echo "Configuration:"
echo "  Model: $MODEL_PATH"
echo "  Benchmark: $BENCHMARK"
echo "  Max turns: $MAX_TURNS"
echo "  Temperature: $TEMPERATURE"
if [ -n "$TASK_ID" ]; then
    echo "  Task ID: $TASK_ID"
else
    echo "  Mode: Multiple tasks"
fi
echo ""

# Run inference
if [ -n "$TASK_ID" ]; then
    python -m src.infer \
        --model-path "$MODEL_PATH" \
        --max-turns $MAX_TURNS \
        --temperature $TEMPERATURE \
        --benchmark $BENCHMARK \
        --task-id "$TASK_ID" \
        "$@"
else
    python -m src.infer \
        --model-path "$MODEL_PATH" \
        --max-turns $MAX_TURNS \
        --temperature $TEMPERATURE \
        --benchmark $BENCHMARK \
        "$@"
fi

echo ""
echo "============================================"
echo "Inference completed!"
echo "Results saved to ./results/"
echo "Workspaces saved to ./workspace_infer/"
echo "============================================"
