\# Changelog



All notable changes to the Smart Factory AI Inspector are documented here.



\## \[1.0.0] — 2026-07-11



\### Added



\- NEU-DET dataset exploration and documentation

\- YOLOv8n baseline training and evaluation

\- YOLOv8s model training and comparison

\- Reusable YOLO inference pipeline

\- FastAPI prediction backend

\- Annotated prediction-image endpoint

\- Streamlit inspection dashboard

\- SQLite inspection logging

\- Inspection-history display

\- Analytics dashboard

\- Filtering and CSV export

\- Batch image inspection

\- EasyOCR integration

\- OCR result storage and history display

\- Model performance dashboard

\- Professional system architecture documentation

\- Project demo screenshots

\- Dockerfile and CPU-compatible runtime dependencies

\- Docker Compose deployment for FastAPI and Streamlit

\- Persistent database and prediction-result mounts

\- Docker health checks and service networking

\- Professional project summary

\- Resume, LinkedIn, and interview portfolio materials



\### Model Performance



The deployed YOLOv8s model achieved:



| Metric | Score |

|---|---:|

| Precision | 0.4802 |

| Recall | 0.5725 |

| mAP@50 | 0.5931 |

| mAP@50–95 | 0.3032 |



\### Deployment



The complete application can be started using:



```bat

docker compose up --build

