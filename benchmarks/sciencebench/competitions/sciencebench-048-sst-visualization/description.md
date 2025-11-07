# ScienceBench Task 48

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Computational Analysis, Map Visualization
- Source: ajdawson/eofs/
- Expected Output: sst_visualization_pred.png
- Output Type: Image

## Task

Compute and plot the leading Empirical Orthogonal Function (EOF) of winter sea surface temperature anomalies in the central and northern Pacific. Export the figure to `pred_results/sst_visualization_pred.png`.

## Dataset

[START Dataset Preview: sea_surface_temperature]
|-- sst_anom.nc
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with `sst_visualization_pred.png`.

## Evaluation

The grader decodes the submitted image, compares it against the reference visualization, and accepts the submission when the similarity score meets or exceeds 60.
