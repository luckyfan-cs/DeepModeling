# ScienceBench Task 75

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Engineering, Machine Learning, Data Visualization
- Source: scverse/scvi-tutorials
- Output Type: Image

## Task

Train the amortized Latent Dirichlet Allocation (LDA) model with 10 topics on the PBMC 10K dataset. After fitting the model, compute topic proportions for every cell and visualise them with UMAP, highlighting the learned topics.

## Dataset

The PBMC dataset is provided as `pbmc/pbmc_10k_protein_v3.h5ad`, an AnnData object containing RNA and protein counts. Use it to reproduce the preprocessing, model training, and embedding steps required by the original notebook.

## Submission Format

Write the submission CSV with columns `file_name` and `image_base64`. Encode the generated PNG (`topic_modeling_pred.png`) to base64, and store the resulting UTF-8 string in the `image_base64` column joined with the expected file name.

## Evaluation

The grader decodes the image, resizes it to match the gold reference, and approves the submission when the similarity score reaches at least 0.60 on the proxy metric.
