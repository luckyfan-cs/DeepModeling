# DABench Task 734 - Is there a correlation between life expectancy and GDP per capita for each continent? Perform correlation analysis for each continent separately and provide the correlation coefficients.

## Task Description

Is there a correlation between life expectancy and GDP per capita for each continent? Perform correlation analysis for each continent separately and provide the correlation coefficients.

## Concepts

Correlation Analysis, Comprehensive Data Preprocessing

## Data Description

Dataset file: `gapminder_cleaned.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Calculate the Pearson correlation coefficient (r) to assess the strength and direction of the linear relationship between life expectancy and GDP per capita for each continent. Assess the correlation significance using a two-tailed test with a significance level (alpha) of 0.05. Report the p-values associated with the correlation test. Consider the correlation significant if the p-value is less than 0.05 and the absolute value of r is greater than or equal to 0.5. Consider the correlation non-significant if the p-value is greater than or equal to 0.05.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

For each continent:
@continent_name[name]
@correlation_coefficient[r_value]
@p_value[p_value]
@correlation_significance[significance]
where "name" is the name of the continent.
where "r_value" is a number between -1 and 1, rounded to two decimal places.
where "p_value" is a number between 0 and 1, rounded to four decimal places.
where "significance" is a string that can either be "significant" or "non-significant" based on the conditions specified in the constraints.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard
