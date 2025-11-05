# ScienceBench Task 69

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Engineering, Statistical Analysis, Data Visualization
- Source: scverse/scvi-tutorials
- Output Type: Image

## Task

Process the Heart Cell Atlas subset, filter lowly expressed genes, compute the top 30 PCA components, and generate a UMAP embedding colored by cell type. Save the visualization to the required PNG output path.

## Dataset

The `hca/` directory contains `hca_subsampled_20k.h5ad`, an AnnData object with expression values and cell-type annotations for a subsampled Heart Cell Atlas dataset.

## Submission Format

Write `pred_results/hca_cell_type_pca.png`. If the workflow works in base64 internally, ensure the image is finally written to disk with the expected filename.

## Evaluation

Submissions are accepted when the visualization achieves at least the reference similarity score (60/100) against the gold image produced by the evaluation script.
