# ScienceBench Task 31

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Computational Analysis, Data Visualization
- Source: materialsproject/pymatgen
- Expected Output: phonon_dos.png
- Output Type: Image

## Task

Use `vasprun.dfpt.phonon.xml.gz` to reconstruct the phonon density of states. Make sure the DOS axes are labeled, include legends for projected curves if present, and export the visualization to the output image path defined by the submission template.

## Dataset

[START Dataset Preview: materials_genomics]
|-- F_CHGCAR
|-- LiMoS2_F_CHGCAR
|-- LiMoS2_CHGCAR
|-- vasprun.dfpt.phonon.xml.gz
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes the submitted image, compares it against the reference visualization, and assigns a similarity score. Scores below 60 fail the evaluation.
