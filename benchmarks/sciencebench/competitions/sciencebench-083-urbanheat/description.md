# ScienceBench Task 83

## Overview

- Domain: Geographical Information Science
- Subtask Categories: Geospatial Analysis, Map Visualization
- Source: https://github.com/GeoStat-Framework/PyKrige
- Expected Output: interpolated_urban_heat.png
- Output Type: Image

## Task

Your task is to analyze urban heat using Kriging interpolation techniques in Python. The analysis should focus on understanding spatial patterns of urban heat islands by using point temperature data and interpolating these values across a city. You also have to use a demographical layer to extract and enhance the data visualization on the elder group. Your goal is to load the temperature sample data, apply the Kriging method to predict temperature across the urban area, and generate a choropleth map showing the average interpolated temperature surface in each census block group. The final output should be saved as "output file".

## Dataset

[START Dataset Preview: UrbanHeat]
|-- CensusBlock.geojson
|-- Temperature.geojson
[END Dataset Preview]


## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.
