# ScienceBench Task 70

## Overview

- Domain: Bioinformatics
- Subtask Categories: Differential Expression, Data Visualization
- Source: scverse/scvi-tutorials
- Output Type: Image

## Task

Perform differential expression analysis on the Heart Cell Atlas subset and visualise the marker genes in a dot plot. Save the plot to `pred_results/hca_cell_type_de.png`.

## Dataset

[START Dataset Preview: hca]
|-- hca_subsampled_20k.h5ad
[END Dataset Preview]

## Submission Format

Create `sample_submission.csv` with columns `file_name` and `image_base64`. Provide one entry for `hca_cell_type_de.png`.

## Evaluation

The grader decodes the submission, compares it with the gold-standard plot, and accepts the result once the similarity score reaches 60.
