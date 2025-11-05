# ScienceBench Task 8

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Selection, Data Visualization
- Source: psa-lab/predicting-activity-by-machine-learning
- Output Type: Image

## Task

Perform backward feature selection using logistic regression to identify the most relevant chemical features for predicting signal inhibition from the DKPES dataset. Binarize the signal inhibition values using an appropriate threshold, track model accuracy as features are removed, and plot accuracy versus number of retained features. 

## Dataset

The `dkpes` folder provides training and test CSV files: `dkpes_train.csv` (with signal inhibition labels and features) and `dkpes_test.csv` (features only).

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode the PNG you saved at `pred_results/dkpes_feature_selection_analysis_pred.png` as base64 (UTF-8 string) and assign it to the matching file name.

## Evaluation

The grader decodes your base64 image, writes it to disk, and compares it to the gold figure using the original GPT-4 based visual judge (falling back to pixel similarity when unavailable). A score of at least 60/100 is required to pass.
