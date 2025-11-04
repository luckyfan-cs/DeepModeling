# ScienceBench Task 64

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Geospatial Analysis, Data Visualization
- Source: OGGM/tutorials
- Expected Output: plotting_flowline_mb_elevation_pred.png
- Output Type: Image

## Task

Show a plot comparing the flowline of region 'RGI60-11.00001' in year 2010 and 2005 with OGGM. The plot should show the mass-balance (MB, in mm w.e. per year) against elevation (in m a.s.i).

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
