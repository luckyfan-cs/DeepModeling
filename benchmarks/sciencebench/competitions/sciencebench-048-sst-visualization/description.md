# ScienceBench Task 48

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Computational Analysis, Map Visualization
- Source: ajdawson/eofs/
- Expected Output: sst_visualization_pred.png
- Output Type: Image

## Task

Compute and plot the leading Empirical Orthogonal Function (EOF) of sea surface temperature in the central and northern Pacific during winter time.

## Dataset

[START Preview of sea_surface_temperature/sst_anom.nc]
 latitude: [-22.5, -17.5, -12.5, ...]
 longitude: [117.5, 122.5, 127.5, ...]
 sst:
 [[[0.43180797846112035, --, --, ...]
 [0.0385165550554825, 0.10425166469930812, --, ...]
 [-0.19866888195473625, 0.0899933837107475, 0.3353907402777514, ...]...]...]
 ...
 [END Preview of sea_surface_temperature/sst_anom.nc]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
