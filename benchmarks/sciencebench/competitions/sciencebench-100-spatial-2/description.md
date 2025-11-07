# ScienceBench Task 100

## Overview

- Domain: Bioinformatics
- Subtask Categories: Statistical Analysis, Data Visualization
- Source: scverse/scanpy-tutorials
- Expected Output: spatial_2_pred.png
- Output Type: Image

## Task

You should visualize the data in spatial coordinates in three figures colored by total_counts, n_genes_by_counts, and clusters, respectively.

## Dataset

[START Preview of lymph/lymph_node.h5ad, which is an AnnData object]

MuData object with n_obs × n_vars = 3000 × 30727
  2 modalities
    gex:        3000 x 30727
      obs:        'cluster_orig', 'patient', 'sample', 'source'
      uns:        'cluster_orig_colors'
      obsm:        'X_umap_orig'
    airr:        3000 x 0
      obs:        'high_confidence', 'is_cell', 'clonotype_orig'
      obsm:        'airr'

[END Preview of lymph/lymph_node.h5ad]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader compares the decoded image with the gold reference using a GPT-based judge (score ≥ 60) and reverts to a deterministic similarity metric if the judge is unavailable.
