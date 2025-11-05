# ScienceBench Task 40

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Engineering, Machine Learning
- Source: anikaliu/CAMDA-DILI
- Output Type: Tabular

## Task

Use molecular descriptors to train Random Forest classifiers that predict DILI risk. Build separate models for the `MCNC`, `MCLCNC`, and `all` splits, and store the predictions in `pred_results/MD_{split}_RF.csv` with columns `standardised_smiles` and `label` (`DILI` or `NoDILI`).

## Dataset

The `dili_MD/` directory contains:

- `mol_descriptors_training.csv` – descriptor features with labels and split annotations.
- `standardized_compounds_excl_ambiguous_cluster.csv` – metadata for compounds.
- `test.csv` – descriptor features for the evaluation set.

## Submission Format

Produce `MD_all_RF.csv`, `MD_MCNC_RF.csv`, and `MD_MCLCNC_RF.csv` inside `pred_results/`. Each file must align with `test.csv` and include the `label` predictions.

## Evaluation

Submissions are accepted when the mean F1 score across the three splits reaches the reference threshold of 0.73.
