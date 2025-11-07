# ScienceBench Task 98

## Overview

- Domain: Bioinformatics
- Subtask Categories: Computational Analysis, Data Visualization
- Source: scverse/scirpy
- Expected Output: 3k_pred.png
- Output Type: Image

## Task

Compute chain quality control information for this single-cell TCR/RNA-seq data collected from resected tumors, histologically normally adjacent tissues (NAT), and peripheral blood. Then, draw a stacked bar chart of the number of cells in each chain pairing, coloring each portion of the stack by the source (tumor, NAT, or blood).

## Dataset

[START Dataset Preview: cell_3k]
|-- 3kdata.h5mu
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader compares the decoded image with the gold reference using a GPT-based judge (score ≥ 60) and a deterministic fallback similarity check when the judge is unavailable.
