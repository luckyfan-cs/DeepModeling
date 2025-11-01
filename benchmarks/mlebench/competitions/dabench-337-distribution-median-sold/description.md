# DABench Task 337 - 2. Is the distribution of the median sold price per square foot skewed? If yes, is it positively or negatively skewed?

## Task Description

2. Is the distribution of the median sold price per square foot skewed? If yes, is it positively or negatively skewed?

## Concepts

Distribution Analysis

## Data Description

Dataset file: `Zip_MedianSoldPricePerSqft_AllHomes.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

For determining the skewness, consider only non-null values. Use the Fisher-Pearson standardized moment coefficient for assessing the skewness. A skewness value > 0 means that there is more weight in the right tail of the distribution (positive skewness). A skewness value < 0 means that there is more weight in the left tail of the distribution (negative skewness). Calculate the skewness up to two decimal places.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@skewness_coefficient[skewness_coefficient]
@skewness_type[skewness_type]
where "skewness_coefficient" is a number greater than or equal to -1 and less than or equal to 1, rounded to two decimal places.
where "skewness_type" is a string that could be either "Positive Skewness", "Negative Skewness", or "No Skewness".

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium
