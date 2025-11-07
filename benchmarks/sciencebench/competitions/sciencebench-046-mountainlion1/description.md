# ScienceBench Task 46

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Map Visualization
- Source: rasterio/rasterio
- Expected Output: ruggedness.png
- Output Type: Image

## Task

Use the elevation raster to compute terrain ruggedness for the study area and visualise the result. Export the final map to `pred_results/ruggedness.png`.

## Dataset

[START Dataset Preview: MountainLionNew]
|-- Elevation.tif
|-- landcover_reclassified.tif
|-- ruggedness.tif
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with `ruggedness.png`.

## Evaluation

The grader decodes the submitted image, compares it against the reference visualization, and accepts the submission when the similarity score meets or exceeds 60.
