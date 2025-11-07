# ScienceBench Task 43

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: neuropsychology/NeuroKit
- Expected Output: EOG_analyze_pred.png
- Output Type: Image

## Task

Process the EOG signal to detect and visualise eye blinks. Clean the signal, detect peaks, build epochs around each blink, and plot the aligned traces together with the median blink pattern. Save the final figure to `pred_results/EOG_analyze_pred.png`.

## Dataset

[START Dataset Preview: biosignals]
|-- eog_100hz.csv
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with `EOG_analyze_pred.png`.

## Evaluation

The grader decodes the submitted image, compares it against the reference visualization, and accepts the submission when the similarity score meets or exceeds 60.
