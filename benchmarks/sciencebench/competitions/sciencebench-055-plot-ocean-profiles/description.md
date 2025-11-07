# ScienceBench Task 55

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Geospatial Analysis, Map Visualization
- Source: SciTools/iris
- Output Type: Image

## Task

Use the South Atlantic temperature and salinity profiles to compute a vertical section for the requested latitude/longitude window. Visualise the resulting temperature–salinity relationship and save the figure to `pred_results/ocean_profiles_vis.png`.

## Dataset

[START Dataset Preview: ocean_profiles]
|-- atlantic_profiles.nc
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, compares it with the reference visualization, and marks the submission correct when the similarity score reaches at least 60.
