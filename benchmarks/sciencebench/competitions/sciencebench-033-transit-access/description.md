# ScienceBench Task 33

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Map Visualization
- Source: geopandas/geopandas
- Expected Output: transit_access.png
- Output Type: Image

## Task

Overlay the bus service areas with block-level demographic layers (poverty, density, vehicle access) for Hamilton County, Tennessee. Derive transit accessibility indicators from the intersections and summarize them in the submission map with clear legends, labels, and context.

## Dataset

[START Dataset Preview: TransitAccessDemographic]
|-- BusServiceArea.geojson
|-- HamiltonDemographics.geojson
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes the submitted image, compares it against the reference visualization, and assigns a similarity score. Scores below 60 fail the evaluation.
