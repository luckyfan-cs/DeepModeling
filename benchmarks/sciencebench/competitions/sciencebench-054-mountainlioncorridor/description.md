# ScienceBench Task 54

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Map Visualization
- Source: rasterio/rasterio
- Output Type: Image

## Task

Combine ruggedness, road distance, reclassified land cover, and protected status into a cost surface that highlights mountain lion movement corridors. Produce a visual overlay of the corridor and export it to `pred_results/mountainLionCorridor.png`.

## Dataset

[START Dataset Preview: MountainLionNew]
|-- distance.tif
|-- distance_to_roads.tif
|-- landcover_reclassified.tif
|-- protected_status_reclassified.tif
|-- ruggedness.tif
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with two columns: `file_name` and `image_base64`. Encode the PNG visualization as base64 and associate it with the file name `mountainLionCorridor.png`.

## Evaluation

The grader decodes your visualization and measures its similarity against the reference image using the shared ScienceBench image-comparison utility (success threshold 60).
