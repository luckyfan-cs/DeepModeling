# ScienceBench Task 54

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Map Visualization
- Source: rasterio/rasterio
- Expected Output: mountainLionCorridor.png
- Output Type: Image

## Task

Integrate ruggedness, road distance, land cover, and protected status into a single cost surface. Assign weights to each criterion to create a comprehensive habitat suitability map. Save the composite cost surface as "output file".

## Dataset

 [START Preview of dataset/distance.tif]
array([[ 0,  0,  0, ...,  8,  8,  8],
       [ 0,  0,  0, ...,  8,  8,  8],
       [ 0,  0,  0, ...,  8,  8,  8],
       ...,
       [ 6,  6,  6, ..., 10, 10, 10],
       [ 6,  6,  6, ..., 10, 10, 10],
       [ 6,  6,  6, ..., 10, 10, 10]], dtype=uint8)
 [EnD Preview of dataset/distance.tif]

[START Preview of dataset/ruggedness.tif]
array([[0, 2, 2, ..., 1, 1, 1],
       [1, 4, 4, ..., 1, 1, 1],
       [2, 4, 4, ..., 1, 1, 0],
       ...,
       [0, 0, 0, ..., 4, 4, 4],
       [0, 0, 0, ..., 4, 4, 4],
       [0, 0, 0, ..., 0, 0, 0]], dtype=uint8)
[EnD Preview of dataset/ruggedness.tif]

[START Preview of dataset/landcover_reclassified.tif]
array([[3, 3, 3, ..., 7, 7, 8],
       [3, 3, 3, ..., 7, 8, 8],
       [1, 3, 3, ..., 7, 8, 8],
       ...,
       [0, 0, 0, ..., 9, 9, 8],
       [0, 0, 0, ..., 9, 9, 9],
       [0, 0, 0, ..., 9, 9, 9]], dtype=uint8)
[EnD Preview of dataset/landcover_reclassifie.tif]

[START Preview of dataset/protected_status_reclassifie.tif]
array([[ 9,  9,  9, ...,  1,  1,  1],
       [ 9,  9,  9, ...,  1,  1,  1],
       [ 9,  9,  9, ...,  1,  1,  1],
       ...,
       [ 1,  1,  1, ..., 10, 10, 10],
       [ 1,  1,  1, ..., 10, 10, 10],
       [ 1,  1,  1, ..., 10, 10, 10]], dtype=uint8)
[EnD Preview of dataset/protected_status_reclassifie.tif]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
