# ScienceBench Task 30

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Computational Analysis, Data Visualization
- Source: materialsproject/pymatgen
- Expected Output: phonon_bandstructure.png
- Output Type: Image

## Task

Read the DFPT results in `vasprun.dfpt.phonon.xml.gz`, reconstruct the phonon dispersion, and render the band structure plot with an appropriate high-symmetry path. Keep the axes labeled and include a legend if multiple branches require clarification. Store the visualization in the output image file expected by the submission template.

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
