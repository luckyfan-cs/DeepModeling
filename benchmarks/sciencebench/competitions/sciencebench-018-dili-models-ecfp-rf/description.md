# ScienceBench Task 18

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Engineering, Machine Learning
- Source: anikaliu/CAMDA-DILI
- Output Type: Tabular

## Task

Train Random Forest models to detect Drug-Induced Liver Injury (DILI) risk using the CAMDA splits. Map the vDILIConcern labels to a binary target (DILI vs NoDILI), train separate models for the `MCNC`, `MCLCNC`, and `all` configurations, run cross-validation/hyperparameter search, and export the best-model predictions on the provided test set. Save each run to `pred_results/{split}_RF.csv` where `split` is `MCNC`, `MCLCNC`, or `all`, with columns `standardised_smiles` and `label` (`DILI` or `NoDILI`).

## Dataset

The `dili/` directory provides:

- `train.csv` – labeled training compounds with cluster information.
- `test.csv` – held-out compounds to score.

## Submission Format

Produce three CSV files in `pred_results/`: `MCNC_RF.csv`, `MCLCNC_RF.csv`, and `all_RF.csv`. Each must contain the columns `standardised_smiles` and `label`, aligned to the order of `test.csv`.

## Evaluation

Submissions are accepted when the SMILES ordering matches the gold reference and the mean F1 score across the three splits reaches the 0.73 threshold used by the original evaluation script.
