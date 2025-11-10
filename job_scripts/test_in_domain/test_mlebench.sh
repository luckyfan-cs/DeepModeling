#!/bin/bash
# MLEBench Selected Tasks Test Script
# This script runs 5 selected MLEBench competition tasks
# Tasks selected for comprehensive testing across different domains

cd /home/aiops/liufan/projects/DeepModeling

python main.py \
  --workflow scientific \
  --benchmark mle \
  --data-dir ./benchmarks/mlebench/competitions \
  --task \
    aptos2019-blindness-detection \
    plant-pathology-2020-fgvc7 \
    us-patent-phrase-to-phrase-matching \
    new-york-city-taxi-fare-prediction \
    tabular-playground-series-dec-2021
