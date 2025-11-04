# ScienceBench Task 49

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Computational Analysis, Map Visualization
- Source: ajdawson/eofs/
- Expected Output: EOF_standard.png
- Output Type: Image

## Task

Compute and plot the leading EOF of geopotential height on the 500 hPa pressure surface over the European/Atlantic sector during winter time.

## Dataset

[START Preview of EOF_standard/hgt_djf.nc]
root group (NETCDF3_CLASSIC data model, file format NETCDF3):
    Conventions: CF-1.0
    dimensions(sizes): time(65), bound(2), pressure(1), latitude(29), longitude(49)
    variables(dimensions): float64 time(time), float64 bounds_time(time, bound), float32 pressure(pressure), float32 latitude(latitude), float64 bounds_latitude(latitude, bound), float32 longitude(longitude), float64 bounds_longitude(longitude, bound), float64 z(time, pressure, latitude, longitude)
    groups:
[END Preview of EOF_standard/hgt_djf.nc]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
