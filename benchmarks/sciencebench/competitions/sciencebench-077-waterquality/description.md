# ScienceBench Task 77

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Statistical Analysis, Map Visualization
- Source: Solve-Geosolutions/transform_2022
- Expected Output: interpolated_water_quality.png
- Output Type: Image

## Task

Model water quality using spatial interpolation techniques in Python. The analysis should focus on understanding spatial patterns of water quality by using point sample data and interpolating these values across a broader area including unsampled locations. Your goal is to load the water quality sample data, and apply appropriate spatial interpolation methods, such as Kriging, to predict water quality across the region. The final output should be a map showing the interpolated water quality surface, saved as "output file"

## Dataset

[START Dataset Preview: WaterQuality]
|-- Bay.geojson
|-- DissolvedO2.geojson
[END Dataset Preview]


## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
