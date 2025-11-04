# ScienceBench Task 75

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Engineering, Machine Learning, Data Visualization
- Source: scverse/scvi-tutorials
- Expected Output: topic_modeling_pred.png
- Output Type: Image

## Task

Train an amortized Latent Dirichlet Allocation (LDA) model with 10 topics on the PBMC 10K dataset. After training, compute topic proportions for each cell and visualize the topic proportions using UMAP.

## Dataset

[START Preview of pbmc/pbmc_10k_protein_v3.h5ad]
​                                    AL627309.1 AL669831.5  LINC00115 ...  AL354822.1 AC004556.1 AC240274.1
AAACCCAAGATTGTGA-1         0.0         0.0         0.0  ...         0.0         0.0         0.0
AAACCCACATCGGTTA-1         0.0         0.0         0.0  ...         0.0         0.0         0.0
AAACCCAGTACCGCGT-1         0.0         0.0         0.0  ...         0.0         0.0         0.0
...
[END Preview of pbmc/pbmc_10k_protein_v3.h5ad]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
