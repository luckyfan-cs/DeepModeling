# ScienceBench Task 25

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: mad-lab-fau/BioPsyKit
- Expected Output: ecg_processing_vis2_pred_result.png
- Output Type: Image

## Task

Process the given ECG data and show heart rate variability (HRV) plot. After loading the ECG data, perform R peak detection and outlier correction. Then, you need to divide the data into two phases: the first phase is from 12:32 to 12:35, the second phase is from 12:35 to 12:38.

## Dataset

[START Preview of ecg_processing_data/ecg_data.pkl]
time,ecg
2019-10-23 12:31:53+02:00,88.0
2019-10-23 12:31:53.003906+02:00,28.0
2019-10-23 12:31:53.007812+02:00,-50.0
...
[END Preview of ecg_processing_data/ecg_data.csv]

[START Preview of ecg_processing_data/sampling_rate.txt]
256.0
[END Preview of ecg_processing_data/sampling_rate.txt]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
