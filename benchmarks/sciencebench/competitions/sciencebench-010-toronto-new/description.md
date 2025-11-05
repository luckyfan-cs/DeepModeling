# ScienceBench Task 10

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Geospatial Analysis, Map Visualization
- Source: geopandas/geopandas
- Output Type: Image

## Task

Analyze Toronto fire stations and their service coverage, identifying potential coverage gaps. Visualize the results.

## Dataset

{"type":"FeatureCollection","features":[{"type":"Feature","id":1,"geometry":{"type":"Point","coordinates":[-79.163608108967836,43.794228005499171]},"properties":{"OBJECTID_1":1,"NAME":"FIRE STATION 214","ADDRESS":"745 MEADOWVALE RD","WARD_NAME":"Scarborough East (44)","MUN_NAME":"Scarborough"}},{"type":"Feature","id":2,"geometry":{"type":"Point","coordinates":[-79.148072382066644,43.777409170303173]},"properties":{"OBJECTID_1":2,"NAME":"FIRE STATION 215","ADDRESS":"5318 LAWRENCE AVE E","WARD_NAME":"Scarborough East (44)","MUN_NAME":"Scarborough"}},{"type":"Feature","id":3,"geometry":{"type":"Point","coordinates":[-79.255069254032705,43.734807353775956]},"properties":{"OBJECTID_1":3,"NAME":"FIRE STATION 221","ADDRESS":"2575 EGLINTON AVE E","WARD_NAME":"Scarborough Southwest (35)","MUN_NAME":"Scarborough"}},...]}


## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode the PNG stored at `pred_results/Fire_Service_Analysis.png` as base64 (UTF-8 string) and place it in the row for that filename.

## Evaluation

The grader decodes your base64 image, writes it to disk, and compares it to the gold visualization using the original GPT-4 visual judge with a 60/100 threshold (falling back to pixel similarity if unavailable).
