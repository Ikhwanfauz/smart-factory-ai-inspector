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

