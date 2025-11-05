# ScienceBench Task 76

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Feature Engineering, Machine Learning, Map Visualization
- Source: Solve-Geosolutions/transform_2022
- Output Type: Image

## Task

Run a random-forest-based prospectivity analysis for tin–tungsten deposits across Tasmania. Prepare the geospatial layers, train and validate the classifier, and generate a probability map that highlights prospective areas. Target an AUC of at least 0.9 before exporting your final visualization.

## Dataset

The `MineralProspectivity/` directory contains the inputs required by the notebook:

- `sn_w_minoccs.gpkg` records known mineral occurrences.
- Raster layers such as `tasgrav_IR.tif`, `tasmag_TMI.tif`, and `tasrad_*` provide geophysical evidence grids.

Use these assets to reproduce the preprocessing, feature extraction, and model training steps from the source project.

## Submission Format

Write the submission CSV with columns `file_name` and `image_base64`. Encode the generated PNG (`mineral_prospectivity.png`) to base64, and store the resulting UTF-8 string alongside the expected file name.

## Evaluation

The grader decodes the submitted image, aligns it with the gold panorama, and accepts the run once the similarity proxy reaches at least 0.60.
