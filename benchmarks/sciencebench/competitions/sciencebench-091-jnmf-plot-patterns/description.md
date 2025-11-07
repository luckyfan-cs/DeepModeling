# ScienceBench Task 91

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Data Visualization
- Source: brand-d/cogsci-jnmf
- Expected Output: `patterns_conscientiousness.png`
- Output Type: Image

## Task

Use the provided factor matrices to visualise conscientiousness patterns extracted via joint NMF. Plot the high, shared, and low patterns as three heatmaps (left to right), each reshaped from a vector into a 64 × 9 grid.

## Dataset

[START Dataset Preview: jnmf_visualization]
|-- fit_result_conscientiousness_W_high.npy
|-- fit_result_conscientiousness_W_low.npy
[END Dataset Preview]

## Submission Format

Encode the composed figure as base64 and save it to `pred_results/patterns_conscientiousness.png`. Submit `sample_submission.csv` with columns `file_name` and `image_base64` referencing that PNG.

## Evaluation

The grader compares the decoded image with the gold reference via a GPT-based judge (score ≥ 60 required) with a deterministic fallback when the judge is unavailable.
