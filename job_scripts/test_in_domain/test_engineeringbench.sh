#!/bin/bash
# Engineering Benchmark Sample Test Script
# Total tasks: 100 (industry-0 to industry-99)
# Sample: 30 tasks (30% sampling, evenly distributed)

cd /home/aiops/liufan/projects/DeepModeling

python main.py \
  --workflow scientific \
  --benchmark engineeringbench \
  --data-dir ./data/engineering-bench/competitions \
  --task \
    industry-0 industry-3 industry-6 industry-9 industry-12 industry-15 industry-18 industry-21 industry-24 industry-27 \
    industry-30 industry-33 industry-36 industry-39 industry-42 industry-45 industry-48 industry-51 industry-54 industry-57 \
    industry-60 industry-63 industry-66 industry-69 industry-72 industry-75 industry-78 industry-81 industry-84 industry-87
