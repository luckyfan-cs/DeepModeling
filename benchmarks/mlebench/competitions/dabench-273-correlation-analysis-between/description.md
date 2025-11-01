# DABench Task 273 - Perform a correlation analysis between the MEANGAM and MEANGBT columns. Additionally, for the correlated variables, identify any outliers in the MEANGAM column using the Z-score method and a threshold of 3 for the absolute Z-score.

## Task Description

Perform a correlation analysis between the MEANGAM and MEANGBT columns. Additionally, for the correlated variables, identify any outliers in the MEANGAM column using the Z-score method and a threshold of 3 for the absolute Z-score.

## Concepts

Correlation Analysis, Outlier Detection

## Data Description

Dataset file: `3901.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

1. Use the Pearson correlation coefficient to assess the correlation between MEANGAM and MEANGBT columns.
2. Define outliers as those data points in the MEANGAM column where the absolute Z-score exceeds 3.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

1. @correlation_coefficient[correlation_value] where "correlation_value" should be a number between -1 and 1, rounded to 3 decimal places.
2. @outlier_count[outlier_total] where "outlier_total" denotes the total number of identified outliers in the MEANGAM column.
3. @outlier_list[outlier_values_list] where "outlier_values_list" is a list of the identified outlier values in MEANGAM column, rounded to 2 decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard
