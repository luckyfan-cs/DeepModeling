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

[START Preview of scirpy_3k/3kdata.h5ad, which is an MuData object]

MuData object with n_obs × n_vars = 3000 × 30727
  2 modalities
    gex:        3000 x 30727
      obs:        'cluster_orig', 'patient', 'sample', 'source'
      uns:        'cluster_orig_colors'
      obsm:        'X_umap_orig'
    airr:        3000 x 0
      obs:        'high_confidence', 'is_cell', 'clonotype_orig'
      obsm:        'airr'

[END Preview of scirpy_3k/3kdata.h5ad]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
