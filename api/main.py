from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import sys
import uuid

# Make project root importable
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.predict import run_inference


app = FastAPI(
    title="Smart Factory AI Inspector API",
    description="FastAPI backend for steel surface defect detection using YOLOv8.",
    version="3A"
)

MODEL_PATH = ROOT_DIR / "models" / "yolov8s_neu_det_best.pt"
UPLOAD_DIR = ROOT_DIR / "results" / "api_uploads"
PREDICTION_DIR = ROOT_DIR / "results" / "api_predictions"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


@app.get("/")
def root():
    return {
        "project": "Smart Factory AI Inspector",
        "version": "3A",
        "message": "FastAPI backend is running.",
        "docs": "/docs",
        "health": "/health",
        "predict_endpoint": "/predict"
    }


@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "model_exists": MODEL_PATH.exists(),
        "model_path": str(MODEL_PATH)
    }


@app.post("/predict")
async def predict_defect(
    file: UploadFile = File(...),
    conf: float = 0.25,
    iou: float = 0.30
):
    if not MODEL_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Model file not found: {MODEL_PATH}"
        )

    original_filename = Path(file.filename).name
    file_extension = Path(original_filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_extension}. Allowed: {sorted(ALLOWED_EXTENSIONS)}"
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    PREDICTION_DIR.mkdir(parents=True, exist_ok=True)

    unique_filename = f"{Path(original_filename).stem}_{uuid.uuid4().hex[:8]}{file_extension}"
    upload_path = UPLOAD_DIR / unique_filename

    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    with open(upload_path, "wb") as f:
        f.write(file_bytes)

    prediction_result = run_inference(
        image_path=str(upload_path),
        model_path=str(MODEL_PATH),
        output_dir=str(PREDICTION_DIR),
        conf=conf,
        iou=iou
    )

    return prediction_result


@app.get("/prediction-image/{filename}")
def get_prediction_image(filename: str):
    image_path = PREDICTION_DIR / filename

    if not image_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Prediction image not found: {filename}"
        )

    return FileResponse(image_path)