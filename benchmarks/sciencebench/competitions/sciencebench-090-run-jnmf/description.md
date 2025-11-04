# ScienceBench Task 90

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis
- Source: brand-d/cogsci-jnmf
- Expected Output: fit_result_conscientiousness_H_high.npy
- Output Type: Tabular

## Task

Perform Non-negative matrix factorization for the matrices X1 and X2 given in jnmf_data. X1 should be factorized into two matrices W_high and H_high, where the product of W_high and H_high's transpose should be close to X1. Similarly, X2 should be factorized into W_low and H_low.

## Dataset

[START Preview of jnmf_data/X1_conscientiousness.npy]
[[1. 1. 1. ... 1. 1. 1.]
 [0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 ...
 [0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 [1. 1. 1. ... 1. 0. 1.]]
 [END Preview of jnmf_data/X1_conscientiousness.npy]

[START Preview of jnmf_data/X2_conscientiousness.npy]
[[1. 1. 1. ... 1. 1. 1.]
 [0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 ...
 [0. 0. 1. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 [1. 1. 0. ... 1. 1. 1.]]
 [END Preview of jnmf_data/X2_conscientiousness.npy]

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Negative root mean squared error (closer to zero is better).
