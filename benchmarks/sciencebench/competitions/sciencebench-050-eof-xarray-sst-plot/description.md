# ScienceBench Task 50

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: ajdawson/eofs/
- Expected Output: EOF_xarray_sst.png
- Output Type: Image

## Task

Compute and plot the leading EOF of sea surface temperature anomalies using the xarray workflow, including the associated principal component time series. Export the figure to `pred_results/EOF_xarray_sst.png`.

## Dataset

[START Dataset Preview: EOF_xarray_sst]
|-- sst_ndjfm_anom.nc
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with `EOF_xarray_sst.png`.

## Evaluation

The grader decodes the submitted image, compares it against the reference visualization, and accepts the submission when the similarity score meets or exceeds 60.
