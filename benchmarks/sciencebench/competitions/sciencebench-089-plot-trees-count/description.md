# ScienceBench Task 89

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Map Visualization
- Source: ResidentMario/geoplot
- Expected Output: `trees_count_vis.png`
- Output Type: Image

## Task

Use the San Francisco street-tree inventory and borough polygons to compute the percentage of missing species labels per region and visualize the results as a quadtree map similar to the reference figure.

## Dataset

[START Dataset Preview: sfo_trees_count]
|-- street_trees_sample.geojson
|-- sfo_boroughs.geojson
[END Dataset Preview]

## Submission Format

Encode the visualization as base64 and save it to `pred_results/trees_count_vis.png`. Submit `sample_submission.csv` with columns `file_name` and `image_base64` that reference that PNG.

## Evaluation

The grader compares the decoded image against the gold reference using a GPT-based judge (minimum score 60) with a deterministic fallback metric when necessary.
