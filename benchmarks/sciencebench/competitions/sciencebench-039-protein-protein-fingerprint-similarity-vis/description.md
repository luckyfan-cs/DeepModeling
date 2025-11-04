# ScienceBench Task 39

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Computational Analysis, Data Visualization
- Source: chemosim-lab/ProLIF
- Expected Output: protein_protein_similarity_pred.png
- Output Type: Image

## Task

Plot the Tanimoto similarities of the fingerprint between the frames. Specifically, the interaction fingerprints between a selected small protein and large protein for the first 10 trajectory frames.

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
