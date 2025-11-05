# Overview

## Description

Santander Bank wants to identify dissatisfied customers early in their relationship. You are given hundreds of anonymized customer attributes and must predict whether each customer is unsatisfied so the bank can take proactive action before the customer leaves.

## Evaluation

Submissions are evaluated using the area under the ROC curve (AUC) between the predicted probability and the observed `TARGET`.

## Submission File

For each `ID` in the test set, submit the predicted probability that the customer is dissatisfied. The file must include a header and match the format below:

```
ID,TARGET
2,0.0
5,0.0
6,0.0
```

# Data

## Dataset Description

The dataset consists of anonymized numerical features describing Santander customers. The `TARGET` column equals `1` for unsatisfied customers and `0` otherwise. Your task is to estimate the probability that each customer in the test set is dissatisfied.

## Files

- `train.csv` — training set with features and the `TARGET` label.
- `test.csv` — test set features without the `TARGET` column.
- `sample_submission.csv` — example submission in the required format.
