\# System Architecture



\## Overview



The Smart Factory AI Inspector is designed as an end-to-end AI inspection pipeline. The system receives an image or video input, performs defect detection and OCR, stores the inspection result, and displays the result through a dashboard.



\## Main Components



\### 1. Input Layer



The system accepts:



\- uploaded image

\- uploaded video

\- webcam image or stream in future versions



\### 2. AI Inference Layer



The AI inference layer contains:



\- defect detection model

\- OCR model



The defect detection model identifies the defect type and confidence score. The OCR model extracts visible product label or serial number information.



\### 3. Backend API



FastAPI is used to create inference endpoints. The API receives the uploaded file, runs the AI models, and returns the result in JSON format.



\### 4. Database Layer



SQLite is used in the first version to store inspection results. The database stores information such as timestamp, image name, defect type, confidence score, OCR text, and inspection status.



\### 5. Dashboard Layer



Streamlit is used to build a simple dashboard for viewing inspection results, defect statistics, and inspection history.



\## Pipeline



```text

Image / Video Upload

&#x20;       ↓

Preprocessing

&#x20;       ↓

Defect Detection Model

&#x20;       ↓

OCR Model

&#x20;       ↓

Result Formatting

&#x20;       ↓

SQLite Database

&#x20;       ↓

Streamlit Dashboard

