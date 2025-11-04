# ScienceBench Task 95

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Feature Engineering, Deep Learning
- Source: deepchem/deepchem
- Expected Output: tox21_mol_scscores_pred.npy
- Output Type: Tabular

## Task

Train a synthetic feasibility model using the NumpyDataset in the train_mols.pkl file of the tox21 dataset. Featurize all our molecules with the ECFP fingerprint with chirality. Use radius 2 and 512 feature dimensions. Create a training set of 100000 molecue pairs and fit the model for 20 epochs. Use the length of smiles as the ground truth complexity metric. After that, predict the complexity scores for the molecues in the test_mols.pkl file.

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Classification accuracy (higher is better).
