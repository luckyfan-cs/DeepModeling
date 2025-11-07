# ScienceBench Task 47

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Geospatial Analysis, Map Visualization
- Source: geopandas/geopandas
- Expected Output: distance_to_habitat.png
- Output Type: Image

## Task

Calculate road distance for the habitat polygons and map the results. Export the visualization to `pred_results/distance_to_habitat.png`.

## Dataset

[START Dataset Preview: MountainLionNew]
|-- Mountain_Lion_Habitat.geojson
|-- road.geojson
|-- distance_to_roads.tif
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with `distance_to_habitat.png`.

## Evaluation

The grader decodes the submitted image, compares it against the reference visualization, and accepts the submission when the similarity score meets or exceeds 60.
