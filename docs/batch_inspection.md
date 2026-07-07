# Batch Image Inspection

## Overview

The Batch Image Inspection feature extends the Smart Factory AI Inspector dashboard by allowing users to upload and inspect multiple steel surface images at once.

Before this feature, the dashboard supported single-image inspection only. With batch inspection, users can upload several images, run inspection for each image automatically, view a batch summary, and export the batch results as a CSV file.

This feature was added and improved in:

Version 7A: Batch Image Inspection
Version 7B: Batch Inspection Documentation
Version 7C: Batch Inspection Polish
Version 7D: Batch Dashboard Documentation Update

---

## Purpose

The purpose of batch inspection is to make the system closer to a real industrial inspection workflow.

In a real factory environment, inspection is usually not performed on only one image. Multiple product images or surface samples may need to be inspected in sequence.

The batch inspection feature helps answer questions such as:

* Can the system inspect many images in one run?
* How many images in the batch contain defects?
* What is the defect rate for the batch?
* Which defect classes were detected?
* Were there any API errors during the batch process?
* Can the batch result be exported for reporting?

---

## System Flow

The batch inspection workflow uses the existing FastAPI prediction endpoint.

The overall flow is:

```text
Multiple images uploaded in Streamlit
↓
Streamlit loops through each uploaded image
↓
Each image is sent to FastAPI /predict
↓
YOLOv8s performs defect detection
↓
FastAPI saves each result into SQLite
↓
Streamlit collects all batch results
↓
Batch result table is displayed
↓
Batch summary metrics are calculated
↓
Batch results can be downloaded as CSV
```

---

## Important Design Decision

Version 7A does not create a new FastAPI batch endpoint.

Instead, the Streamlit dashboard calls the existing endpoint repeatedly:

```text
POST /predict
```

Example concept:

```text
image 1 → /predict
image 2 → /predict
image 3 → /predict
image 4 → /predict
image 5 → /predict
```

This design keeps the backend simple and reuses the existing prediction and database logging logic.

Because every image still goes through `/predict`, each batch prediction is automatically saved into the SQLite database.

---

## FastAPI Endpoint Used

The batch inspection feature uses:

```text
POST /predict
```

This is the same endpoint used for single-image prediction.

The endpoint receives one image at a time and returns a structured JSON result containing information such as:

* inspection status
* number of detections
* defect class
* confidence score
* annotated image path
* inspection ID

---

## Streamlit Dashboard Feature

The batch inspection section is located in:

```text
dashboard/app.py
```

The section title is:

```text
Batch Image Inspection
```

Main Streamlit components used:

* multiple image uploader
* selected image counter
* selected image list expander
* confidence threshold slider
* IoU threshold slider
* run batch inspection button
* clear batch results button
* progress bar
* batch result table
* batch summary metrics
* defect class distribution table
* defect class distribution bar chart
* CSV download button



## Version 7C Dashboard Polish

Version 7C improved the batch inspection section to make it clearer, more user-friendly, and closer to a real dashboard module.

The polished batch dashboard includes:

* selected image counter
* selected image list inside an expandable section
* Run Batch Inspection button
* Clear Batch Results button
* progress bar during batch processing
* successful inspection count
* defect detected count
* no defect detected count
* batch error count
* batch defect rate
* average confidence
* cleaner result table
* defect class distribution table
* defect class distribution bar chart
* batch CSV export

These improvements make the batch inspection workflow easier to understand and easier to demonstrate during portfolio review or interview discussion.

The selected image counter helps users confirm how many images will be inspected before running the batch process.

The selected image list helps users verify the uploaded filenames.

The clear batch results button allows users to reset previous batch output before running a new test.

The improved metrics provide a fast summary of the batch quality-control result.

The defect class distribution chart helps users quickly see which defect types appeared in the uploaded batch.


---

## Multiple Image Upload

The dashboard uses Streamlit's file uploader with multiple-file support.

Supported image types:

```text
jpg
jpeg
png
```

Users can select several images from the NEU-DET test image folder or any compatible steel surface image folder.

---

## Confidence and IoU Thresholds

