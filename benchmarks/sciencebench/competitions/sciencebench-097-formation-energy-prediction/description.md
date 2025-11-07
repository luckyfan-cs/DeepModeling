# ScienceBench Task 97

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Deep Learning
- Source: deepchem/deepchem
- Expected Output: `formation_energy_prediction_pred.txt`
- Output Type: Text (numeric)

## Task

Train a formation-energy predictor using the provided perovskite training molecules and output the predicted energies for the test set in the original order.

## Dataset

[START Dataset Preview: perovskite]
|-- perovskite_train.pkl
|-- perovskite_test.pkl
[END Dataset Preview]

## Submission Format

Write the predictions to `pred_results/formation_energy_prediction_pred.txt`, one floating-point value per line.

## Evaluation

The grader computes the mean squared error against the gold targets (pass if MSE ≤ 0.1).
