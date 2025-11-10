#!/bin/bash
# MLEBench Individual Tasks Test Script
# This script allows running each selected task individually

cd /home/aiops/liufan/projects/DeepModeling

# Check if task name is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <task_number>"
    echo ""
    echo "Available tasks:"
    echo "  1 - aptos2019-blindness-detection (医疗影像 - 糖尿病视网膜病变)"
    echo "  2 - plant-pathology-2020-fgvc7 (计算机视觉 - 植物病理学)"
    echo "  3 - us-patent-phrase-to-phrase-matching (NLP - 专利短语匹配)"
    echo "  4 - new-york-city-taxi-fare-prediction (回归 - 出租车票价预测)"
    echo "  5 - tabular-playground-series-dec-2021 (表格数据竞赛)"
    echo ""
    echo "Example: $0 1"
    exit 1
fi

case $1 in
    1)
        TASK="aptos2019-blindness-detection"
        DESC="APTOS 2019 糖尿病视网膜病变检测"
        ;;
    2)
        TASK="plant-pathology-2020-fgvc7"
        DESC="植物病理学 2020 - 叶片病害分类"
        ;;
    3)
        TASK="us-patent-phrase-to-phrase-matching"
        DESC="美国专利短语匹配"
        ;;
    4)
        TASK="new-york-city-taxi-fare-prediction"
        DESC="纽约市出租车票价预测"
        ;;
    5)
        TASK="tabular-playground-series-dec-2021"
        DESC="表格数据游乐场系列 (2021年12月)"
        ;;
    *)
        echo "Error: Invalid task number. Please choose 1-5."
        exit 1
        ;;
esac

echo "=========================================="
echo "Running MLEBench Task"
echo "=========================================="
echo "Task: $TASK"
echo "Description: $DESC"
echo "=========================================="
echo ""

python main.py \
  --workflow scientific \
  --benchmark mle \
  --data-dir ./benchmarks/mlebench/competitions \
  --task $TASK

echo ""
echo "=========================================="
echo "Task Completed: $DESC"
echo "=========================================="
