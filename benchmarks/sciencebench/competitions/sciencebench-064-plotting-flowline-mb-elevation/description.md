# ScienceBench Task 64

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Geospatial Analysis, Data Visualization
- Source: OGGM/tutorials
- Output Type: Image

## Task

Use OGGM outputs to compare the 2005 and 2010 flowline mass balance for glacier `RGI60-11.00001`. Plot mass balance (mm w.e. yr⁻¹) against elevation and save the figure to `pred_results/plotting_flowline_mb_elevation_pred.png`.

## Dataset

[START Dataset Preview: ocean_glacier]
|-- RGI60-11.00001/climate_historical.nc
|-- RGI60-11.00001/elevation_band_flowline.csv
|-- RGI60-11.00001/model_flowlines_dyn_melt_f_calib.pkl
|-- RGI60-11.00001/model_diagnostics_historical.nc
[END Dataset Preview]

## Submission Format

Create `sample_submission.csv` with columns `file_name` and `image_base64`, containing a single row for `plotting_flowline_mb_elevation_pred.png`.

## Evaluation

The grader decodes the submitted image, compares it to the reference plot, and accepts the submission when the similarity score is at least 60.
