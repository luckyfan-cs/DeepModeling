# ScienceBench Task 42

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: neuropsychology/NeuroKit
- Expected Output: EDR_analyze_pred.png
- Output Type: Image

## Task

Derive respiratory signals from ECG data using multiple EDR methods and create a comparative visualization. Clean the ECG, detect R peaks, compute the heart period, generate EDR with four methods, and plot them together before saving the figure to `pred_results/EDR_analyze_pred.png`.

## Dataset

[START Dataset Preview: biosignals]
|-- bio_eventrelated_100hz.csv
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with `EDR_analyze_pred.png`.

## Evaluation

The grader decodes the submitted image, compares it against the reference visualization, and accepts the submission when the similarity score meets or exceeds 60.
