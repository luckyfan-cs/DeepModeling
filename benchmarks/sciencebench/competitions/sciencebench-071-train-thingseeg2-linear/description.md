# ScienceBench Task 71

## Overview

- Domain: Psychology and Cognitive Science
- Subtask Categories: Feature Engineering, Machine Learning
- Source: ZitongLu1996/EEG2EEG
- Output Type: NumPy array

## Task

Learn a linear mapping from Subject 01 to Subject 03 EEG representations using the provided ThingseEG2 training splits. Fit the model on the paired training recordings, apply it to the Subject 01 test data, and save the generated Subject 03 signals as the required NumPy file.

## Dataset

The `thingseeg2/` directory contains:

- `train/sub01.npy`, `train/sub03.npy` – aligned training signals.
- `test/sub01.npy` – Subject 01 test signals to transform.

## Submission Format

Write `pred_results/linear_sub01tosub03_pred.npy` containing a NumPy array shaped like the provided test data (200 × 3400 after reshaping).

## Evaluation

Submissions are accepted when the Spearman correlation between the generated signals and the normalized gold signals reaches at least 0.6 (matching the reference evaluation script).
