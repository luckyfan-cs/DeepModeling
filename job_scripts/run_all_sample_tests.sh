#!/bin/bash
# Run All Sample Tests
# This script runs all four benchmark sample tests sequentially

set -e  # Exit on error

echo "=========================================="
echo "Running All Benchmark Sample Tests"
echo "=========================================="
echo ""
echo "Total tasks to run: 243"
echo "  - Engineering: 30 tasks (30%)"
echo "  - Math Modeling: 145 tasks (11%)"
echo "  - Science: 35 tasks (34%)"
echo "  - MLE (DA-Bench): 33 tasks (13%)"
echo ""
echo "=========================================="

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Run Engineering Benchmark
echo ""
echo "=========================================="
echo "[1/4] Running Engineering Benchmark Sample Tests"
echo "=========================================="
bash "$SCRIPT_DIR/test_engineeringbench_sample.sh"

# Run Math Modeling Benchmark
echo ""
echo "=========================================="
echo "[2/4] Running Math Modeling Benchmark Sample Tests"
echo "=========================================="
bash "$SCRIPT_DIR/test_mathmodelingbench_sample.sh"

# Run Science Benchmark
echo ""
echo "=========================================="
echo "[3/4] Running Science Benchmark Sample Tests"
echo "=========================================="
bash "$SCRIPT_DIR/test_sciencebench_sample.sh"

# Run MLE DA-Bench
echo ""
echo "=========================================="
echo "[4/4] Running MLE DA-Bench Sample Tests"
echo "=========================================="
bash "$SCRIPT_DIR/test_mlebench_dabench_sample.sh"

echo ""
echo "=========================================="
echo "All Sample Tests Completed!"
echo "=========================================="
echo "Check results in: runs/benchmark_results/"
