# ScienceBench Task 65

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Geospatial Analysis, Data Visualization
- Source: OGGM/tutorials
- Expected Output: plotting_surface_mass_pred.png
- Output Type: Image

## Task

Show a time series plot for the mass-balance (MB) computed by OGGM for the region 'RGI60-11.00001' from 1960 to 2020.

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
