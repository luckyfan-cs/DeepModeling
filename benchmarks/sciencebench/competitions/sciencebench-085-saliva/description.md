# ScienceBench Task 85

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Engineering
- Source: mad-lab-fau/BioPsyKit
- Expected Output: saliva_pred.json
- Output Type: Tabular

## Task

Analyze the given saliva data and compute features that represent sample statistics or distribution (e.g., mean, location of max/min value, skewness) for each subject. Save the computed features along with subject condition as a dictionary of dictionaries into a json file "output file".

## Dataset

[START Preview of saliva_data/data.pkl, which is a pandas DataFrame, and (condition, subject, sample) is the index]
condition,subject,sample,cortisol
Intervention,Vp01,0,6.988899999999999
Intervention,Vp01,1,7.0332
Intervention,Vp01,2,5.7767
Intervention,Vp01,3,5.2579
Intervention,Vp01,4,5.00795
[END Preview of saliva_data/data.pkl]

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Element-wise equality between your submission and the reference.
