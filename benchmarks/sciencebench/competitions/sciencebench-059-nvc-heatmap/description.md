# ScienceBench Task 59

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: nriesterer/syllogistic-nvc
- Expected Output: nvc_heatmap.png
- Output Type: Image

## Task

Create a heatmap visualization for the NVC (No Valid Conclusion) predictions from various models and the Most Frequent Answer (MFA) for syllogistic reasoning tasks.

## Dataset

[START Preview of nvc/Ragni2016.csv]
id,sequence,task,choices,response,response_type,domain,gender,age
1,0,Some;models;managers/All;models;clerks,All;managers;clerks|All;clerks;managers|Some;managers;clerks|Some;clerks;managers|Some not;managers;clerks|Some not;clerks;managers|No;managers;clerks|No;clerks;managers|NVC,Some;managers;clerks,single-choice,syllogistic,female,56
1,1,No;divers;carpenters/All;linguists;carpenters,All;divers;linguists|All;linguists;divers|Some;divers;linguists|Some;linguists;divers|Some not;divers;linguists|Some not;linguists;divers|No;divers;linguists|No;linguists;divers|NVC,No;divers;linguists,single-choice,syllogistic,female,56
1,2,All;therapists;climbers/Some;skaters;therapists,All;climbers;skaters|All;skaters;climbers|Some;climbers;skaters|Some;skaters;climbers|Some not;climbers;skaters|Some not;skaters;climbers|No;climbers;skaters|No;skaters;climbers|NVC,Some;skaters;climbers,single-choice,syllogistic,female,56
...
[END Preview of nvc/Ragni2016.csv]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
