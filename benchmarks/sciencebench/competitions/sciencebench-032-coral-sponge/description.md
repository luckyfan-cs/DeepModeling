# ScienceBench Task 32

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: rasterio/rasterio
- Expected Output: CoralandSponge.png
- Output Type: Image

## Task

Derive slope and aspect rasters from `CatalinaBathymetry.tif`, join those measurements to the coral and sponge observations, and aggregate mean slope/aspect per species. Present the summary in the submission image expected by the template, including clear legends, units, and map context for Catalina Island.

## Dataset

[START Dataset Preview: CoralSponge]
|-- CatalinaBathymetry.tif
|-- CatalinaBathymetry.tif.aux.xml
|-- CatalinaBathymetry.tif.vat.cpg
|-- CatalinaBathymetry.tif.vat.dbf
|-- CatalinaBathymetry.tfw
|-- CoralandSpongeCatalina.geojson
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes the submitted image, compares it against the reference visualization, and assigns a similarity score. Scores below 60 fail the evaluation.
