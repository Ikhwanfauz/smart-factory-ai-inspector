CREATE TABLE IF NOT EXISTS inspections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    image_name TEXT NOT NULL,
    inspection_status TEXT NOT NULL,
    defect_class TEXT,
    confidence REAL,
    num_detections INTEGER NOT NULL,
    output_image_path TEXT,
    json_path TEXT,
    raw_result_json TEXT,
    ocr_status TEXT,
    ocr_text TEXT,
    ocr_num_text_regions INTEGER,
    raw_ocr_json TEXT
);