#!/bin/bash
# examples/deepmodeling-rl/quickstart.sh
# Quick start script for DeepModeling RL training

set -e

echo "==================================="
echo "DeepModeling RL Quick Start"
echo "==================================="

# 1. Check Python environment
echo ""
echo "[1/4] Checking Python environment..."
python --version

# 2. Install dependencies (if needed)
# if ! python -c "import agentlightning" 2>/dev/null; then
#     echo ""
#     echo "[2/4] Installing agent-lightning..."
#     pip install agentlightning
#     pip install "agentlightning[verl]"
#     pip install langgraph langchain langchain-core
# else
#     echo ""
#     echo "[2/4] agent-lightning already installed ✓"
# fi

# 3. Set defaults
BENCHMARK="${1:-engineering}"
MODE="${2:-fast}"
WORKSPACE_DIR="${WORKSPACE_DIR:-./workspace_rl}"
DATA_ROOT="${DATA_ROOT:-../../data/engineering-bench/competitions}"

echo ""
echo "[3/4] Configuration:"
echo "  Benchmark: $BENCHMARK"
echo "  Mode: $MODE"
echo "  Workspace: $WORKSPACE_DIR"
echo "  Data root: $DATA_ROOT"

# 4. Run training
echo ""
echo "[4/4] Starting RL training..."
echo ""

python train_deepmodeling.py "$MODE" \
    --benchmark "$BENCHMARK" \
    --split engineering_mini \
    --n-runners 1 \
    --max-turns 3 \
    --workspace-dir "$WORKSPACE_DIR" \
    --val-temperature 0.0

echo ""
echo "==================================="
echo "Training completed!"
echo "==================================="
