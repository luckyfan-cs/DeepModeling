# ScienceBench Task 101

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Deep Learning
- Source: ppdebreuck/modnet
- Expected Output: experimental_band_gap_prediction_pred.csv
- Output Type: Tabular

## Task

Train a MODNet model for predicting experimental band gap using the examples in the matbench_expt_gap_train dataset. Use 'elu' as the activation function. Your target attribute is 'gap_expt_eV'. Make sure the results are in the 'gap_expt_eV' column.

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Classification accuracy (higher is better).
