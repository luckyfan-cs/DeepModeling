#!/bin/bash
# Verify Sample Tasks
# This script verifies that all tasks in the sample test scripts exist

set -e

PROJECT_DIR="/home/aiops/liufan/projects/DeepModeling"
BENCH_DIR="$PROJECT_DIR/benchmarks"

echo "Verifying sample tasks existence..."
echo ""

# Function to check task existence
check_tasks() {
    local benchmark=$1
    local comp_dir=$2
    local tasks=$3
    local total=0
    local found=0
    local missing=0

    echo "Checking $benchmark tasks in $comp_dir..."

    for task in $tasks; do
        total=$((total + 1))
        if [ -d "$comp_dir/$task" ]; then
            found=$((found + 1))
        else
            echo "  [MISSING] $task"
            missing=$((missing + 1))
        fi
    done

    echo "  Total: $total | Found: $found | Missing: $missing"
    echo ""

    return $missing
}

# Check Engineering Benchmark
ENGINEERING_TASKS="industry-0 industry-3 industry-6 industry-9 industry-12 industry-15 industry-18 industry-21 industry-24 industry-27 industry-30 industry-33 industry-36 industry-39 industry-42 industry-45 industry-48 industry-51 industry-54 industry-57 industry-60 industry-63 industry-66 industry-69 industry-72 industry-75 industry-78 industry-81 industry-84 industry-87"
check_tasks "Engineering" "$BENCH_DIR/engineeringbench/competitions" "$ENGINEERING_TASKS"
eng_missing=$?

# Check Math Modeling Benchmark - BWOR
BWOR_TASKS="bwor-0 bwor-5 bwor-10 bwor-15 bwor-20 bwor-25 bwor-30 bwor-35 bwor-40 bwor-45 bwor-50 bwor-55 bwor-60 bwor-65 bwor-70 bwor-75 bwor-80"
check_tasks "Math Modeling (bwor)" "$BENCH_DIR/mathmodelingbench/competitions" "$BWOR_TASKS"
bwor_missing=$?

# Check Math Modeling Benchmark - mamo-easy (sample)
EASY_TASKS="mamo-easy-0 mamo-easy-10 mamo-easy-100 mamo-easy-200 mamo-easy-300 mamo-easy-400 mamo-easy-500 mamo-easy-600 mamo-easy-650"
check_tasks "Math Modeling (mamo-easy sample)" "$BENCH_DIR/mathmodelingbench/competitions" "$EASY_TASKS"
easy_missing=$?

# Check Science Benchmark (sample)
SCIENCE_TASKS="sciencebench-001-clintox-nn sciencebench-010-toronto-new sciencebench-040-md-rf sciencebench-070-single-cell-analysis-de sciencebench-100-spatial-2"
check_tasks "Science (sample)" "$BENCH_DIR/sciencebench/competitions" "$SCIENCE_TASKS"
sci_missing=$?

# Check MLE DA-Bench (sample)
DABENCH_TASKS="dabench-0-mean-fare dabench-108-generate-feature-called dabench-243-what-mean-batting dabench-424-develop-machine-learning dabench-604-identify-remove-outliers dabench-759-median-range-maximum"
check_tasks "MLE DA-Bench (sample)" "$BENCH_DIR/mlebench/competitions" "$DABENCH_TASKS"
dabench_missing=$?

total_missing=$((eng_missing + bwor_missing + easy_missing + sci_missing + dabench_missing))

echo "=========================================="
if [ $total_missing -eq 0 ]; then
    echo "✓ All sample tasks verified successfully!"
else
    echo "✗ Found $total_missing missing tasks"
    echo "Please check the task names in the test scripts"
fi
echo "=========================================="

exit $total_missing
