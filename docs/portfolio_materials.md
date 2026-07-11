\# Smart Factory AI Inspector — Portfolio Materials



\## Resume Project Title



\*\*Smart Factory AI Inspector — End-to-End Computer Vision Inspection System\*\*



\---



\## Resume Description



Developed an end-to-end AI inspection prototype for detecting steel surface defects using YOLOv8s, FastAPI, Streamlit, SQLite, EasyOCR, and Docker Compose.



\---



\## Recommended Resume Bullets



\- Developed and evaluated a six-class YOLOv8s steel surface defect detection model using the NEU-DET dataset, achieving 0.5931 mAP@50 and 0.5725 recall on 180 test images.



\- Built a reusable computer vision inference pipeline and FastAPI backend that supports configurable confidence and IoU thresholds, JSON prediction output, annotated images, and inspection-history endpoints.



\- Designed a Streamlit dashboard for single-image and batch inspection, including defect analytics, filtering, CSV export, model-performance reporting, and optional EasyOCR product or batch ID extraction.



\- Integrated SQLite logging for YOLO and OCR results, including safe database schema migration, inspection history, defect-rate analysis, confidence metrics, and defect-class distributions.



\- Containerized the FastAPI backend and Streamlit dashboard as separate services using Docker Compose, with internal service networking, health checks, persistent runtime data, and mounted model weights.



\---



\## Compact Three-Bullet Resume Version



Use this version when resume space is limited:



\- Developed a six-class YOLOv8s steel surface defect detection system using the NEU-DET dataset, achieving 0.5931 mAP@50 and 0.5725 recall on the test set.



\- Built FastAPI and Streamlit applications for single-image and batch inspection, annotated predictions, EasyOCR extraction, SQLite logging, analytics, filtering, and CSV export.



\- Deployed the application using Docker Compose with separate API and dashboard containers, service health checks, persistent inspection data, and mounted model weights.



\---



\## One-Line Resume Version



Built an end-to-end steel surface defect inspection system using YOLOv8s, FastAPI, Streamlit, EasyOCR, SQLite, and Docker Compose.



\---



\## LinkedIn Project Description



I developed the Smart Factory AI Inspector, an end-to-end computer vision project for automated steel surface quality inspection.



The project uses a YOLOv8s object detection model trained on the NEU-DET dataset to detect six steel surface defect classes. I developed a reusable Python inference pipeline, exposed model predictions through FastAPI, and built a Streamlit dashboard for single-image and batch inspection.



The application also includes optional EasyOCR processing for product or batch ID reading, SQLite inspection logging, inspection history, analytics, filtering, CSV export, and model-performance reporting.



For deployment, I containerized the FastAPI and Streamlit applications as separate services using Docker Compose. The containers communicate through an internal Docker network while model weights, database records, uploaded images, and prediction outputs are stored through mounted directories.



This project helped me strengthen my practical skills in computer vision, API development, OCR integration, database design, dashboard development, Docker deployment, debugging, and technical documentation.



\### Technology Stack



`Python` `YOLOv8` `PyTorch` `FastAPI` `Streamlit` `EasyOCR` `SQLite` `OpenCV` `Pandas` `Docker` `Docker Compose`



\---



\## Short LinkedIn Version



Developed an end-to-end steel surface defect inspection prototype using YOLOv8s, FastAPI, Streamlit, EasyOCR, SQLite, and Docker Compose.



The system supports six-class defect detection, single and batch inspection, annotated predictions, optional OCR, database logging, analytics, filtering, CSV export, and model-performance reporting.



The YOLOv8s model achieved 0.5931 mAP@50 and 0.5725 recall on the NEU-DET test dataset.



\---



\## GitHub Repository Description



End-to-end steel surface defect inspection system using YOLOv8s, FastAPI, Streamlit, EasyOCR, SQLite, analytics, batch processing, and Docker Compose.



\---



\## 30-Second Interview Pitch



The Smart Factory AI Inspector is an end-to-end computer vision project that detects six types of steel surface defects using YOLOv8s.



I trained and evaluated the model on the NEU-DET dataset, built a reusable inference pipeline, and deployed it through FastAPI. I also created a Streamlit dashboard for single-image and batch inspection, optional OCR, inspection history, analytics, filtering, and CSV export.



Finally, I containerized FastAPI and Streamlit as separate services using Docker Compose. The project demonstrates the complete AI engineering workflow from model development to deployment.



\---



\## 60-Second Interview Pitch



My Smart Factory AI Inspector project is an end-to-end AI quality-inspection prototype for detecting steel surface defects.



