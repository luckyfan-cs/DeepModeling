# ScienceBench Task 55

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Geospatial Analysis, Map Visualization
- Source: SciTools/iris
- Expected Output: ocean_profiles_vis.png
- Output Type: Image

## Task

Use sea temperature and salinity data from the South Atlantic Ocean to calculate and plot a vertical temperature-salinity profile within a specified range of latitude, longitude, and depth.

## Dataset

[START Preview of ocean_profiles/atlantic_profiles.nc]
 lat: [-9.833798, -8.167144, -6.500489, ...]
 lon: [0.5, 325.5, 330.5, ...]
 salinity:
 [[[35.98895263671875, 36.721397399902344, 36.43146896362305, ...]
 [35.96759033203125, 36.57795715332031, 36.29718780517578, ...]
 [35.869930267333984, 36.48030090332031, 36.23310089111328, ...]...]...]
 ...
 [END Preview of ocean_profiles/atlantic_profiles.nc]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
