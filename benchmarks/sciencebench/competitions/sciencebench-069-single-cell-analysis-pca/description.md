# ScienceBench Task 69

## Overview

- Domain: Bioinformatics
- Subtask Categories: Dimensionality Reduction, Data Visualization
- Source: scverse/scvi-tutorials
- Output Type: Image

## Task

Process the Heart Cell Atlas subset, compute a PCA embedding, and colour the scatter plot by cell type. Save the figure to `pred_results/hca_cell_type_pca.png`.

## Dataset

[START Dataset Preview: hca]
|-- hca_subsampled_20k.h5ad
[END Dataset Preview]

## Submission Format

Create `sample_submission.csv` with columns `file_name` and `image_base64`. Provide one row for `hca_cell_type_pca.png`.

## Evaluation

The grader decodes the submitted figure, compares it with the reference visualization, and accepts the submission when the similarity score reaches at least 60.
