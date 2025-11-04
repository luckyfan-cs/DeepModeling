# ScienceBench Task 70

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Engineering, Deep Learning, Computational Analysis, Data Visualization
- Source: scverse/scvi-tutorials
- Expected Output: hca_cell_type_de.png
- Output Type: Image

## Task

Train a VAE model on the given data and perform a 1-vs-all differential expression test for each cell type. Extract top markers for each cell type using the results. Visualize them as a dotplot with the cell types organized using a dendrogram.

## Dataset

[START Preview of hca/hca_subsampled_20k.h5ad]
                                    AL627309.1  AC114498.1  AL669831.2  ...  AL354822.1  AC004556.1  AC240274.1
AACTCCCCACGAGAGT-1-HCAHeart7844001         0.0         0.0         0.0  ...         0.0         0.0         0.0
ATAACGCAGAGCTGGT-1-HCAHeart7829979         0.0         0.0         0.0  ...         0.0         0.0         0.0 
GTCAAGTCATGCCACG-1-HCAHeart7702879         0.0         0.0         0.0  ...         0.0         0.0         0.0
...  
[END Preview of hca/hca_subsampled_20k.h5ad]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
