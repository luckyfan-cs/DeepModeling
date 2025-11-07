# ScienceBench Task 88

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Map Visualization
- Source: ResidentMario/geoplot
- Expected Output: `collisions_map_vis.png`
- Output Type: Image

## Task

Use the provided NYC fatal collision records and borough boundaries to create a choropleth or point map that highlights the 2016 fatal crashes. Match the styling of the reference figure that overlays incidents on the city map.

## Dataset

[START Dataset Preview: nyc_collisions_map]
|-- fatal_collisions.geojson
|-- nyc_boroughs.geojson
[END Dataset Preview]

## Submission Format

Encode the visualization as base64 and save it to `pred_results/collisions_map_vis.png`. Submit a CSV named `sample_submission.csv` with the columns `file_name` and `image_base64` referencing that PNG.

## Evaluation

The grader compares the decoded image against the gold reference with a GPT-based judge (score ≥ 60 required) and falls back to a deterministic pixel metric when the judge is unavailable.
