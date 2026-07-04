\# Test Evaluation Summary



\## Model



YOLOv8n trained for 30 epochs.



\## Dataset



NEU-DET Steel Surface Defect Dataset.



\## Test Set



| Item | Count |

|---|---:|

| Test images | 180 |

| Test instances | 264 |

| Background images | 36 |



\## Overall Test Metrics



| Metric | Value |

|---|---:|

| Precision | 0.478 |

| Recall | 0.593 |

| mAP50 | 0.554 |

| mAP50-95 | 0.273 |



\## Per-Class Performance



| Class | Images | Instances | Precision | Recall | mAP50 | mAP50-95 |

|---|---:|---:|---:|---:|---:|---:|

| crazing | 28 | 41 | 0.350 | 0.263 | 0.319 | 0.120 |

| inclusion | 34 | 80 | 0.641 | 0.800 | 0.805 | 0.374 |

| patches | 20 | 38 | 0.661 | 0.921 | 0.893 | 0.583 |

| pitted\_surface | 9 | 9 | 0.321 | 0.333 | 0.282 | 0.124 |

| rolled-in\_scale | 31 | 60 | 0.479 | 0.467 | 0.514 | 0.216 |

| scratches | 26 | 36 | 0.416 | 0.772 | 0.509 | 0.221 |



\## Observation



The baseline YOLOv8n model successfully detects steel surface defects on the test set. The strongest classes are `patches` and `inclusion`, while weaker classes include `crazing` and `pitted\_surface`.



The model has reasonable recall but lower precision, meaning it can find many defects but still produces some incorrect detections. The mAP50-95 score is still low, which shows that bounding-box localization can be improved.



\## Next Experiment



The next experiment will compare this baseline with a larger model:



\- YOLOv8s

\- 50 epochs

\- image size 640

\- batch size 8

