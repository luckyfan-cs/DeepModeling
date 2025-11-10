#!/bin/bash
# Simple vLLM startup script

MODEL_PATH=${1:-/home/aiops/liufan/projects/models/dm-sft-Qwen2.5-7B-Instruct/merged}
PORT=${2:-8000}

echo "Starting vLLM..."
echo "Model: $MODEL_PATH"
echo "Port: $PORT"
echo ""

# Kill any existing vLLM process on this port
lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
sleep 2

# Start vLLM
nohup python -m vllm.entrypoints.openai.api_server \
    --model "$MODEL_PATH" \
    --host 0.0.0.0 \
    --port $PORT \
    --gpu-memory-utilization 0.7 \
    --max-model-len 8192 \
    --dtype bfloat16 \
    > vllm.log 2>&1 &

VLLM_PID=$!
echo "vLLM started (PID: $VLLM_PID)"
echo "Monitor with: tail -f vllm.log"
echo ""
echo "Waiting for API to be ready..."

# Wait for API
MAX_WAIT=180
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
    if curl -s http://localhost:$PORT/v1/models > /dev/null 2>&1; then
        echo ""
        echo "✓ vLLM API is ready!"
        echo ""
        curl http://localhost:$PORT/v1/models | jq .
        exit 0
    fi
    echo -n "."
    sleep 5
    WAITED=$((WAITED + 5))
done

echo ""
echo "✗ API failed to start within ${MAX_WAIT}s"
echo "Check vllm.log for details"
exit 1
