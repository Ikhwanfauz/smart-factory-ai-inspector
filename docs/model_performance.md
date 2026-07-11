# Model Performance

## Overview

The Smart Factory AI Inspector uses a YOLOv8 object detection model to identify steel surface defects from uploaded images.

The current model used by the inference pipeline, FastAPI backend, and Streamlit dashboard is:

```text
models/yolov8s_neu_det_best.pt
```

This model is based on YOLOv8s and was trained for 50 epochs using the NEU-DET Steel Surface Defect Dataset.

---

## Dataset

The NEU-DET dataset contains six steel surface defect classes:

| Class ID | Defect Class    |
| -------- | --------------- |
| 0        | crazing         |
| 1        | inclusion       |
| 2        | patches         |
| 3        | pitted_surface  |
| 4        | rolled-in_scale |
| 5        | scratches       |

Dataset distribution:

| Dataset Split | Number of Images |
| ------------- | ---------------: |
| Training      |            1,259 |
| Validation    |              360 |
| Test          |              180 |
| Total         |            1,799 |

The dedicated test dataset was used to evaluate the final trained model.

---

## Current Model

| Property                | Value                                                   |
| ----------------------- | ------------------------------------------------------- |
| Model architecture      | YOLOv8s                                                 |
| Training epochs         | 50                                                      |
| Dataset                 | NEU-DET                                                 |
| Number of classes       | 6                                                       |
| Test images             | 180                                                     |
| Local model path        | `models/yolov8s_neu_det_best.pt`                        |
| Original trained weight | `runs/detect/baseline_yolov8s_50epochs/weights/best.pt` |

The trained `.pt` model files are excluded from Git because model weights are large runtime artifacts.

---

## Evaluation Results

The YOLOv8s model achieved the following results on the NEU-DET test dataset:

| Metric    |  Score | Percentage |
| --------- | -----: | ---------: |
| Precision | 0.4802 |     48.02% |
| Recall    | 0.5725 |     57.25% |
| mAP@50    | 0.5931 |     59.31% |
| mAP@50–95 | 0.3032 |     30.32% |

Full evaluation values:

```text
Precision: 0.4801818699198428
Recall: 0.5725307719081977
mAP@50: 0.5931250558972471
mAP@50–95: 0.30323180922386844
```

---

## Metric Explanation

### Precision

Precision measures how many predicted defect detections were correct.

A precision score of 0.4802 means that approximately 48.02% of the model's predicted defect detections matched actual defects.

Higher precision means fewer false-positive detections.

### Recall

Recall measures how many actual defects in the test dataset were successfully detected.

A recall score of 0.5725 means that the model detected approximately 57.25% of the actual defects.

Higher recall means fewer defects are missed by the model.

### mAP@50

mAP@50 measures the model's overall object detection performance using an Intersection over Union threshold of 0.50.

The model achieved an mAP@50 score of 0.5931, equivalent to 59.31%.

This indicates moderate defect detection performance under the standard IoU threshold.

### mAP@50–95

mAP@50–95 calculates the mean Average Precision across multiple IoU thresholds from 0.50 to 0.95.

The model achieved an mAP@50–95 score of 0.3032, equivalent to 30.32%.

This metric is stricter because the predicted bounding boxes must align more accurately with the ground-truth defect locations.

---

## Performance Interpretation

The evaluation results show that the model can identify multiple types of steel surface defects, but there is still room for improvement.

The recall is higher than the precision, which means the model can find a reasonable number of actual defects but may also produce some incorrect detections.

The difference between mAP@50 and mAP@50–95 indicates that defect classification is generally stronger than precise bounding-box localization.

Steel surface defects can be challenging to detect because:

* Some defect classes have similar visual textures.
* Certain defects are small or have unclear boundaries.
* Lighting and image contrast can affect defect visibility.
* The dataset contains a limited number of training images.
* Surface patterns may be confused with actual defects.

---

## Why YOLOv8s Is Used

YOLOv8s is currently used as the main model because it provides the strongest available balance between:

* Detection performance
* Inference speed
* Model size
* FastAPI integration
* Streamlit dashboard usage
* CPU and GPU deployment compatibility

The model is suitable for demonstrating an end-to-end industrial AI inspection workflow while remaining practical for local deployment.

---

## Dashboard Integration

The Streamlit Model Performance Dashboard displays:

* Precision
* Recall
* mAP@50
* mAP@50–95
* Evaluation results table
* Performance bar chart
* Metric explanations
* Model and dataset information

This allows users to understand both the system's inspection capabilities and the machine learning evaluation behind the application.

---

## Possible Future Improvements

Future model improvements may include:

* Training for more epochs
* Increasing the dataset size
* Improving class balance
* Applying additional image augmentation
* Testing larger YOLO architectures
* Performing hyperparameter tuning
* Evaluating confidence and IoU threshold combinations
* Reviewing class-level precision and recall
* Analysing the confusion matrix
* Testing the model on real industrial images

---

## Conclusion

The YOLOv8s model provides a functional baseline for detecting steel surface defects within the Smart Factory AI Inspector.

The model is fully integrated with the inference pipeline, FastAPI backend, Streamlit dashboard, SQLite inspection logging, analytics, batch inspection, and optional OCR processing.

The Model Performance Dashboard and this documentation demonstrate that the project covers not only application development but also model evaluation and performance interpretation.
