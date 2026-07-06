# SQLite Database Logging

This document explains the database logging feature in the Smart Factory AI Inspector project.

## Purpose

The SQLite database logging feature stores every inspection result produced by the FastAPI backend.

Before database logging, the system could detect defects and return the result, but the prediction history was not saved.

With database logging, each inspection is stored with useful information such as timestamp, image name, inspection status, detected defect class, confidence score, number of detections, and output image path.

This improves the project by adding traceability, which is important in real industrial inspection systems.

## System Flow

```text
User uploads image through Streamlit dashboard
        ↓
FastAPI receives the image
        ↓
YOLOv8 model performs defect detection
        ↓
Prediction result is generated
        ↓
Result is saved into SQLite database
        ↓
FastAPI returns result to dashboard
        ↓
Dashboard displays current result and inspection history