\# Inference Pipeline



\## Overview



This document explains the inference pipeline for the Smart Factory AI Inspector project.



The inference pipeline takes an input image, runs defect detection using the trained YOLOv8s model, saves an annotated prediction image, and exports the prediction result as a JSON file.



\## Current Model



The current inference model is:



```text

models/yolov8s\_neu\_det\_best.pt

