# ScienceBench Task 50

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: ajdawson/eofs/
- Expected Output: EOF_xarray_sst.png
- Output Type: Image

## Task

Compute and plot the leading Empirical Orthogonal Function (EOF) of sea surface temperature in the central and northern Pacific during winter time. The associated time series shows large peaks and troughs for well-known El Nino and La Nina events.

## Dataset

[START Preview of EOF_xarray_sst/sst_ndjfm_anom.nc]
root group (NETCDF3_CLASSIC data model, file format NETCDF3):
    Conventions: CF-1.0
    dimensions(sizes): time(50), bound(2), latitude(18), longitude(30)
    variables(dimensions): float64 time(time), float64 bounds_time(time, bound), float32 latitude(latitude), float64 bounds_latitude(latitude, bound), float32 longitude(longitude), float64 bounds_longitude(longitude, bound), float64 sst(time, latitude, longitude)
    groups:
[END Preview of EOF_xarray_sst/sst_ndjfm_anom.nc]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
