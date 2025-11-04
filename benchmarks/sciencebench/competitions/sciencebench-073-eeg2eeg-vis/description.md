# ScienceBench Task 73

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Data Visualization
- Source: ZitongLu1996/EEG2EEG
- Expected Output: eeg2eeg_vis_pred.png
- Output Type: Image

## Task

Visualize the original and generated EEG signal of Sub-03 using a line plot. Images and channels corresponding to each timepoint should be averaged before plotting. Save the line plot to "output file".

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
