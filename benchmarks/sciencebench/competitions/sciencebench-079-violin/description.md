# ScienceBench Task 79

## Overview

- Domain: Bioinformatics
- Subtask Categories: Computational Analysis, Data Visualization
- Source: scverse/scanpy-tutorials
- Expected Output: violin.png
- Output Type: Image

## Task

Using the data provided, compute for each cell the number of genes found in the cell's expression counts. Plot the distribution of this computation using a violin plot. Overlay the violin plot with a strip plot showing the same data.

## Dataset

[START Dataset Preview: violin]
|-- violin.h5ad
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
