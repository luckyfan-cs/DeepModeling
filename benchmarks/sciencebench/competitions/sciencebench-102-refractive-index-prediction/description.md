# ScienceBench Task 102

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Deep Learning
- Source: ppdebreuck/modnet
- Expected Output: ref_index_predictions_pred.csv
- Output Type: Tabular

## Task

Train a MODNet model for predicting the refractive index for materials using examples in the md_ref_index_train file. Use 'elu' as the activation function. Put the results in the 'refractive_index' column.

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Classification accuracy (higher is better).
