#!/bin/bash
# MLEBench - DA-Bench Sample Test Script
# Total tasks: 258 (dabench-0 to dabench-760, non-consecutive)
# Sample: 33 tasks (~13% sampling, covering diverse data analysis tasks)

cd /home/aiops/liufan/projects/DeepModeling

python main.py \
  --workflow scientific \
  --benchmark mle \
  --data-dir ./benchmarks/mlebench/competitions \
  --task \
    dabench-0-mean-fare \
    dabench-11-correlation-coefficient-between \
    dabench-27-identify-outliers-charges \
    dabench-55-what-mean-number \
    dabench-69-feature-engineering-creating \
    dabench-108-generate-feature-called \
    dabench-124-there-significant-difference \
    dabench-139-question-percentage-votes \
    dabench-178-comprehensive-data-preprocessing \
    dabench-216-mean-standard-deviation \
    dabench-243-what-mean-batting \
    dabench-268-meanpot-values-normally \
    dabench-282-correlation-analysis-given \
    dabench-320-what-mean-eventmsgtype \
    dabench-351-determine-correlation-coefficient \
    dabench-372-find-mean-median \
    dabench-412-feature-called-familysize \
    dabench-424-develop-machine-learning \
    dabench-446-what-mean-wind \
    dabench-466-there-correlation-between \
    dabench-495-outlier-detection-percentage \
    dabench-516-fare-distribution-skewed \
    dabench-527-what-average-male \
    dabench-551-what-mean-column \
    dabench-578-what-average-trading \
    dabench-604-identify-remove-outliers \
    dabench-651-there-outliers-coordinate \
    dabench-663-scatter-plot-high \
    dabench-674-build-machine-learning \
    dabench-716-data-preprocessing-dropping \
    dabench-727-machine-learning-techniques \
    dabench-738-distribution-column-credit \
    dabench-759-median-range-maximum
