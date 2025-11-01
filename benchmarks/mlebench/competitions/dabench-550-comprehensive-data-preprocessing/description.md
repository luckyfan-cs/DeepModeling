# DABench Task 550 - Perform comprehensive data preprocessing on the abalone dataset. Handle any missing values and scale the variables (length, diameter, height, whole weight, shucked weight, viscera weight, shell weight) using min-max normalization. Then, perform a distribution analysis to determine if the scaled variables adhere to a normal distribution.

## Task Description

Perform comprehensive data preprocessing on the abalone dataset. Handle any missing values and scale the variables (length, diameter, height, whole weight, shucked weight, viscera weight, shell weight) using min-max normalization. Then, perform a distribution analysis to determine if the scaled variables adhere to a normal distribution.

## Concepts

Comprehensive Data Preprocessing, Distribution Analysis

## Data Description

Dataset file: `abalone.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Any missing values should be filled using the median of the respective column. Use sklearn's MinMaxScaler for normalization, scale the variables to a range between 0 and 1. For distribution analysis, use skewness and kurtosis to determine the distribution type. If skewness is between -0.5 and 0.5 and kurtosis is between -2 and 2, we consider it as normal.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@missing_values_handled["Yes"/"No"], @min_max_scaler_scale[range], @distribution_type[distribution type]
where "missing_values_handled" indicates if missing values have been properly handled or not, "range" should be a string that specifies the range of the scaled variables, for example "0-1", "distribution type" should be a string which can be "Normal" or "Non-Normal".

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard
