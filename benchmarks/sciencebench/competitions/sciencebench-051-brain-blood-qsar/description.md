# ScienceBench Task 51

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Feature Engineering, Deep Learning
- Source: deepchem/deepchem
- Output Type: Tabular

## Task

Train a blood–brain barrier permeability model using the provided logBB dataset. Build and evaluate a graph convolutional or similar molecular model, generate predictions for the held-out test set, and save the classification results to the required CSV with columns `smiles` (or identifier) and `label` (`0` or `1`).

## Dataset

The `brain-blood/` directory provides two SDF files:

- `logBB.sdf` – training compounds with logBB labels and activity classes.
- `logBB_test.sdf` – test compounds whose permeability class must be predicted.

## Submission Format

Write `pred_results/brain_blood_qsar.csv` and include a `label` column with your predicted activity class for each test molecule.

## Evaluation

Submissions are accepted when the balanced accuracy on the test set meets or exceeds 0.70, matching the original evaluation script.
