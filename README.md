\# Smart Factory AI Inspector



An end-to-end AI inspection system for manufacturing quality control using computer vision, OCR, API deployment, and dashboard analytics.



\## Project Overview



Manual visual inspection in manufacturing can be slow, inconsistent, and difficult to scale. This project simulates an AI-assisted quality-control system that detects surface defects from product images, extracts product label or serial number information using OCR, stores inspection results, and visualizes inspection analytics through a dashboard.



The project is designed as a practical AI/ML engineering portfolio project. It focuses not only on model training, but also on deployment, inference API, database logging, dashboard analytics, and professional documentation.



\## Key Features



\- Upload image or video for inspection

\- Detect surface defects using a computer vision model

\- Extract product label or serial number using OCR

\- Store inspection results in a database

\- Display inspection history and defect statistics in a dashboard

\- Provide API endpoints for model inference

\- Prepare the system for Docker-based deployment



\## Planned Tech Stack



| Component | Tool |

|---|---|

| Defect Detection | YOLOv8 / YOLO11 |

| OCR | EasyOCR / PaddleOCR |

| Backend API | FastAPI |

| Dashboard | Streamlit |

| Database | SQLite |

| Experiment Tracking | MLflow |

| Deployment | Docker |

| Version Control | GitHub |



\## System Architecture



```text

Image / Video Upload

&#x20;       ↓

FastAPI Backend

&#x20;       ↓

Defect Detection Model + OCR

&#x20;       ↓

SQLite Database

&#x20;       ↓

Streamlit Dashboard

&#x20;       ↓

Inspection Report / Analytics

## Database Logging and Inspection History

The project includes SQLite-based inspection logging.

Every prediction request made through the FastAPI backend is automatically saved into a local SQLite database. Each inspection record stores the timestamp, uploaded image name, inspection status, detected defect class, confidence score, number of detections, and annotated output image path.

The Streamlit dashboard also includes an inspection history table, allowing recent prediction records to be viewed directly from the web interface.

Database-related files:

```text
database/schema.sql
database/db.py
docs/database_logging.md

```markdown
| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API root information |
| GET | `/health` | Backend and model health check |
| POST | `/predict` | Upload image and run YOLOv8 defect detection |
| GET | `/prediction-image/{filename}` | Retrieve annotated prediction image |
| GET | `/inspections` | Retrieve recent inspection history from SQLite |



### Version 6A–6B: Analytics Dashboard, Filtering, and CSV Export

The Streamlit dashboard includes an analytics section based on inspection records stored in SQLite.

Current analytics features:

* total inspection count
* defect detected count
* no defect detected count
* defect rate percentage
* average confidence
* most common defect class
* defect count by class table
* defect count by class bar chart
* filtered inspection history
* CSV export for filtered records

Documentation:

```text
docs/analytics_dashboard.md
```


### Version 7A–7D: Batch Image Inspection

The Streamlit dashboard supports batch image inspection.

Users can upload multiple steel surface images, run inspection for each image through the FastAPI `/predict` endpoint, view batch-level summary metrics, and download the batch result as a CSV file.

Current batch inspection features:

* multiple image upload
* repeated FastAPI `/predict` calls
* confidence threshold control
* IoU threshold control
* selected image counter
* selected image list
* progress bar during inspection
* clear batch results button
* batch result table
* successful inspection count
* batch defect count
* batch no-defect count
* batch error count
* batch defect rate
* average confidence
* defect class distribution table
* defect class distribution bar chart
* CSV export for batch results
* automatic SQLite logging for each successful prediction


Documentation:

```text
docs/batch_inspection.md
```

### Version 8A–8D: OCR Integration

The project includes OCR support for reading visible text such as product IDs, batch numbers, serial numbers, or labels.

OCR features:

- standalone OCR prototype in Streamlit
- optional OCR during main inspection
- OCR result returned by FastAPI `/predict`
- OCR result saved into SQLite
- OCR status shown in inspection history
- OCR text shown in inspection history
- OCR text region count shown in inspection history

OCR database fields:

- `ocr_status`
- `ocr_text`
- `ocr_num_text_regions`
- `raw_ocr_json`

Documentation:

```text
docs/ocr_integration.md



---

## Version 9 — Model Performance Dashboard

Version 9 adds model evaluation visibility to the Smart Factory AI Inspector.

The project now shows not only inspection results, but also the machine learning performance of the deployed YOLOv8s model.

### Version 9A — Model Performance Dashboard

The Streamlit dashboard now includes:

* Precision
* Recall
* mAP@50
* mAP@50–95
* Evaluation result table
* Performance bar chart
* Metric explanations
* Model information
* Dataset information

### Version 9B — Model Performance Documentation

Detailed model evaluation documentation is available at:

```text
docs/model_performance.md
```

The documentation explains:

* NEU-DET dataset distribution
* YOLOv8s model configuration
* Evaluation metrics
* Performance interpretation
* Reasons for selecting YOLOv8s
* Current model limitations
* Possible future improvements

### Current YOLOv8s Test Performance

| Metric    |  Score |
| --------- | -----: |
| Precision | 0.4802 |
| Recall    | 0.5725 |
| mAP@50    | 0.5931 |
| mAP@50–95 | 0.3032 |

The current production model is:

```text
models/yolov8s_neu_det_best.pt
```

The model was trained for 50 epochs using the NEU-DET steel surface defect dataset.

Version 9 demonstrates knowledge of model evaluation, performance interpretation, and deployment—not only application development.


