# ScienceBench Task 2

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Feature Selection, Machine Learning
- Source: uw-cmg/MAST-ML
- Expected Output: mat_diffusion_features.csv
- Output Type: Tabular

## Task

Generate features for the given diffusion data based on material composition and use the SHAP feature selection approach to select 20 features. Save the selected features as a CSV file "mat_diffusion_features.csv" to the folder "output file".

## Dataset

[START Preview of mat_diffusion/diffusion_data_nofeatures_new.xlsx]
  Material compositions 1  Material compositions 2  Material compositions joined  E_regression
0                      Ag                      Ag                           AgAg      0.000000
1                      Ag                      Co                           AgCo     -0.090142
2                      Ag                      Cr                           AgCr      0.259139
...
[END Preview of mat_diffusion/diffusion_data_nofeatures_new.xlsx]

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Element-wise equality between your submission and the reference.
