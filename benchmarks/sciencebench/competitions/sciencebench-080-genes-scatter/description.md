# ScienceBench Task 80

## Overview

- Domain: Bioinformatics
- Subtask Categories: Computational Analysis, Data Visualization
- Source: scverse/scanpy-tutorials
- Expected Output: genes_scatter.png
- Output Type: Image

## Task

For the data in provided, plot a scatter plot where the x-axis is the total number of counts per cell and the y-axis is number of genes found in the cell's expression counts. Color each point by the percentage of counts in that cell that are for mitochondrial genes.

## Dataset

[START Dataset Preview: violin]
|-- violin.h5ad
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
