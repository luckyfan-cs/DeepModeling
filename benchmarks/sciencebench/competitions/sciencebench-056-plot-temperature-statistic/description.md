# ScienceBench Task 56

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Geospatial Analysis, Map Visualization
- Source: SciTools/iris
- Output Type: Image

## Task

Analyse 240 years of North American surface temperatures and plot where five-year windows exceed 280 K. Store the resulting visualization at `pred_results/temperature_statistic_vis.png`.

## Dataset

[START Dataset Preview: temperature_statistic]
|-- E1_north_america.nc
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, compares it to the reference, and awards full credit for similarity scores of 60 or higher.
