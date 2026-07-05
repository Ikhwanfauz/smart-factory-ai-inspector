from ultralytics import YOLO
from pathlib import Path
import argparse
import json
import cv2


def run_inference(
    image_path: str,
    model_path: str = "models/yolov8s_neu_det_best.pt",
    output_dir: str = "results/inference_samples",
    conf: float = 0.25
):
    image_path = Path(image_path)
    model_path = Path(model_path)
    output_dir = Path(output_dir)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    model = YOLO(str(model_path))

    results = model.predict(
        source=str(image_path),
        conf=conf,
        imgsz=640,
        save=False,
        verbose=False
    )

    result = results[0]
    names = model.names

    detections = []

    for box in result.boxes:
        class_id = int(box.cls[0].item())
        class_name = names[class_id]
        confidence = float(box.conf[0].item())

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        detections.append({
            "class_id": class_id,
            "class_name": class_name,
            "confidence": round(confidence, 4),
            "bbox_xyxy": [
                round(x1, 2),
                round(y1, 2),
                round(x2, 2),
                round(y2, 2)
            ]
        })

    annotated_image = result.plot()

    output_image_path = output_dir / f"{image_path.stem}_prediction.jpg"
    output_json_path = output_dir / f"{image_path.stem}_prediction.json"

    cv2.imwrite(str(output_image_path), annotated_image)

    prediction_result = {
        "image_path": str(image_path),
        "model_path": str(model_path),
        "confidence_threshold": conf,
        "num_detections": len(detections),
        "detections": detections
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(prediction_result, f, indent=4)

    print("\n=== Smart Factory AI Inspector Prediction ===")
    print(f"Image: {image_path}")
    print(f"Model: {model_path}")
    print(f"Detections: {len(detections)}")

    if len(detections) == 0:
        print("Result: No defect detected.")
    else:
        for i, det in enumerate(detections, start=1):
            print(
                f"{i}. {det['class_name']} | "
                f"confidence: {det['confidence']} | "
                f"bbox: {det['bbox_xyxy']}"
            )

    print(f"\nSaved image: {output_image_path}")
    print(f"Saved JSON: {output_json_path}")

    return prediction_result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run YOLOv8 defect detection inference for Smart Factory AI Inspector."
    )

    parser.add_argument(
        "--image",
        required=True,
        help="Path to input image"
    )

    parser.add_argument(
        "--model",
        default="models/yolov8s_neu_det_best.pt",
        help="Path to trained YOLO model"
    )

    parser.add_argument(
        "--output",
        default="results/inference_samples",
        help="Output folder for prediction image and JSON"
    )

    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold"
    )

    args = parser.parse_args()

    run_inference(
        image_path=args.image,
        model_path=args.model,
        output_dir=args.output,
        conf=args.conf
    )