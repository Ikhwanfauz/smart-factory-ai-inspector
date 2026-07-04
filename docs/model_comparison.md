\# Model Comparison



\## Objective



This document compares the first two YOLO baseline models trained for the Smart Factory AI Inspector project.



The goal is to identify which model gives better defect detection performance on the NEU-DET steel surface defect dataset.



\## Dataset



NEU-DET Steel Surface Defect Dataset in YOLOv8 format.



\## Compared Models



| Model | Epochs | Image Size | Batch Size |

|---|---:|---:|---:|

| YOLOv8n | 30 | 640 | 8 |

| YOLOv8s | 50 | 640 | 8 |



\## Test Set Comparison



| Model | Precision | Recall | mAP50 | mAP50-95 |

|---|---:|---:|---:|---:|

| YOLOv8n 30 epochs | 0.478 | 0.593 | 0.554 | 0.273 |

| YOLOv8s 50 epochs | 0.480 | 0.573 | 0.593 | 0.303 |



\## Observation



YOLOv8s achieved better overall detection performance than YOLOv8n on the test set.



The mAP50 improved from 0.554 to 0.593, and the stricter mAP50-95 improved from 0.273 to 0.303. This suggests that YOLOv8s provides better overall detection and localization quality.



The recall of YOLOv8s is slightly lower than YOLOv8n, meaning YOLOv8n detected slightly more defect instances. However, YOLOv8s achieved better mAP scores, so it is selected as the current best baseline model.



\## Current Best Model



YOLOv8s trained for 50 epochs.



Local model path:



```text

runs/detect/baseline\_yolov8s\_50epochs/weights/best.pt

