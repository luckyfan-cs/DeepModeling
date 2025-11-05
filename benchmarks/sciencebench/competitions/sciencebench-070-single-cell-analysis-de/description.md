# ScienceBench Task 70

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Engineering, Deep Learning, Data Visualization
- Source: scverse/scvi-tutorials
- Output Type: Image

## Task

Train a variational autoencoder (VAE) on the Heart Cell Atlas subset, perform one-vs-all differential expression for each cell type, select top markers, and visualize them in a dendrogram-organized dot plot. Save the visualization to the required PNG output path.

## Dataset

The `hca/` directory contains the AnnData file `hca_subsampled_20k.h5ad` with expression counts and cell-type annotations for ~20k cells.

## Submission Format

Write `pred_results/hca_cell_type_de.png`. If base64 is used internally, ensure the final dot plot image is written to disk under the expected filename.

## Evaluation

Submissions are accepted when the rendered plot reaches the reference similarity score (60/100) compared against the gold visualization.
