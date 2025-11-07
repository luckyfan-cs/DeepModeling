# ScienceBench Task 96

## Overview

- Domain: Bioinformatics
- Subtask Categories: Data Visualization
- Source: scverse/scanpy-tutorials
- Expected Output: scatter_pred.png
- Output Type: Image

## Task

Analyze the preprocessed PBMC dataset with precomputed UMAP components for 700 cells and 765 highly variable genes. Compute clusters using the Leiden method and visualize the clustering results with UMAP. Save the figure to "output file".

## Dataset

[START Preview of pbmc68k/pbmc68k_reduced.h5ad, which is an AnnData object]

AnnData object with n_obs × n_vars = 700 × 765
    obs: 'bulk_labels', 'n_genes', 'percent_mito', 'n_counts', 'S_score', 'G2M_score', 'phase', 'louvain'
    var: 'n_counts', 'means', 'dispersions', 'dispersions_norm', 'highly_variable'
    uns: 'bulk_labels_colors', 'louvain', 'louvain_colors', 'neighbors', 'pca', 'rank_genes_groups'
    obsm: 'X_pca', 'X_umap'
    varm: 'PCs'
    obsp: 'distances', 'connectivities'

[END Preview of pbmc68k/pbmc68k_reduced.h5ad]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader compares the decoded image with the gold reference using a GPT-based judge (score ≥ 60) and falls back to a deterministic similarity metric if the judge is unavailable.
