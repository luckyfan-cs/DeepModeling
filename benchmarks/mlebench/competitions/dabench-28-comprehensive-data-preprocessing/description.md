# DABench Task 28 - Perform comprehensive data preprocessing on the dataset, including cleaning, transformation, and handling of missing values.

## Task Description

Perform comprehensive data preprocessing on the dataset, including cleaning, transformation, and handling of missing values.

## Concepts

Comprehensive Data Preprocessing

## Data Description

Dataset file: `insurance.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Handle the missing values in the 'age', 'sex', and 'region' columns by removing the corresponding rows. Transform the 'sex' and 'smoker' columns to binary format (0 and 1). Normalize 'age', 'bmi', 'children', and 'charges' columns. Report the mean of each column after the preprocessing.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@mean_age[mean_age]
@mean_sex[mean_sex]
@mean_bmi[mean_bmi]
@mean_children[mean_children]
@mean_smoker[mean_smoker]
@mean_region[mean_region]
@mean_charges[mean_charges]
where "mean_xxx" are all floating-point numbers rounded to four decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard
