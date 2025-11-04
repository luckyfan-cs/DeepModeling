# ScienceBench Task 58

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis
- Source: nriesterer/syllogistic-nvc
- Expected Output: individuals.csv
- Output Type: Tabular

## Task

Generate a CSV file 'individuals.csv' containing the number of persons whose best-fit model-rule combination aligns with the models and rules from a set of given predictions. Each row in the CSV should represent a model-rule combination with the format: "Model; Rule; Num persons".

## Dataset

[START Preview of nvc/Ragni2016.csv]
id,sequence,task,choices,response,response_type,domain,gender,age
1,0,Some;models;managers/All;models;clerks,All;managers;clerks|All;clerks;managers|Some;managers;clerks|Some;clerks;managers|Some not;managers;clerks|Some not;clerks;managers|No;managers;clerks|No;clerks;managers|NVC,Some;managers;clerks,single-choice,syllogistic,female,56
1,1,No;divers;carpenters/All;linguists;carpenters,All;divers;linguists|All;linguists;divers|Some;divers;linguists|Some;linguists;divers|Some not;divers;linguists|Some not;linguists;divers|No;divers;linguists|No;linguists;divers|NVC,No;divers;linguists,single-choice,syllogistic,female,56
1,2,All;therapists;climbers/Some;skaters;therapists,All;climbers;skaters|All;skaters;climbers|Some;climbers;skaters|Some;skaters;climbers|Some not;climbers;skaters|Some not;skaters;climbers|No;climbers;skaters|No;skaters;climbers|NVC,Some;skaters;climbers,single-choice,syllogistic,female,56
...
[END Preview of nvc/Ragni2016.csv]

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Negative root mean squared error (closer to zero is better).
