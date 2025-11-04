#!/bin/bash
################################################################################
# Example 5: External Data Storage
################################################################################
# This script demonstrates using external storage for large datasets
# Useful when data is too large to fit in the project directory
################################################################################

set -e  # Exit on error

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Configuration
WORKFLOW="scientific"
BENCHMARK="mathmodeling"
LLM_MODEL="gpt-4o-mini"
TASK="bwor-11"

# External storage path (customize this to your setup)
# Examples:
#   - Network storage: /mnt/nfs/datasets/mathmodeling-bench
#   - External drive:  /media/external_drive/mathmodeling-data
#   - Cloud mount:     /mnt/s3/mathmodeling-bench
EXTERNAL_DATA_DIR="${EXTERNAL_DATA_DIR:-/mnt/external_drive/mathmodeling-data}"

echo "============================================================"
echo "DeepModeling Example: External Data Storage"
echo "============================================================"
echo "Scenario: Large dataset stored on external storage"
echo "Task: $TASK"
echo "Model: $LLM_MODEL"
echo "External Data: $EXTERNAL_DATA_DIR"
echo "============================================================"
echo ""

# Check if external data directory exists
if [ ! -d "$EXTERNAL_DATA_DIR" ]; then
    echo "WARNING: External data directory not found: $EXTERNAL_DATA_DIR"
    echo ""
    echo "Please update EXTERNAL_DATA_DIR to point to your external storage."
    echo "Example locations:"
    echo "  - Network storage: /mnt/nfs/datasets/mathmodeling-bench"
    echo "  - External drive:  /media/external_drive/mathmodeling-data"
    echo "  - Cloud mount:     /mnt/s3/mathmodeling-bench"
    echo ""
    echo "Using fallback to local data directory..."
    EXTERNAL_DATA_DIR="./data/mathmodeling-bench"
fi

echo "Using data directory: $EXTERNAL_DATA_DIR"
echo ""

# Run the task with external data
python main.py \
  --workflow "$WORKFLOW" \
  --benchmark "$BENCHMARK" \
  --data-dir "$EXTERNAL_DATA_DIR" \
  --llm-model "$LLM_MODEL" \
  --task "$TASK"

echo ""
echo "============================================================"
echo "Task completed!"
echo ""
echo "Architecture Benefits:"
echo "  ✓ Registry (small):  Stored in project (benchmarks/)"
echo "  ✓ Data (large):      Stored externally ($EXTERNAL_DATA_DIR)"
echo "  ✓ Results:           Stored in project (runs/)"
echo ""
echo "This allows:"
echo "  - Large datasets on cheap storage"
echo "  - Fast project repository"
echo "  - Shared data across multiple projects"
echo "============================================================"
