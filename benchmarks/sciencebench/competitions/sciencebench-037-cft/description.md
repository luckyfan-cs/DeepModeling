# ScienceBench Task 37

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis
- Source: mad-lab-fau/BioPsyKit
- Expected Output: cft_pred_results.json
- Output Type: Tabular

## Task

Load the heart rate data in sheet `MIST3`, compute baseline heart rate, onset heart rate, and onset heart rate percentage, then save them to `pred_results/cft_pred_results.json` using the keys `baseline_hr`, `onset_hr`, and `onset_hr_percent`.

## Dataset

[START Dataset Preview: mist_hr]
|-- hr_sample_mist.xlsx
[END Dataset Preview]

## Submission Format

Submit `sample_submission.json` matching the reference structure with the three required keys.

## Evaluation

The grader validates that all three parameters exactly match the reference values (within floating-point tolerance). Submissions with any mismatch fail.
