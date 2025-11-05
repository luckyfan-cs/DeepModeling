# ScienceBench Task 19

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Engineering, Machine Learning
- Source: anikaliu/CAMDA-DILI
- Output Type: Tabular

## Task

Train support vector machine (SVM) classifiers to detect Drug-Induced Liver Injury (DILI) risk using the CAMDA dataset splits. Map vDILIConcern labels to a binary target, build models for the `MCNC`, `MCLCNC`, and `all` configurations, and write predictions to `pred_results/{split}_SVM.csv` with the columns `standardised_smiles` and `label` (`DILI` or `NoDILI`).

## Dataset

The `dili/` directory provides the same training and test files as Task 18: `train.csv` (labeled data) and `test.csv` (evaluation data).

## Submission Format

Produce three CSV files in `pred_results/`: `MCNC_SVM.csv`, `MCLCNC_SVM.csv`, and `all_SVM.csv`, each aligned to the order of `test.csv` and containing the required columns.

## Evaluation

Submissions are accepted when SMILES ordering matches the reference and the mean F1 score across the three splits reaches the 0.73 threshold defined by the official evaluation script.
