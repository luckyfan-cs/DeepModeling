# DABench Task 111 - Perform comprehensive data preprocessing by handling missing values in the Self_Employed and LoanAmount columns. Use different strategies to handle the missing values in each column and compare the impact on the dataset's summary statistics (mean, median, etc.).

## Task Description

Perform comprehensive data preprocessing by handling missing values in the Self_Employed and LoanAmount columns. Use different strategies to handle the missing values in each column and compare the impact on the dataset's summary statistics (mean, median, etc.).

## Concepts

Comprehensive Data Preprocessing, Summary Statistics

## Data Description

Dataset file: `test_Y3wMUE5_7gLdaTN.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Replace missing values in Self_Employed with 'No' and in LoanAmount with the median value of the column. Calculate the mean, median, and standard deviation of LoanAmount after preprocessing.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@mean_loan[mean], @median_loan[median], @std_dev_loan[std_dev] where "mean", "median", and "std_dev" are numbers (float), rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard
