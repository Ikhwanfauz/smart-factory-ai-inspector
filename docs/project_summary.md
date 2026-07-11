\# Smart Factory AI Inspector — Project Summary



\## Project Overview



Smart Factory AI Inspector is an end-to-end industrial AI prototype for automated steel surface quality inspection.



The system uses a YOLOv8s object detection model to identify six types of steel surface defects. It also supports optional OCR for reading product IDs, batch numbers, serial numbers, or labels from uploaded images.



The project was developed as an AI/ML engineering portfolio project and demonstrates the complete workflow from dataset preparation and model training to API deployment, database logging, analytics, containerization, and user-facing application development.



\---



\## Business Problem



Manual surface inspection in manufacturing can be:



\- slow

\- inconsistent

\- difficult to scale

\- dependent on operator experience

\- challenging to document and analyse over time



The Smart Factory AI Inspector simulates how computer vision can support quality-control teams by automatically detecting visible defects, recording inspection results, and presenting useful production analytics.



This project is a portfolio prototype and has not been validated for real production-line decision making.



\---



\## Proposed Solution



The system provides an integrated inspection workflow:



1\. A user uploads one or multiple steel surface images.

2\. Streamlit sends the image to the FastAPI backend.

3\. YOLOv8s detects and classifies surface defects.

4\. EasyOCR optionally extracts visible product or batch information.

5\. FastAPI returns structured JSON and an annotated prediction image.

6\. SQLite stores the complete inspection result.

7\. Streamlit displays inspection history, analytics, filtering, and exports.

8\. Docker Compose runs FastAPI and Streamlit as separate connected services.



\---



\## Defect Classes



The model detects six NEU-DET steel surface defect classes:



| Class ID | Defect Class |

|---:|---|

| 0 | Crazing |

| 1 | Inclusion |

| 2 | Patches |

| 3 | Pitted surface |

| 4 | Rolled-in scale |

| 5 | Scratches |



\---



\## Dataset



The project uses the NEU-DET Steel Surface Defect Dataset in YOLO format.



| Dataset Split | Images |

|---|---:|

| Training | 1,259 |

| Validation | 360 |

| Test | 180 |

| Total | 1,799 |



\---



\## Machine Learning Model



The deployed model is a YOLOv8s object detection model trained for 50 epochs.



Local model path:



```text

models/yolov8s\_neu\_det\_best.pt