The batch inspection section includes separate sliders for:

* batch confidence threshold
* batch IoU threshold

These values are sent to the FastAPI `/predict` endpoint as parameters for each image.

Example values:

```text
Confidence threshold = 0.25
IoU threshold = 0.30
```

These are the same default values used in earlier single-image testing.

---

## Batch Processing Logic

When the user clicks:

```text
Run Batch Inspection
```

Streamlit processes each uploaded image one by one.

For each image:

1. The uploaded image is converted into bytes.
2. The image is sent to FastAPI using `requests.post()`.
3. FastAPI runs YOLOv8s inference.
4. FastAPI saves the result into SQLite.
5. Streamlit extracts important fields from the API response.
6. The result is added into a batch results list.

After all images are processed, the list is converted into a Pandas DataFrame and displayed in the dashboard.

---

## Batch Result Fields

The batch result table includes:

| Field             | Description                            |
| ----------------- | -------------------------------------- |
| image_name        | Uploaded image filename                |
| inspection_status | Prediction result status               |
| defect_class      | Predicted defect class                 |
| confidence        | Confidence score of the best detection |
| num_detections    | Number of detected defects             |
| inspection_id     | SQLite inspection record ID            |
| api_status        | API request status                     |

---

## Batch Summary Metrics

The dashboard calculates summary metrics for the batch.

Current batch metrics:

* Batch Images
* Defect Detected
* No Defect Detected
* Batch Errors
* Batch Defect Rate

---

## Batch Defect Rate

The batch defect rate is calculated as:

```text
batch_defect_rate = batch_defect_count / total_batch_images × 100
```

Example:

```text
8 defective images / 10 total images × 100 = 80%
```

This gives a quick quality-control summary for the uploaded batch.

---

## Error Handling

If one image fails during batch inspection, the dashboard does not stop the whole batch.

Instead, the failed image is saved into the batch result table with:

```text
inspection_status = ERROR
```

The `api_status` column shows the error information.

This makes the batch process more robust because one failed image does not cancel all other images.

---

## SQLite Logging

Each image in the batch is sent through the existing FastAPI `/predict` endpoint.

Therefore, each successful prediction is saved into the SQLite database table:

```text
inspections
```

Database file:

```text
database/inspection_logs.db
```

This means batch inspection also updates:

* inspection history
* analytics dashboard
* filtered inspection history
* CSV export from inspection history

---

## CSV Export

After batch inspection is completed, the dashboard allows the user to download the batch result as a CSV file.

Default filename:

```text
batch_inspection_results.csv
```

This file can be opened in:

* Microsoft Excel
* Google Sheets
* Pandas
* Power BI
* other reporting tools

CSV export is useful for saving inspection reports and analyzing batch-level model behavior outside the dashboard.

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
3. Scroll to the Batch Image Inspection section.
4. Upload several test images.
5. Set confidence threshold and IoU threshold.
6. Click Run Batch Inspection.
7. Wait for the progress bar to finish.
8. Check the batch result table.
9. Check the batch summary metrics.
10. Download the batch CSV file.
11. Check the inspection history section to confirm that new records were saved.
12. Refresh the analytics dashboard to confirm that batch results are included.

---

## Example Test Images

Example folder:

```text
data\raw\NEU-DET\test\images
```

Recommended first test:

```text
5 to 10 images
```

This is enough to confirm that the batch workflow, SQLite logging, and CSV export are working correctly.

---

## Portfolio Value

The batch inspection feature shows that the project is moving from a simple model demo toward a practical industrial AI inspection system.

This feature demonstrates:

* multi-image processing
* backend API integration
* automated inspection workflow
* database logging
* dashboard reporting
* CSV export
* error handling
* end-to-end system design

For an AI/ML engineer portfolio, this is valuable because it shows both model usage and software system integration.

---

## Future Improvements

Future improvements for batch inspection can include:

* dedicated FastAPI batch endpoint
* batch ZIP upload
* folder-based batch processing
* batch ID tracking
* batch-level database table
* date and time filtering
* product ID or serial number tracking with OCR
* model performance analytics per batch

