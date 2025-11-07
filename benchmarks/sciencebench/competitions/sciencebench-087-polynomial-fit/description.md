# ScienceBench Task 87

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Statistical Analysis
- Source: SciTools/iris
- Expected Output: `polynomial_fit_pred.csv`
- Output Type: CSV (tabular)

## Task

Fit a polynomial model to the A1B North America air-temperature series provided in the dataset. Use the monthly temperatures to estimate a smoothed annual temperature curve and export the predicted yearly values to the required CSV file.

## Dataset

[START Dataset Preview: polynomial_fit]
|-- A1B_north_america.nc
[END Dataset Preview]

## Submission Format

Write `pred_results/polynomial_fit_pred.csv` with the columns `Year` and `Fitted_Temperature`, sorted by year and stored as floating-point values.

## Evaluation

The grader sorts both CSV files and requires an exact match with the gold reference after ordering.
