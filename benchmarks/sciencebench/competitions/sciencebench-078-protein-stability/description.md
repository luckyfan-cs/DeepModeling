# ScienceBench Task 78

## Overview

- Domain: Bioinformatics
- Subtask Categories: Feature Engineering, Deep Learning
- Source: deepchem/deepchem
- Expected Output: pucci-proteins_test_pred.csv
- Output Type: Tabular

## Task

Train a neural network model using the pucci dataset to predict the melting temperature (deltaTm) of proteins caused due to the point mutation of one amino acid at chain A. The dataset also contains the PDB files which need to be processed to retrieve the original (wild-type) amino acid sequence and then to create the mutated sequences. Save the predictions for the test set as a single column dataframe "deltaTm" to the file "output file".

## Dataset

[START Preview of pucci/pucci-proteins_train.csv]
Unnamed: 0,N,PDBid,Chain,RESN,RESwt,RESmut,ΔTmexp,Tmexp [wt],ΔΔHmexp,ΔHmexp [wt],ΔΔCPexp ,ΔCPexp [wt],ΔΔGexp(T),T,Nres,R (Å),Protein,Organism,Ref.,pH,Exp.Tech., 
,219,1ey0,A,29,GLY,PHE,-5.9,53.1,5,-337,-,-9.1,4.6,25,149,1.6,S. Nuclease,STAA,"[31,35]",[7.0],FL-CD,
,1605,5pti,A,36,GLY,ALA,-11.7,78.0,61,-353,-,-1.7,-,-,58,1.0,PTI,Bovine,[229],[3.0],CD,
,287,1ey0,A,82,THR,VAL,1.1,53.1,-14,-337,-,-9.1,-,-,149,1.6,S. Nuclease,STAA,[31],[7.0],FL-CD,
...
[START Preview of pucci/pucci-proteins_train.csv]

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Classification accuracy (higher is better).
