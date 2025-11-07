# ScienceBench Task 81

## Overview

- Domain: Bioinformatics
- Subtask Categories: Data Visualization
- Source: scverse/scanpy-tutorials
- Expected Output: umap.png
- Output Type: Image

## Task

For the given gene expression dataset, perform a scatter plot in UMAP basis to visualize groups of cells that express popular marker genes across various cell types: T-cell, B-cell, plasma, monocytes and dendritic. Also add plots for number of UMI counts per cell and bulk labels per cell.

## Dataset

[START Dataset Preview: pbmc_umap]
|-- pbmc.h5ad
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
