\# Baseline Training Summary



\## Model



YOLOv8n



\## Dataset



NEU-DET Steel Surface Defect Dataset in YOLOv8 format.



\## Training Configuration



| Parameter | Value |

|---|---|

| Model | yolov8n.pt |

| Epochs | 30 |

| Image Size | 640 |

| Batch Size | 8 |

| Device | GPU |

| Workers | 0 |



\## Final Epoch Metrics



| Metric | Value |

|---|---:|

| Precision | 0.51547 |

| Recall | 0.57367 |

| mAP50 | 0.57628 |

| mAP50-95 | 0.29498 |



\## Observation



The baseline model successfully learned from the dataset. The mAP50 improved from 0.14451 at epoch 1 to 0.57628 at epoch 30. This confirms that the dataset, training pipeline, and YOLO configuration are working correctly.



However, the model is not final yet. The mAP50-95 score is still relatively low, which suggests that localization accuracy and stricter detection quality can be improved.



\## Possible Improvements



\- Train for more epochs

\- Try a larger model such as YOLOv8s

\- Compare YOLOv8n vs YOLOv8s

\- Analyze per-class performance

\- Add controlled data augmentation

\- Tune confidence threshold

