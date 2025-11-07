# ScienceBench Task 82

## Overview

- Domain: Bioinformatics
- Subtask Categories: Data Visualization
- Source: scverse/scanpy-tutorials
- Expected Output: dendrogram.png
- Output Type: Image

## Task

For the given data in 'pbmc_umap/pbmc.h5ad', visualize the dendrogram of the 'bulk_labels' variable.

## Dataset

[START Dataset Preview: pbmc_umap]
|-- pbmc.h5ad
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
