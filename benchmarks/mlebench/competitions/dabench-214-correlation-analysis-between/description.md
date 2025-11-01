# DABench Task 214 - 2. Perform a correlation analysis between the sentiment scores ("neg", "neu", "pos") and the article length ("text" column non-space character count) for articles published by the source "ABC News". Identify any significant correlations between the variables and provide a brief explanation of the findings.

## Task Description

2. Perform a correlation analysis between the sentiment scores ("neg", "neu", "pos") and the article length ("text" column non-space character count) for articles published by the source "ABC News". Identify any significant correlations between the variables and provide a brief explanation of the findings.

## Concepts

Correlation Analysis, Feature Engineering

## Data Description

Dataset file: `fb_articles_20180822_20180829_df.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

{
- Use Pearson correlation for the correlation analysis.
- Assess the strength of the correlation between each pair of variables. Consider correlations to be weak if |r| < 0.3, moderate if 0.3 <= |r| < 0.5, and strong if |r| >= 0.5. 
}

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

{
@neg_length_corr[neg_length_correlation]
@neu_length_corr[neu_length_correlation]
@pos_length_corr[pos_length_correlation]
where "neg_length_correlation", "neu_length_correlation" and "pos_length_correlation" are decimal numbers between -1 and 1 (rounded to 2 decimal places) representing the strength of the correlation between the sentiment scores and the article length.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard
