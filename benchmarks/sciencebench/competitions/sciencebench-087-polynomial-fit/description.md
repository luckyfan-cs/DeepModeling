# ScienceBench Task 87

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Statistical Analysis
- Source: SciTools/iris
- Expected Output: polynomial_fit_pred.csv
- Output Type: Tabular

## Task

Generate the requested output based on the provided scientific data.

## Dataset

[START Preview of polynomial_fit/A1B_north_america.nc]
 time: [-946800, -938160, -929520, ...]
 air_temperature: [[[296.07858, 296.17642, 296.25217, …]…]…]
 ...
 [END Preview of polynomial_fit/A1B_north_america.nc]

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Negative root mean squared error (closer to zero is better).
