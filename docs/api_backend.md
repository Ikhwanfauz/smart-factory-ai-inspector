# FastAPI Backend

## Overview

This document explains the FastAPI backend for the Smart Factory AI Inspector project.

The backend allows a user to upload an image through an API endpoint. The uploaded image is processed by the trained YOLOv8s defect detection model. The API then returns a structured JSON response containing the inspection result, detected defect class, confidence score, and bounding box information.

## Backend Goal

The goal of this backend is to move the project from a local command-line inference script into a deployable AI inspection service.

The backend supports:

- API health check
- Image upload
- YOLOv8 defect detection
- JSON prediction response
- Local saving of uploaded images and prediction outputs

## Main API File

The FastAPI backend is implemented in:

```text
api/main.py