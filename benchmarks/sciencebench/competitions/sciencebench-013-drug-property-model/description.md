# ScienceBench Task 13

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Engineering, Deep Learning
- Source: kexinhuang12345/DeepPurpose
- Expected Output: hiv_test_pred.csv
- Output Type: Tabular

## Task

Train a property prediction model using the HIV dataset to predict the activity of drugs against HIV. Save the SMILES strings and their corresponding predictions to "output file" using the same column names as in the given dataset.

## Dataset

[START Preview of hiv/HIV_train.csv]
smiles,activity,HIV_active
O=C(O)CC(NC(=O)OCc1ccccc1)C(=O)O,CI,0
O=[N+]([O-])c1ccc(Nc2ccccc2)c2nonc12,CI,0
CCOC(=O)C(=NNc1ccc(C)cc1)N1C(=S)N(C)N=C(C)C=C1S,CI,0
...
[END Preview of hiv/HIV_train.csv]

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Classification accuracy (higher is better).
