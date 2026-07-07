# Analytics Dashboard

## Overview

The Analytics Dashboard extends the Smart Factory AI Inspector from a single-image defect detection system into a basic inspection monitoring system.

Instead of only showing the latest prediction result, the dashboard now summarizes inspection history stored in the SQLite database. This allows users to understand defect trends, inspection quality, and common defect types over recent predictions.

This feature was added in:

* Version 6A: Analytics Dashboard
* Version 6B: Filtering and CSV Export

---

## Purpose

The purpose of the analytics module is to provide a simple quality-control overview for inspection records.

The analytics dashboard helps answer questions such as:

* How many inspections have been performed?
* How many images contain defects?
* What is the defect rate?
* What is the average model confidence?
* Which defect class appears most often?
* How many detections exist for each defect class?
* Can inspection records be filtered and exported?

This makes the project more realistic as an industrial AI inspection system, because real inspection systems usually need historical tracking and reporting, not only one-time predictions.

---

## System Flow

The analytics dashboard uses inspection records that are already saved by the FastAPI backend.

The overall flow is:

```text
Image uploaded through Streamlit
↓
FastAPI receives the image
↓
YOLOv8s model performs defect detection
↓
Prediction result is saved into SQLite
↓
Streamlit requests inspection history from FastAPI
↓
Analytics dashboard summarizes the records
↓
Filtered records can be exported as CSV
```

---

## Data Source

The analytics dashboard uses the existing FastAPI inspection history endpoint:

```text
GET /inspections
```

Example request:

```text
http://127.0.0.1:8000/inspections?limit=100
```

The endpoint returns recent inspection records from the local SQLite database.

---

## SQLite Database

The inspection history is stored in:

```text
database/inspection_logs.db
```

The database table is:

```text
inspections
```

Main columns used by the analytics dashboard:

| Column            | Description                                                  |
| ----------------- | ------------------------------------------------------------ |
| id                | Unique inspection record ID                                  |
| timestamp         | Time when the inspection was saved                           |
| image_name        | Uploaded image filename                                      |
| inspection_status | Result status, such as DEFECT_DETECTED or NO_DEFECT_DETECTED |
| defect_class      | Predicted defect class                                       |
| confidence        | Model confidence score                                       |
| num_detections    | Number of detections found                                   |
| output_image_path | Path to annotated prediction image                           |
| json_path         | Path to saved JSON output, if available                      |
| raw_result_json   | Full raw prediction result in JSON format                    |

---

## Version 6A: Analytics Dashboard

Version 6A added a new analytics section to the Streamlit dashboard.

The analytics dashboard displays:

* Total inspections
* Defect detected count
* No defect detected count
* Defect rate percentage
* Average confidence
* Most common defect class
* Defect count by class table
* Defect count by class bar chart

### Total Inspections

This metric shows how many recent inspection records were loaded from the database.

### Defect Detected Count

This metric counts how many records have:

```text
inspection_status = DEFECT_DETECTED
```

### No Defect Detected Count

This metric counts how many records have:

```text
inspection_status = NO_DEFECT_DETECTED
```

### Defect Rate

The defect rate is calculated as:

```text
defect_rate = defect_detected_count / total_inspections × 100
```

This gives a quick overview of how often defects are detected in recent inspections.

### Average Confidence

The average confidence is calculated from the confidence values stored in the database.

This value gives a rough overview of how confident the model is across recent predictions.

### Most Common Defect

The most common defect is calculated from the defect_class column, using only records where a defect was detected.

### Defect Count by Class

The dashboard groups detected defects by class and displays the count for each defect type.

Example defect classes:

* crazing
* inclusion
* patches
* pitted_surface
* rolled-in_scale
* scratches

This helps identify which defect type appears most often.

---

## Version 6B: Filtering and CSV Export

Version 6B added a filtered inspection history section.

The filtering section allows users to load recent inspection records and filter them before export.

Available filters:

* Inspection status
* Defect class
* Confidence range
* Image name search

---

## Filter by Inspection Status

Users can filter records by inspection status.

Example statuses:

```text
DEFECT_DETECTED
NO_DEFECT_DETECTED
```

This makes it easier to focus only on defective or non-defective inspection results.

---

## Filter by Defect Class

Users can filter records by defect class.

Example:

```text
inclusion
scratches
patches
```

This is useful when analyzing a specific defect type.

---

## Filter by Confidence Range

Users can choose a confidence range between 0.00 and 1.00.

Example:

```text
0.50 to 1.00
```

This can be used to focus on high-confidence predictions or inspect low-confidence predictions.

Records without confidence values can also be included using the checkbox option.

---

## Search by Image Name

Users can search for inspection records by image filename.

Example:

```text
inclusion
```

This is useful when testing specific dataset images or looking for a particular inspection case.

---

## CSV Export

After filtering the inspection records, users can download the filtered results as a CSV file.

Default exported filename:

```text
filtered_inspection_history.csv
```

This feature is useful for:

* manual reporting
* external analysis
* Excel review
* sharing inspection results
* documenting model behavior

---

## Streamlit Dashboard Sections

After Version 6B, the Streamlit dashboard includes:

1. Image upload and prediction result
2. Detection result table
3. Annotated prediction image
4. Raw JSON result
5. Inspection history table
6. Analytics dashboard
7. Filtered inspection history
8. CSV export

---

## How to Run

Start the FastAPI backend:

```bash
conda activate SFAI
cd /d C:\Users\ikhwa\smart-factory-ai-inspector
python -m uvicorn api.main:app --reload
```

Start the Streamlit dashboard in another terminal:

```bash
conda activate SFAI
cd /d C:\Users\ikhwa\smart-factory-ai-inspector
python -m streamlit run dashboard/app.py
```

Open the dashboard:

```text
http://localhost:8501
```

---

## How to Test

1. Start the FastAPI backend.
2. Start the Streamlit dashboard.
3. Upload several test images.
4. Confirm that predictions are saved into SQLite.
5. Scroll to the Analytics Dashboard section.
6. Click Refresh Analytics Dashboard.
7. Check the metrics and defect class chart.
8. Scroll to the Filtered Inspection History section.
9. Click Load / Refresh Filter Data.
10. Apply filters.
11. Download the filtered CSV file.

---

## Example Use Case

A quality-control engineer uploads inspection images into the dashboard. Each prediction result is saved in the SQLite database.

After several inspections, the engineer can check:

* how many total inspections were completed
* how many defects were detected
* which defect type appeared most often
* whether the model confidence is acceptable
* whether specific defect types should be reviewed
* whether filtered inspection records should be exported for reporting

This makes the project closer to a real industrial inspection workflow.

---

## Notes

The analytics dashboard currently uses recent inspection records from SQLite.

The current analytics are simple but useful for a portfolio project. Future improvements can include:

* date range filtering
* batch inspection analytics
* daily defect trend charts
* model confidence distribution
* product ID or serial number tracking using OCR
* connection to a larger production database
