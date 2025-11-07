# ScienceBench Task 65

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Geospatial Analysis, Data Visualization
- Source: OGGM/tutorials
- Output Type: Image

## Task

Generate a time-series plot of OGGM surface mass balance for glacier `RGI60-11.00001`, covering 1960–2020. Save the figure to `pred_results/plotting_surface_mass_pred.png`.

## Dataset

[START Dataset Preview: ocean_glacier]
|-- RGI60-11.00001/model_diagnostics_historical.nc
|-- RGI60-11.00001/model_diagnostics_spinup_historical.nc
|-- RGI60-11.00001/reference_mb_results.csv
|-- RGI60-11.00001/gridded_data.nc
[END Dataset Preview]

## Submission Format

Create `sample_submission.csv` with columns `file_name` and `image_base64`. Include a single row for `plotting_surface_mass_pred.png`.

## Evaluation

The grader decodes your PNG, compares it with the reference plot, and accepts submissions with a similarity score of at least 60.
