# ScienceBench Task 49

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Computational Analysis, Map Visualization
- Source: ajdawson/eofs/
- Expected Output: EOF_standard.png
- Output Type: Image

## Task

Compute and plot the leading EOF of 500 hPa geopotential height over the Euro‑Atlantic sector during winter. Export the figure to `pred_results/EOF_standard.png`.

## Dataset

[START Dataset Preview: EOF_standard]
|-- hgt_djf.nc
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with `EOF_standard.png`.

## Evaluation

The grader decodes the submitted image, compares it against the reference visualization, and accepts the submission when the similarity score meets or exceeds 60.
