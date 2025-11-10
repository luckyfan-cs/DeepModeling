#!/bin/bash
# Run DeepModeling inference on trained models

set -e

# Default values
MODEL_PATH=""
API_ENDPOINT=""
USE_LOCAL_MODEL=false
MAX_TURNS=10
TEMPERATURE=0.0
BENCHMARK="engineering"
TASK_ID=""
COMPETITIONS=""
TASK_LIMIT=""
WORKSPACE_DIR="./workspace_infer"
OUTPUT_DIR="./results"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --model-path)
            MODEL_PATH="$2"
            shift 2
            ;;
        --api-endpoint)
            API_ENDPOINT="$2"
            shift 2
            ;;
        --use-local-model)
            USE_LOCAL_MODEL=true
            shift
            ;;
        --max-turns)
            MAX_TURNS="$2"
            shift 2
            ;;
        --temperature)
            TEMPERATURE="$2"
            shift 2
            ;;
        --benchmark)
            BENCHMARK="$2"
            shift 2
            ;;
        --task-id)
            TASK_ID="$2"
            shift 2
            ;;
        --competitions)
            shift
            COMPETITIONS=""
            while [[ $# -gt 0 ]] && [[ ! "$1" =~ ^-- ]]; do
                COMPETITIONS="$COMPETITIONS $1"
                shift
            done
            ;;
        --task-limit)
            TASK_LIMIT="$2"
            shift 2
            ;;
        --workspace-dir)
            WORKSPACE_DIR="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Build command
CMD="python -m src.infer"

if [ -n "$MODEL_PATH" ]; then
    CMD="$CMD --model-path $MODEL_PATH"
fi

if [ -n "$API_ENDPOINT" ]; then
    CMD="$CMD --api-endpoint $API_ENDPOINT"
fi

if [ "$USE_LOCAL_MODEL" = true ]; then
    CMD="$CMD --use-local-model"
fi

CMD="$CMD --max-turns $MAX_TURNS"
CMD="$CMD --temperature $TEMPERATURE"
CMD="$CMD --benchmark $BENCHMARK"
CMD="$CMD --workspace-dir $WORKSPACE_DIR"
CMD="$CMD --output-dir $OUTPUT_DIR"

if [ -n "$TASK_ID" ]; then
    CMD="$CMD --task-id $TASK_ID"
fi

if [ -n "$COMPETITIONS" ]; then
    CMD="$CMD --competitions$COMPETITIONS"
fi

if [ -n "$TASK_LIMIT" ]; then
    CMD="$CMD --task-limit $TASK_LIMIT"
fi

echo "Running inference with command:"
echo "$CMD"
echo ""

eval $CMD
