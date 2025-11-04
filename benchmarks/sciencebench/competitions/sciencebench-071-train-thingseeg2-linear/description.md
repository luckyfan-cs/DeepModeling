# ScienceBench Task 71

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Feature Engineering, Machine Learning
- Source: ZitongLu1996/EEG2EEG
- Expected Output: linear_sub01tosub03_pred.npy
- Output Type: Tabular

## Task

Train a linear model to learn the mapping of neural representations in EEG signals from one subject (Sub 01) to another (Sub 03) based on the preprocessed EEG data from Sub 01 and Sub 03. Then use the test set of Subject 1 (Sub 01) to generate EEG signal of Subject 3 (Sub 03).

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Element-wise equality between your submission and the reference.
