# OCR Integration

## Overview

The OCR integration extends the Smart Factory AI Inspector by adding text recognition capability to the inspection workflow.

Before OCR integration, the system only detected steel surface defects using YOLOv8. With OCR, the system can also read visible text from uploaded images, such as product IDs, batch numbers, serial numbers, or labels.

This feature was added in:

- Version 8A: OCR Prototype
- Version 8B: Save OCR Results into SQLite
- Version 8C: Show OCR Results in Inspection History
- Version 8D: OCR Documentation

---

## Purpose

The purpose of OCR is to connect visual defect inspection with product or batch identification.

In a real factory environment, defect inspection is more useful when each result can be linked to a specific product, batch, or serial number.

Example use cases:

- read product ID from label
- read batch number from packaging
- read serial number from inspected part
- connect defect history with production tracking
- improve traceability in quality-control reports

---

## System Flow

The OCR-enabled inspection flow is:

```text
Upload image in Streamlit
↓
FastAPI receives image
↓
YOLOv8s detects steel surface defects
↓
Optional OCR runs if enabled
↓
Prediction result and OCR result are saved into SQLite
↓
Dashboard displays inspection result
↓
Inspection history shows OCR status and OCR text