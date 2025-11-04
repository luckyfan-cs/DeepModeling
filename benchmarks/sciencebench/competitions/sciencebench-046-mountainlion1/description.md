# ScienceBench Task 46

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Map Visualization
- Source: rasterio/rasterio
- Expected Output: ruggedness.png
- Output Type: Image

## Task

To evaluate mountain lion habitat suitability, calculate terrain ruggedness using elevation data.

## Dataset

[START Preview of dataset/Elevation.tif]
[[242 242 244 ... 135 135 135]
 [242 242 242 ... 135 136 136]
 [242 241 240 ... 136 136 136]
 ...
 [  0   0   0 ...   7   7   7]
 [  0   0   0 ...   3   3   3]
 [  0   0   0 ...   3   3   3]]
 [EnD Preview of dataset/Elevation.tif]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
