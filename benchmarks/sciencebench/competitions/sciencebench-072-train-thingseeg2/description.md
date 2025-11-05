# ScienceBench Task 72

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Feature Engineering, Deep Learning
- Source: ZitongLu1996/EEG2EEG
- Output Type: Array

## Task

Train the EEG2EEG model that maps neural representations from Subject 01 to Subject 03 using the provided preprocessed recordings. After fitting the model with the training data, run inference on the Subject 01 test set and generate the corresponding Subject 03 responses.

## Dataset

The `thingseeg2/` directory contains the NumPy arrays needed for training and evaluation:

- `train/sub01.npy` and `train/sub03.npy` provide aligned training trials for both subjects.
- `test/sub01.npy` contains held-out trials from Subject 01 to be translated by the model.

All arrays are stored with channels × time information, matching the data shapes referenced in the original EEG2EEG notebook.

## Submission Format

Produce the required submission CSV with two columns: `file_name` and `array_base64`. Encode the generated NumPy array (`eeg2eeg_sub01tosub03_pred.npy`) with `numpy.save` into an in-memory buffer, then base64 encode the resulting bytes before writing them into the CSV row.

## Evaluation

The grader decodes your array, applies the same normalization as the reference implementation, and reshapes it to `(200, 3400)`. A submission is accepted when the Spearman correlation with the gold array reaches at least 0.73.
