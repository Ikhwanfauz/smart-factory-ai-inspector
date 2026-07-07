from io import BytesIO
from typing import Any, Dict, List

import numpy as np
from PIL import Image


_OCR_READER = None


def get_ocr_reader():
    """
    Load EasyOCR reader once and reuse it.

    Note:
    The first run may take longer because EasyOCR loads the OCR model.
    """
    global _OCR_READER

    if _OCR_READER is None:
        import easyocr

        # English OCR first.
        # gpu=False keeps it safe for CPU usage.
        _OCR_READER = easyocr.Reader(["en"], gpu=False)

    return _OCR_READER


def run_ocr_on_image_bytes(
    image_bytes: bytes,
    min_confidence: float = 0.30
) -> Dict[str, Any]:
    """
    Run OCR on image bytes and return structured OCR result.

    Args:
        image_bytes: Uploaded image bytes.
        min_confidence: Minimum OCR confidence threshold.

    Returns:
        Dictionary containing OCR status, extracted text, and detections.
    """
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image_array = np.array(image)

    reader = get_ocr_reader()

    raw_results = reader.readtext(image_array)

    detections: List[Dict[str, Any]] = []

    for bbox, text, confidence in raw_results:
        confidence_value = float(confidence)

        if confidence_value >= min_confidence:
            detections.append(
                {
                    "text": str(text),
                    "confidence": confidence_value,
                    "bbox": [
                        [float(point[0]), float(point[1])]
                        for point in bbox
                    ],
                }
            )

    extracted_text = " ".join(
        detection["text"] for detection in detections
    ).strip()

    ocr_status = (
        "TEXT_DETECTED"
        if len(detections) > 0
        else "NO_TEXT_DETECTED"
    )

    return {
        "ocr_status": ocr_status,
        "num_text_regions": len(detections),
        "extracted_text": extracted_text,
        "detections": detections,
    }