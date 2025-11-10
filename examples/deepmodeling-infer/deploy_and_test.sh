#!/bin/bash
# Automated deployment and testing script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
MODEL_PATH=""
PORT=8000
BENCHMARK="engineering"
TASK=""
TASK_LIMIT=""
MAX_TURNS=10
TEMPERATURE=0.0
DEPLOY_BACKEND="vllm"
SKIP_DEPLOY=false

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            MODEL_PATH="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --benchmark)
            BENCHMARK="$2"
            shift 2
            ;;
        --task)
            TASK="$2"
            shift 2
            ;;
        --task-limit)
            TASK_LIMIT="$2"
            shift 2
            ;;
        --max-turns)
            MAX_TURNS="$2"
            shift 2
            ;;
        --temperature)
            TEMPERATURE="$2"
            shift 2
            ;;
        --backend)
            DEPLOY_BACKEND="$2"
            shift 2
            ;;
        --skip-deploy)
            SKIP_DEPLOY=true
            shift
            ;;
        --help)
            echo "Usage: $0 --model /path/to/model [options]"
            echo ""
            echo "Options:"
            echo "  --model PATH          Path to model (required)"
            echo "  --port PORT           API port (default: 8000)"
            echo "  --benchmark NAME      Benchmark name (default: engineering)"
            echo "  --task ID             Single task ID to test"
            echo "  --task-limit N        Number of tasks to test"
            echo "  --max-turns N         Max turns per task (default: 10)"
            echo "  --temperature FLOAT   Sampling temperature (default: 0.0)"
            echo "  --backend NAME        Deployment backend: vllm|transformers (default: vllm)"
            echo "  --skip-deploy         Skip deployment, use existing API"
            echo ""
            echo "Examples:"
            echo "  # Deploy and test single task"
            echo "  $0 --model /path/to/model --task industry-0"
            echo ""
            echo "  # Test 5 random tasks"
            echo "  $0 --model /path/to/model --task-limit 5"
            echo ""
            echo "  # Use existing API"
            echo "  $0 --skip-deploy --port 8000 --task industry-0"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate inputs
if [ "$SKIP_DEPLOY" = false ] && [ -z "$MODEL_PATH" ]; then
    print_error "Model path is required (use --model)"
    exit 1
fi

if [ -z "$TASK" ] && [ -z "$TASK_LIMIT" ]; then
    print_error "Either --task or --task-limit is required"
    exit 1
fi

# Print configuration
echo "============================================"
echo "DeepModeling Inference - Deploy & Test"
echo "============================================"
if [ "$SKIP_DEPLOY" = false ]; then
    echo "Model: $MODEL_PATH"
    echo "Backend: $DEPLOY_BACKEND"
fi
echo "Port: $PORT"
echo "Benchmark: $BENCHMARK"
if [ -n "$TASK" ]; then
    echo "Task: $TASK"
else
    echo "Task limit: $TASK_LIMIT"
fi
echo "Max turns: $MAX_TURNS"
echo "Temperature: $TEMPERATURE"
echo "============================================"
echo ""

