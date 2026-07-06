from pathlib import Path
from datetime import datetime
import sqlite3
import json


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_DIR = PROJECT_ROOT / "database"
DB_PATH = DATABASE_DIR / "inspection_logs.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


def get_connection():
    """
    Create SQLite connection.
    row_factory allows us to convert rows into dictionary-like objects later.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Create database and inspections table if they do not exist.
    """
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()


def _get_best_detection(result: dict):
    """
    Get the detection with the highest confidence.
    This makes the function flexible even if there are multiple defects.
    """
    detections = result.get("detections", [])

    if not detections:
        return None

    best_detection = max(
        detections,
        key=lambda item: item.get("confidence", 0)
    )

    return best_detection


def save_inspection_result(result: dict, image_name: str = None):
    """
    Save one inspection result into SQLite database.
    """

    init_db()

    timestamp = datetime.now().isoformat(timespec="seconds")

    final_image_name = (
        image_name
        or result.get("image_name")
        or result.get("filename")
        or "unknown_image"
    )

    inspection_status = result.get("inspection_status", "UNKNOWN")

    num_detections = result.get(
        "num_detections",
        len(result.get("detections", []))
    )

    best_detection = _get_best_detection(result)

    defect_class = None
    confidence = None

    if best_detection is not None:
        defect_class = (
            best_detection.get("class")
            or best_detection.get("class_name")
            or best_detection.get("label")
        )
        confidence = best_detection.get("confidence")

    output_image_path = (
        result.get("output_image_path")
        or result.get("annotated_image_path")
        or result.get("prediction_image_path")
    )

    json_path = (
        result.get("json_path")
        or result.get("json_output_path")
        or result.get("result_json_path")
    )

    raw_result_json = json.dumps(result, indent=2, default=str)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO inspections (
            timestamp,
            image_name,
            inspection_status,
            defect_class,
            confidence,
            num_detections,
            output_image_path,
            json_path,
            raw_result_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            final_image_name,
            inspection_status,
            defect_class,
            confidence,
            num_detections,
            output_image_path,
            json_path,
            raw_result_json,
        ),
    )

    conn.commit()
    inspection_id = cursor.lastrowid
    conn.close()

    return inspection_id


def get_recent_inspections(limit: int = 20):
    """
    Get recent inspection logs.
    This will be useful later for Version 5B dashboard history.
    """
    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            timestamp,
            image_name,
            inspection_status,
            defect_class,
            confidence,
            num_detections,
            output_image_path,
            json_path
        FROM inspections
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    init_db()
    print(f"Database ready: {DB_PATH}")