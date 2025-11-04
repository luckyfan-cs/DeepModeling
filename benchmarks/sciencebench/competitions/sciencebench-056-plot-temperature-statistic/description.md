# ScienceBench Task 56

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Geospatial Analysis, Map Visualization
- Source: SciTools/iris
- Expected Output: temperature_statistic_vis.png
- Output Type: Image

## Task

Use 240 years of annual average surface temperature data from North America to calculate and plot the number of occurrences where the temperature exceeds 280K for five consecutive years.

## Dataset

[START Preview of temperature_statistic/E1_north_america.nc]
 latitude: [15, 16.25, 17.5, ...]
 longitude: [225, 226.875, 228.75, ...]
 air_temperature:
 [[[296.07858, 296.17642, 296.25217, ...]
 [295.51743, 295.58868, 295.6807, ...]
 [294.92886, 294.98587, 295.02686, ...]...]...]
 ...
 [END Preview of temperature_statistic/E1_north_america.nc]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