# Step 1: Deploy model (if not skipped)
if [ "$SKIP_DEPLOY" = false ]; then
    print_info "Step 1: Deploying model..."
    
    # Check if port is already in use
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warn "Port $PORT is already in use"
        read -p "Kill existing process and continue? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            lsof -ti:$PORT | xargs kill -9
            sleep 2
        else
            print_error "Cannot proceed with port $PORT in use"
            exit 1
        fi
    fi
    
    # Deploy based on backend
    if [ "$DEPLOY_BACKEND" = "vllm" ]; then
        print_info "Deploying with vLLM..."
        
        # Check if vllm is installed
        if ! python -c "import vllm" 2>/dev/null; then
            print_error "vLLM not installed. Install with: pip install vllm"
            exit 1
        fi
        
        # Start vLLM in background
        nohup python -m vllm.entrypoints.openai.api_server \
            --model "$MODEL_PATH" \
            --host 0.0.0.0 \
            --port $PORT \
            --gpu-memory-utilization 0.5 \
            --max-model-len 4096 \
            > vllm.log 2>&1 &
        
        DEPLOY_PID=$!
        print_info "vLLM started (PID: $DEPLOY_PID)"
        
    elif [ "$DEPLOY_BACKEND" = "transformers" ]; then
        print_error "Transformers backend not yet implemented in this script"
        exit 1
    else
        print_error "Unknown backend: $DEPLOY_BACKEND"
        exit 1
    fi
    
    # Wait for API to be ready
    print_info "Waiting for API to be ready (this may take 2-3 minutes for large models)..."
    print_info "You can monitor progress with: tail -f vllm.log"
    MAX_WAIT=240
    WAITED=0
    while [ $WAITED -lt $MAX_WAIT ]; do
        if curl -s http://localhost:$PORT/v1/models > /dev/null 2>&1; then
            print_info "API is ready!"
            break
        fi
        sleep 2
        WAITED=$((WAITED + 2))
        echo -n "."
    done
    echo ""
    
    if [ $WAITED -ge $MAX_WAIT ]; then
        print_error "API failed to start within ${MAX_WAIT}s"
        print_error "Check vllm.log for details"
        exit 1
    fi
    
    # Test API
    print_info "Testing API..."
    if curl -s http://localhost:$PORT/v1/models | grep -q "object"; then
        print_info "API test passed!"
    else
        print_error "API test failed"
        exit 1
    fi
    
else
    print_info "Skipping deployment, using existing API at port $PORT"
    
    # Verify API is available
    if ! curl -s http://localhost:$PORT/v1/models > /dev/null 2>&1; then
        print_error "No API found at port $PORT"
        exit 1
    fi
    print_info "API verified!"
fi

echo ""

# Step 2: Run inference
print_info "Step 2: Running inference..."

# Build inference command
CMD="python main.py --workflow scientific --benchmark $BENCHMARK"
CMD="$CMD --llm-api http://localhost:$PORT"
CMD="$CMD --max-turns $MAX_TURNS"
CMD="$CMD --temperature $TEMPERATURE"

if [ -n "$TASK" ]; then
    CMD="$CMD --task $TASK"
else
    CMD="$CMD --task-limit $TASK_LIMIT"
fi

print_info "Executing: $CMD"
echo ""

# Run inference
$CMD

INFER_EXIT_CODE=$?

echo ""

# Step 3: Show results
if [ $INFER_EXIT_CODE -eq 0 ]; then
    print_info "Step 3: Inference completed successfully!"
    echo ""
    print_info "Results summary:"
    LATEST_SUMMARY=$(ls -t results/summary_*.json | head -1)
    if [ -f "$LATEST_SUMMARY" ]; then
        cat "$LATEST_SUMMARY" | jq '{
            total_tasks,
            successful,
            failed,
            success_rate: (.successful / .total_tasks * 100 | round),
            avg_grade: (.avg_grade | . * 10000 | round / 10000),
            avg_turns: (.avg_turns | . * 100 | round / 100)
        }'
    fi
else
    print_error "Inference failed with exit code $INFER_EXIT_CODE"
fi

echo ""

# Step 4: Cleanup prompt
if [ "$SKIP_DEPLOY" = false ]; then
    echo ""
    read -p "Stop the deployed model? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Stopping model service..."
        lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
        print_info "Model service stopped"
    else
        print_info "Model service still running on port $PORT"
        print_info "To stop later: lsof -ti:$PORT | xargs kill -9"
    fi
fi

echo ""
echo "============================================"
echo "Complete!"
echo "============================================"
echo "Results: results/"
echo "Workspaces: workspace_infer/"
if [ "$SKIP_DEPLOY" = false ]; then
    echo "Logs: vllm.log"
fi
echo "============================================"

exit $INFER_EXIT_CODE
