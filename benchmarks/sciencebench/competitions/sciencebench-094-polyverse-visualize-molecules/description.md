# ScienceBench Task 94

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Molecule Visualization
- Source: deepchem/deepchem
- Expected Output: polyverse_visualize_molecules_pred.png
- Output Type: Image

## Task

Visuzalize the molecule in the file 'molecule_ZINC001754572633.pkl' with a graph, which is a rdkit.Chem.rdchem.Mol object, using the rdkit and networkx library. You should use orange for Carbon (C) atoms, magenta for Oxygen (O) atoms, and cyan for Nitrogen (N) atoms. Use the spring layout with random seed set to 10 when drawing the molecue. Set the node size to 800 and add labels to the nodes.

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
