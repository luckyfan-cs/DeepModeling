# DABench Task 275 - Perform a comprehensive analysis of the dataset by:
1. Removing any duplicate entries.
2. Filling in missing values in the USFLUX column with the mean value of the column.
3. Creating a new feature named "MEANGAM_MEANGBZ_DIFF" by subtracting the MEANGBZ column from the MEANGAM column.
4. Applying machine learning techniques to predict the values in the TOTUSJH column using the MEANJZH, TOTUSJZ, and MEANGBT columns. You will need to use a Random Forest Regressor with 100 trees for this task.

## Task Description

Perform a comprehensive analysis of the dataset by:
1. Removing any duplicate entries.
2. Filling in missing values in the USFLUX column with the mean value of the column.
3. Creating a new feature named "MEANGAM_MEANGBZ_DIFF" by subtracting the MEANGBZ column from the MEANGAM column.
4. Applying machine learning techniques to predict the values in the TOTUSJH column using the MEANJZH, TOTUSJZ, and MEANGBT columns. You will need to use a Random Forest Regressor with 100 trees for this task.

## Concepts

Comprehensive Data Preprocessing, Feature Engineering, Machine Learning

## Data Description

Dataset file: `3901.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

1. Remove duplicates based on the entire row.
2. Missing values in the USFLUX column should be replaced with the mean of the same column.
3. Use the Random Forest Regressor as the machine learning model.
4. The Random Forest Regressor should have 100 trees.
5. The independent variables for the prediction should be the MEANJZH, TOTUSJZ, and MEANGBT columns.
6. The dependent or target variable for the prediction should be the TOTUSJH column.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

1. @duplicate_count[duplicate_total] where "duplicate_total" should be an integer indicating the number of duplicate rows removed.
2. @usflux_mean[mean_value] where "mean_value" should be a number rounded to 2 decimal places.
3. @new_feature_mean[new_feature_mean] where "new_feature_mean" is the mean of the new feature "MEANGAM_MEANGBZ_DIFF", rounded to 2 decimal places.
4. @model_accuracy[model_accuracy] where "model_accuracy" is the accuracy of the Random Forest Regressor model, should be a percentage rate between 0 and 100, rounded to 3 decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard
