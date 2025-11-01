# DABench Task 759 - 5. Calculate the median and range of the maximum temperature (TMAX_F) for each type of observation (obs_type) recorded in the dataset. Are there any differences in the median and range between different observation types?

## Task Description

5. Calculate the median and range of the maximum temperature (TMAX_F) for each type of observation (obs_type) recorded in the dataset. Are there any differences in the median and range between different observation types?

## Concepts

Summary Statistics, Distribution Analysis

## Data Description

Dataset file: `weather_data_1864.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

In your analysis:
- Consider only two observation types: "TMAX" and "TMIN".
- Report the median rounded to two decimal places.
- Calculate the range as the difference between the maximum and minimum temperatures for each observation type.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@@median_tmax["median_TMAX"]
@median_tmin["median_TMIN"]
@range_tmax["range_TMAX"]
@range_tmin["range_TMIN"]

where "median_TMAX" and "median_TMIN" are the median temperatures for TMAX and TMIN observation types, respectively. They are numbers between -100 and 100, rounded to two decimal places.
where "range_TMAX" and "range_TMIN" are the range of temperatures for TMAX and TMIN observation types, respectively. They are numbers greater than 0.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard
