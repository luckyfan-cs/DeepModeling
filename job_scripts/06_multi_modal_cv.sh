#!/bin/bash
################################################################################
# Example 6: Multi-Modal Data - Computer Vision
################################################################################
# This script demonstrates handling image data for computer vision tasks
# Example: Digit recognition (MNIST-style classification)
################################################################################

set -e  # Exit on error

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Configuration
WORKFLOW="scientific"
BENCHMARK="mle"
DATA_DIR="./data/mlebench"
LLM_MODEL="gpt-4o-mini"
TASK="digit-recognizer"

echo "============================================================"
echo "DeepModeling Example: Computer Vision (Image Data)"
echo "============================================================"
echo "Task: $TASK"
echo "Model: $LLM_MODEL"
echo "Data Modality: Images (PNG/JPG)"
echo "Task Type: Multi-class image classification"
echo "============================================================"
echo ""
echo "Dataset Structure:"
echo "  data/mlebench/competitions/digit-recognizer/"
echo "    ├── train/                # Training images (28x28 grayscale)"
echo "    ├── test/                 # Test images"
echo "    ├── train_labels.csv      # Image IDs and labels (0-9)"
echo "    └── sample_submission.csv # Expected format"
echo ""
echo "The framework will:"
echo "  1. Load and preprocess images automatically"
echo "  2. Design CNN architecture"
echo "  3. Train image classifier"
echo "  4. Generate predictions for test images"
echo "  5. Create submission file"
echo ""

# Run computer vision task
python main.py \
  --workflow "$WORKFLOW" \
  --benchmark "$BENCHMARK" \
  --data-dir "$DATA_DIR" \
  --llm-model "$LLM_MODEL" \
  --task "$TASK"

echo ""
echo "============================================================"
echo "Computer vision task completed!"
echo ""
echo "Image Processing Pipeline:"
echo "  ✓ Automatic image loading (PNG/JPG/TIFF)"
echo "  ✓ Image preprocessing and normalization"
echo "  ✓ CNN model architecture design"
echo "  ✓ Training with data augmentation"
echo "  ✓ Prediction on test images"
echo "  ✓ Submission file generation"
echo ""
echo "Results: runs/modeling_run_${TASK}_*/submission.csv"
echo "============================================================"
