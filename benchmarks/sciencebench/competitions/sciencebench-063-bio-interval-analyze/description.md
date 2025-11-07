# ScienceBench Task 63

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Signal Processing, Data Visualization
- Source: neuropsychology/NeuroKit
- Output Type: Image

## Task

Extract heart-rate and respiration-rate intervals from the biosignals recordings, then visualise both modalities. Produce `pred_results/bio_ecg_plot.png` to summarise the ECG analysis and `pred_results/bio_rsp_plot.png` to summarise the respiration analysis.

## Dataset

[START Dataset Preview: biosignals]
|-- bio_eventrelated_100hz.csv
|-- bio_resting_5min_100hz.csv
|-- ecg_1000hz.csv
|-- eog_100hz.csv
[END Dataset Preview]

## Submission Format

Create `sample_submission.csv` containing two rows with columns `file_name` and `image_base64`. Provide entries for `bio_ecg_plot.png` and `bio_rsp_plot.png`, leaving the encoded strings blank.

## Evaluation

The grader decodes both submitted images, compares them to the reference plots, and grants full credit when each similarity score meets or exceeds 60.
