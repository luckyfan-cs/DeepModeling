# ScienceBench Task 52

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Feature Engineering, Deep Learning, Molecule Visualization
- Source: deepchem/deepchem
- Output Type: Image

## Task

Visualise the aquatic toxicity QSAR dataset by highlighting atomic contributions for the provided test compound. Export the figure to `pred_results/aquatic_toxicity_qsar_vis.png`.

## Dataset

[START Dataset Preview: aquatic_toxicity]
|-- Tetrahymena_pyriformis_OCHEM.sdf
|-- Tetrahymena_pyriformis_OCHEM_test_ex.sdf
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with `aquatic_toxicity_qsar_vis.png`.

## Evaluation

The grader decodes the submitted image, compares it against the reference visualization, and accepts the submission when the similarity score meets or exceeds 60.
