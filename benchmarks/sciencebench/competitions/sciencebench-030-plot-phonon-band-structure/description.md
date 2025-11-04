# ScienceBench Task 30

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Computational Analysis, Data Visualization
- Source: materialsproject/pymatgen
- Expected Output: phonon_bandstructure.png
- Output Type: Image

## Task

Calculate and plot the phonon band structure using the output from VASP DFPT calculations saved in "vasprun.dfpt.phonon.xml.gz".

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