I used the NEU-DET dataset, which contains six defect classes, and trained both YOLOv8n and YOLOv8s models. I selected YOLOv8s as the deployed model based on its stronger evaluation results. It achieved 0.5931 mAP@50, 0.5725 recall, and 0.4802 precision on the test dataset.



After training, I developed a reusable Python inference pipeline and integrated it with FastAPI. The API handles image uploads, model inference, configurable thresholds, annotated prediction images, JSON results, optional OCR, and SQLite inspection logging.



I then built a Streamlit dashboard for single-image inspection, batch processing, inspection history, analytics, filtering, CSV export, and model-performance visualization.



For deployment, I used Docker Compose to run FastAPI and Streamlit as separate containers connected through an internal network. This project allowed me to practise model development, API integration, database design, dashboard development, deployment, debugging, and documentation.



\---



\## Detailed Interview Explanation



\### 1. What problem does the project solve?



The project simulates automated visual quality inspection for manufacturing.



Manual inspection can be slow, inconsistent, and difficult to scale. The system uses computer vision to detect visible steel surface defects and stores inspection results for later analysis.



\### 2. Why did you choose YOLOv8?



YOLOv8 provides a practical balance between object-detection performance, inference speed, model size, and ease of deployment.



I compared YOLOv8n and YOLOv8s. YOLOv8s produced the stronger available results and was therefore selected as the deployed model.



\### 3. Why did you use FastAPI?



FastAPI separates the machine learning inference logic from the user interface.



The backend provides prediction, health-check, annotated-image, and inspection-history endpoints. This makes the model easier to integrate with other applications.



\### 4. Why did you use Streamlit?



Streamlit allowed me to build an interactive dashboard quickly while remaining focused on Python.



The dashboard supports image upload, threshold controls, OCR, single and batch inspection, history, analytics, charts, filtering, and CSV export.



\### 5. Why did you use SQLite?



SQLite is lightweight and appropriate for a local portfolio prototype.



It allowed me to implement persistent inspection logging without requiring an external database server.



\### 6. Why did you add OCR?



In industrial environments, product images may include serial numbers, batch IDs, or labels.



EasyOCR was added as an optional feature so the system can save visible text together with the defect-inspection result.



\### 7. Why did you use Docker Compose?



The project has two applications: FastAPI and Streamlit.



Docker Compose allows both services to run in separate containers with one command. It also demonstrates internal service networking, health checks, persistent data, and reproducible deployment.



\### 8. What was the most difficult part?



The most challenging part was integrating multiple components into one reliable workflow.



The project required debugging API requests, database schema updates, OCR initialization, file paths, Streamlit state, Docker networking, model mounting, and container startup order.



\### 9. What would you improve next?



I would collect more real industrial data, perform hyperparameter tuning, evaluate class-level metrics, improve bounding-box localization, add authentication, replace SQLite with a production database, and deploy the system to a cloud environment.



\---



\## STAR Interview Answer



\### Situation



Manual visual inspection in manufacturing can be inconsistent and difficult to scale, while many machine learning portfolio projects stop after model training.



\### Task



I wanted to build a complete AI inspection prototype that demonstrated not only computer vision modelling but also deployment, database logging, analytics, OCR, and containerization.



\### Action



I trained and evaluated YOLOv8 models on the NEU-DET dataset, selected YOLOv8s as the deployed model, built a reusable inference pipeline, created FastAPI endpoints, integrated SQLite and EasyOCR, developed a Streamlit dashboard, added batch processing and analytics, and deployed the system using Docker Compose.



\### Result



The final application supports end-to-end defect inspection, optional OCR, inspection history, analytics, CSV export, batch processing, model-performance reporting, and reproducible local deployment.



The deployed model achieved 0.5931 mAP@50 and 0.5725 recall on the test dataset.



\---



\## Honest Limitation Statement



This project is an engineering portfolio prototype and has not been validated for autonomous production-line quality decisions.



The current model performance represents a functional baseline. Additional real industrial data, tuning, validation, monitoring, and safety controls would be necessary before production deployment.



\---



\## Skills Demonstrated



\- Python

\- Computer vision

\- Object detection

\- YOLOv8

\- PyTorch

\- Model training and evaluation

\- FastAPI

\- REST API development

\- Streamlit

\- EasyOCR

\- SQLite

\- Pandas

\- OpenCV

\- Batch processing

\- Data visualization

\- Docker

\- Docker Compose

\- Git and GitHub

\- Technical documentation

\- Debugging and system integration

