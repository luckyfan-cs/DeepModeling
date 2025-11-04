#!/bin/bash
################################################################################
# Example 8: Advanced Options and Configurations
################################################################################
# This script demonstrates advanced configuration options:
# - Different LLM models
# - Custom parameters
# - Logging and debugging
# - Resource constraints
################################################################################

set -e  # Exit on error

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "============================================================"
echo "DeepModeling Example: Advanced Options"
echo "============================================================"
echo ""

# Example 1: Using different LLM models
echo "1. Different LLM Models:"
echo "   --llm-model gpt-4o-mini              # OpenAI (fast, cheap)"
echo "   --llm-model gpt-4o                   # OpenAI (powerful)"
echo "   --llm-model claude-3-5-sonnet-20241022  # Anthropic"
echo "   --llm-model deepseek-ai/DeepSeek-V3.1-Terminus  # DeepSeek"
echo ""

# Example 2: Configuration parameters
echo "2. Configuration Parameters:"
echo "   --workflow scientific                # Scientific method workflow"
echo "   --benchmark mathmodeling             # Or 'mle' for data science"
echo "   --data-dir /path/to/data             # Data directory"
echo "   --task task-id                       # Specific task ID"
echo ""

# Example 3: Environment variables
echo "3. Environment Variables (set in .env):"
echo "   OPENAI_API_KEY=sk-...                # OpenAI API key"
echo "   ANTHROPIC_API_KEY=sk-ant-...         # Anthropic API key"
echo "   OPENAI_API_BASE=https://...          # Custom API endpoint"
echo ""

# Example 4: Advanced usage - Multiple models comparison
echo "4. Example: Comparing Multiple Models"
echo "   Running same task with different models..."
echo ""

WORKFLOW="scientific"
BENCHMARK="mathmodeling"
DATA_DIR="./data/mathmodeling-bench"
TASK="bwor-0"

# Uncomment the models you want to test
MODELS=(
    "gpt-4o-mini"
    # "gpt-4o"
    # "claude-3-5-sonnet-20241022"
    # "deepseek-ai/DeepSeek-V3.1-Terminus"
)

for MODEL in "${MODELS[@]}"; do
    echo "----------------------------------------"
    echo "Testing with model: $MODEL"
    echo "----------------------------------------"

    python main.py \
      --workflow "$WORKFLOW" \
      --benchmark "$BENCHMARK" \
      --data-dir "$DATA_DIR" \
      --llm-model "$MODEL" \
      --task "$TASK" || echo "Model $MODEL failed (skipping)"

    echo ""
done

echo "============================================================"
echo "Advanced configuration examples completed!"
echo ""
echo "Tips:"
echo "  - Use cheaper models (gpt-4o-mini) for testing"
echo "  - Use powerful models (gpt-4o, claude) for production"
echo "  - Set OPENAI_API_BASE for custom endpoints"
echo "  - Check logs in runs/ for detailed execution traces"
echo "============================================================"
