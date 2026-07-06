# Streamlit Dashboard Guide

## Overview

This document explains how to run and use the Streamlit dashboard for the Smart Factory AI Inspector project.

The dashboard provides a simple user interface for uploading steel surface images, sending them to the FastAPI backend, running YOLOv8 defect detection, and displaying the inspection result.

## Dashboard Goal

The goal of the dashboard is to make the AI inspection system easy to use and easy to demonstrate.

Instead of running prediction from the terminal or Swagger API page, the user can upload an image through a web interface and view the result visually.

## Main Dashboard File

The dashboard is implemented in:

```text
dashboard/app.py
```

## System Flow

The dashboard works together with the FastAPI backend.

```text
User uploads image
        ↓
Streamlit dashboard
        ↓
FastAPI backend
        ↓
YOLOv8s defect detection model
        ↓
JSON response + annotated image
        ↓
Dashboard displays result
```

## Requirements

Before running the dashboard, make sure the required packages are installed:

```bash
pip install streamlit requests pillow
```

These packages are also included in:

```text
requirements.txt
```

## Run the FastAPI Backend First

The dashboard depends on the FastAPI backend. Therefore, the backend must be running first.

Open Terminal 1:

```bash
conda activate SFAI
cd /d C:\Users\ikhwa\smart-factory-ai-inspector
uvicorn api.main:app --reload
```

If `uvicorn` is not recognized, use:

```bash
python -m uvicorn api.main:app --reload
```

The backend should run at:

```text
http://127.0.0.1:8000
```

## Run the Streamlit Dashboard

Open Terminal 2:

```bash
conda activate SFAI
cd /d C:\Users\ikhwa\smart-factory-ai-inspector
streamlit run dashboard/app.py
```

If `streamlit` is not recognized, use:

```bash
python -m streamlit run dashboard/app.py
```

The dashboard should open in the browser at:

```text
http://localhost:8501
```

## Dashboard Features

The dashboard includes:

- Backend connection status
- Image uploader
- Confidence threshold slider
- IoU threshold slider
- Inspection result display
- Number of detections
- Top confidence score
- Detected defect class
- Detection details table
- Annotated prediction image
- Raw JSON response viewer

## Prediction Settings

### Confidence Threshold

The confidence threshold controls how confident the model must be before accepting a detection.

A higher confidence threshold gives fewer but stronger detections.

A lower confidence threshold may detect difficult defects but can increase false positives.

Default value:

```text
0.25
```

### IoU Threshold

The IoU threshold controls duplicate box suppression.

A lower IoU value can help remove overlapping duplicate boxes.

Default value:

```text
0.30
```

## Recommended Test Image

A good test image is:

```text
data/raw/NEU-DET/test/images/inclusion_97_jpg.rf.a6dcfde75d5c8ac13e21fafae9158e8f.jpg
```

Recommended settings:

```text
Confidence Threshold = 0.25
IoU Threshold = 0.30
```

Expected result:

```text
Inspection Status: DEFECT_DETECTED
Detected Class: inclusion
Top Confidence: around 74.91%
Number of Detections: 1
```

## Output Explanation

When the dashboard runs inspection, it receives a JSON response from the FastAPI backend.

Important fields include:

```text
inspection_status
num_detections
class_counts
top_detection
detections
output_image_path
output_json_path
```

The annotated prediction image is loaded from the backend and displayed in the dashboard.

## Inspection Status

The dashboard shows one of two main statuses:

```text
DEFECT DETECTED
NO DEFECT DETECTED
```

`DEFECT DETECTED` means the model found at least one defect above the selected confidence threshold.

`NO DEFECT DETECTED` means no defect was detected above the selected confidence threshold.

## Notes

The dashboard is currently designed for local development.

The FastAPI backend runs on:

```text
http://127.0.0.1:8000
```

The Streamlit dashboard runs on:

```text
http://localhost:8501
```

Both must be running at the same time for the dashboard to work.

## Current Version

This dashboard is part of:

```text
Version 4A: Streamlit Dashboard Starter
Version 4B: Dashboard Documentation + Demo Guide
```