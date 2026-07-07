import streamlit as st
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import pandas as pd

from src.ocr import run_ocr_on_image_bytes

API_URL = "http://127.0.0.1:8000"


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Smart Factory AI Inspector",
    page_icon="🏭",
    layout="wide"
)


st.title("🏭 Smart Factory AI Inspector")
st.caption("Industrial steel surface defect detection using YOLOv8 + FastAPI + Streamlit")


def check_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None


def run_prediction(uploaded_file, conf, iou):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    params = {
        "conf": conf,
        "iou": iou
    }

    response = requests.post(
        f"{API_BASE_URL}/predict",
        files=files,
        params=params,
        timeout=60
    )

    response.raise_for_status()
    return response.json()


def load_prediction_image(output_image_path):
    filename = Path(output_image_path).name

    response = requests.get(
        f"{API_BASE_URL}/prediction-image/{filename}",
        timeout=30
    )

    response.raise_for_status()
    return Image.open(BytesIO(response.content))


st.sidebar.header("Backend Connection")
st.sidebar.write(f"API URL: `{API_BASE_URL}`")

health = check_api_health()

if health is None:
    st.sidebar.error("FastAPI backend is not running.")
    st.warning(
        "Please start the FastAPI backend first:\n\n"
        "`uvicorn api.main:app --reload`"
    )
    st.stop()

if health.get("model_exists"):
    st.sidebar.success("Backend connected. Model found.")
else:
    st.sidebar.error("Backend connected, but model file is missing.")
    st.stop()


st.sidebar.header("Prediction Settings")

conf = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.05,
    max_value=0.95,
    value=0.25,
    step=0.05
)

iou = st.sidebar.slider(
    "IoU Threshold",
    min_value=0.10,
    max_value=0.90,
    value=0.30,
    step=0.05
)


uploaded_file = st.file_uploader(
    "Upload a steel surface image",
    type=["jpg", "jpeg", "png", "bmp", "webp"]
)


if uploaded_file is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Input Image")
        input_image = Image.open(uploaded_file)
        st.image(input_image, use_container_width=True)

    with col2:
        st.subheader("Inspection Result")

        if st.button("Run Inspection", type="primary"):
            with st.spinner("Running defect detection..."):
                try:
                    result = run_prediction(uploaded_file, conf, iou)

                    status = result.get("inspection_status", "UNKNOWN")
                    num_detections = result.get("num_detections", 0)
                    top_detection = result.get("top_detection")
                    detections = result.get("detections", [])

                    if status == "DEFECT_DETECTED":
                        st.error("DEFECT DETECTED")
                    else:
                        st.success("NO DEFECT DETECTED")

                    metric_col1, metric_col2 = st.columns(2)

                    with metric_col1:
                        st.metric("Number of Detections", num_detections)

                    with metric_col2:
                        if top_detection:
                            st.metric(
                                "Top Confidence",
                                f"{top_detection['confidence'] * 100:.2f}%"
                            )
                        else:
                            st.metric("Top Confidence", "N/A")

                    if top_detection:
                        st.write("### Top Detection")
                        st.write(f"**Class:** {top_detection['class_name']}")
                        st.write(f"**Confidence:** {top_detection['confidence']}")
                        st.write(f"**Bounding Box:** {top_detection['bbox_xyxy']}")

                    if detections:
                        st.write("### Detection Details")
                        df = pd.DataFrame(detections)
                        st.dataframe(df, use_container_width=True)

                    output_image_path = result.get("output_image_path")

                    if output_image_path:
                        prediction_image = load_prediction_image(output_image_path)
                        st.write("### Annotated Prediction Image")
                        st.image(prediction_image, use_container_width=True)

                    with st.expander("Raw JSON Response"):
                        st.json(result)

                except requests.exceptions.RequestException as e:
                    st.error("Prediction request failed.")
                    st.code(str(e))

else:
    st.info("Upload an image to start inspection.")

    st.divider()

st.subheader("Inspection History")

history_limit = st.number_input(
    "Number of recent inspections to show",
    min_value=5,
    max_value=100,
    value=20,
    step=5
)

if st.button("Refresh Inspection History"):
    try:
        history_response = requests.get(
            f"{API_URL}/inspections",
            params={"limit": history_limit},
            timeout=10
        )

        if history_response.status_code == 200:
            history_data = history_response.json()
            records = history_data.get("records", [])

            if records:
                history_df = pd.DataFrame(records)

                display_columns = [
                    "id",
                    "timestamp",
                    "image_name",
                    "inspection_status",
                    "defect_class",
                    "confidence",
                    "num_detections",
                    "output_image_path"
                ]

                available_columns = [
                    column for column in display_columns
                    if column in history_df.columns
                ]

                st.dataframe(
                    history_df[available_columns],
                    use_container_width=True
                )

            else:
                st.info("No inspection history found yet.")

        else:
            st.error(
                f"Failed to load inspection history. "
                f"Status code: {history_response.status_code}"
            )

    except requests.exceptions.RequestException as error:
        st.error(f"Could not connect to FastAPI backend: {error}")

        # =========================
# Version 6A: Analytics Dashboard
# =========================

st.divider()
st.subheader("📊 Analytics Dashboard")

st.write(
    "This section summarizes recent inspection history from the SQLite database."
)

analytics_limit = st.number_input(
    "Number of recent inspections for analytics",
    min_value=5,
    max_value=500,
    value=100,
    step=5,
    key="analytics_limit"
)

if st.button("Refresh Analytics Dashboard"):
    try:
        analytics_response = requests.get(
            f"{API_URL}/inspections",
            params={"limit": analytics_limit}
        )

        if analytics_response.status_code == 200:
            analytics_data = analytics_response.json()
            records = analytics_data.get("records", [])

            if len(records) == 0:
                st.info("No inspection records found yet. Run some predictions first.")
            else:
                df_analytics = pd.DataFrame(records)

                # Clean numeric columns
                if "confidence" in df_analytics.columns:
                    df_analytics["confidence"] = pd.to_numeric(
                        df_analytics["confidence"],
                        errors="coerce"
                    )

                if "num_detections" in df_analytics.columns:
                    df_analytics["num_detections"] = pd.to_numeric(
                        df_analytics["num_detections"],
                        errors="coerce"
                    ).fillna(0).astype(int)

                # Basic metrics
                total_inspections = len(df_analytics)

                defect_detected_count = (
                    df_analytics["inspection_status"] == "DEFECT_DETECTED"
                ).sum()

                no_defect_detected_count = (
                    df_analytics["inspection_status"] == "NO_DEFECT_DETECTED"
                ).sum()

                defect_rate = (
                    defect_detected_count / total_inspections * 100
                    if total_inspections > 0
                    else 0
                )

                average_confidence = df_analytics["confidence"].mean()

                # Defect-only dataframe
                defect_df = df_analytics[
                    df_analytics["inspection_status"] == "DEFECT_DETECTED"
                ].copy()

                if len(defect_df) > 0:
                    defect_df["defect_class"] = defect_df["defect_class"].fillna("unknown")

                    defect_count_by_class = (
                        defect_df["defect_class"]
                        .value_counts()
                        .reset_index()
                    )

                    defect_count_by_class.columns = ["defect_class", "count"]

                    most_common_defect = defect_count_by_class.iloc[0]["defect_class"]
                else:
                    defect_count_by_class = pd.DataFrame(
                        columns=["defect_class", "count"]
                    )
                    most_common_defect = "None"

                # Display metrics
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Total Inspections", total_inspections)

                with col2:
                    st.metric("Defect Detected", defect_detected_count)

                with col3:
                    st.metric("No Defect Detected", no_defect_detected_count)

                col4, col5, col6 = st.columns(3)

                with col4:
                    st.metric("Defect Rate", f"{defect_rate:.2f}%")

                with col5:
                    if pd.isna(average_confidence):
                        st.metric("Average Confidence", "N/A")
                    else:
                        st.metric("Average Confidence", f"{average_confidence:.4f}")

                with col6:
                    st.metric("Most Common Defect", most_common_defect)

                # Defect class table and chart
                st.markdown("### Defect Count by Class")

                if len(defect_count_by_class) == 0:
                    st.info("No defect classes found yet.")
                else:
                    st.dataframe(
                        defect_count_by_class,
                        use_container_width=True
                    )

                    chart_data = defect_count_by_class.set_index("defect_class")
                    st.bar_chart(chart_data)

                # Optional raw analytics data
                with st.expander("Show Raw Analytics Data"):
                    st.dataframe(
                        df_analytics,
                        use_container_width=True
                    )

        else:
            st.error(
                f"Failed to load analytics data. "
                f"Status code: {analytics_response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to FastAPI backend: {e}")


        # =========================
# Version 6B: Filtering + CSV Export
# =========================

st.divider()
st.subheader("🔎 Filtered Inspection History + CSV Export")

st.write(
    "Filter inspection history records and export the selected results as a CSV file."
)

filter_limit = st.number_input(
    "Number of recent inspections to load for filtering",
    min_value=5,
    max_value=1000,
    value=100,
    step=5,
    key="filter_limit"
)

# Store loaded records in session state so filters do not disappear after every click
if "filter_records" not in st.session_state:
    st.session_state["filter_records"] = []

if st.button("Load / Refresh Filter Data"):
    try:
        filter_response = requests.get(
            f"{API_URL}/inspections",
            params={"limit": filter_limit}
        )

        if filter_response.status_code == 200:
            filter_data = filter_response.json()
            st.session_state["filter_records"] = filter_data.get("records", [])

            st.success(
                f"Loaded {len(st.session_state['filter_records'])} inspection records."
            )

        else:
            st.error(
                f"Failed to load inspection records. "
                f"Status code: {filter_response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to FastAPI backend: {e}")


filter_records = st.session_state["filter_records"]

if len(filter_records) == 0:
    st.info("No filter data loaded yet. Click 'Load / Refresh Filter Data' first.")
else:
    df_filter = pd.DataFrame(filter_records)

    # Clean and prepare columns
    if "timestamp" in df_filter.columns:
        df_filter["timestamp"] = pd.to_datetime(
            df_filter["timestamp"],
            errors="coerce"
        )

    if "confidence" in df_filter.columns:
        df_filter["confidence"] = pd.to_numeric(
            df_filter["confidence"],
            errors="coerce"
        )

    if "num_detections" in df_filter.columns:
        df_filter["num_detections"] = pd.to_numeric(
            df_filter["num_detections"],
            errors="coerce"
        ).fillna(0).astype(int)

    if "inspection_status" in df_filter.columns:
        df_filter["inspection_status"] = df_filter["inspection_status"].fillna("UNKNOWN")

    if "defect_class" in df_filter.columns:
        df_filter["defect_class"] = df_filter["defect_class"].fillna("None")

    if "image_name" in df_filter.columns:
        df_filter["image_name"] = df_filter["image_name"].fillna("Unknown")

    st.markdown("### Filter Options")

    col_status, col_class = st.columns(2)

    with col_status:
        status_options = ["All"] + sorted(
            df_filter["inspection_status"].dropna().unique().tolist()
        )

        selected_status = st.selectbox(
            "Inspection Status",
            status_options,
            key="selected_status_filter"
        )

    with col_class:
        defect_class_options = ["All"] + sorted(
            df_filter["defect_class"].dropna().unique().tolist()
        )

        selected_defect_class = st.selectbox(
            "Defect Class",
            defect_class_options,
            key="selected_defect_class_filter"
        )

    confidence_range = st.slider(
        "Confidence Range",
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.01,
        key="confidence_range_filter"
    )

    include_missing_confidence = st.checkbox(
        "Include records without confidence value",
        value=True,
        key="include_missing_confidence_filter"
    )

    image_search = st.text_input(
        "Search by image name",
        value="",
        key="image_name_search_filter"
    )

    # Apply filters
    filtered_df = df_filter.copy()

    if selected_status != "All":
        filtered_df = filtered_df[
            filtered_df["inspection_status"] == selected_status
        ]

    if selected_defect_class != "All":
        filtered_df = filtered_df[
            filtered_df["defect_class"] == selected_defect_class
        ]

    min_confidence, max_confidence = confidence_range

    if "confidence" in filtered_df.columns:
        confidence_mask = (
            (filtered_df["confidence"] >= min_confidence)
            & (filtered_df["confidence"] <= max_confidence)
        )

        if include_missing_confidence:
            confidence_mask = confidence_mask | filtered_df["confidence"].isna()

        filtered_df = filtered_df[confidence_mask]

    if image_search.strip() != "":
        filtered_df = filtered_df[
            filtered_df["image_name"]
            .str.contains(image_search.strip(), case=False, na=False)
        ]

    st.markdown("### Filtered Results")

    col_total, col_filtered = st.columns(2)

    with col_total:
        st.metric("Loaded Records", len(df_filter))

    with col_filtered:
        st.metric("Filtered Records", len(filtered_df))

    if len(filtered_df) == 0:
        st.warning("No records match the selected filters.")
    else:
        st.dataframe(
            filtered_df,
            use_container_width=True
        )

        csv_data = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Filtered Results as CSV",
            data=csv_data,
            file_name="filtered_inspection_history.csv",
            mime="text/csv"
        )


# =========================
# Version 7C: Batch Image Inspection Polish
# =========================

st.divider()
st.subheader("🖼️ Batch Image Inspection")

st.write(
    "Upload multiple steel surface images and inspect them automatically using the FastAPI prediction endpoint."
)

batch_uploaded_files = st.file_uploader(
    "Upload multiple images for batch inspection",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    key="batch_uploaded_files"
)

if batch_uploaded_files:
    st.info(f"{len(batch_uploaded_files)} image(s) selected for batch inspection.")

    with st.expander("Selected Images"):
        selected_image_names = [uploaded_file.name for uploaded_file in batch_uploaded_files]
        st.write(selected_image_names)

col_batch_conf, col_batch_iou = st.columns(2)

with col_batch_conf:
    batch_confidence = st.slider(
        "Batch Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.05,
        key="batch_confidence_threshold"
    )

with col_batch_iou:
    batch_iou = st.slider(
        "Batch IoU Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.30,
        step=0.05,
        key="batch_iou_threshold"
    )

if "batch_results" not in st.session_state:
    st.session_state["batch_results"] = []

col_run_batch, col_clear_batch = st.columns(2)

with col_run_batch:
    run_batch_button = st.button("Run Batch Inspection")

with col_clear_batch:
    clear_batch_button = st.button("Clear Batch Results")

if clear_batch_button:
    st.session_state["batch_results"] = []
    st.success("Batch results cleared.")

if run_batch_button:
    if not batch_uploaded_files:
        st.warning("Please upload at least one image for batch inspection.")
    else:
        batch_results = []
        progress_bar = st.progress(0)
        status_text = st.empty()

        total_files = len(batch_uploaded_files)

        for index, uploaded_file in enumerate(batch_uploaded_files):
            status_text.write(
                f"Inspecting image {index + 1} of {total_files}: {uploaded_file.name}"
            )

            try:
                image_bytes = uploaded_file.getvalue()

                files = {
                    "file": (
                        uploaded_file.name,
                        image_bytes,
                        uploaded_file.type or "image/jpeg"
                    )
                }

                params = {
                    "conf": batch_confidence,
                    "iou": batch_iou
                }

                response = requests.post(
                    f"{API_URL}/predict",
                    files=files,
                    params=params
                )

                if response.status_code == 200:
                    result = response.json()
                    detections = result.get("detections", [])

                    if len(detections) > 0:
                        best_detection = max(
                            detections,
                            key=lambda det: det.get("confidence", 0)
                        )

                        defect_class = (
                            best_detection.get("class")
                            or best_detection.get("class_name")
                            or best_detection.get("defect_class")
                            or result.get("defect_class")
                            or "unknown"
                        )

                        confidence = best_detection.get(
                            "confidence",
                            result.get("confidence", None)
                        )

                    else:
                        defect_class = result.get("defect_class", None)
                        confidence = result.get("confidence", None)

                    batch_results.append(
                        {
                            "image_name": uploaded_file.name,
                            "inspection_status": result.get(
                                "inspection_status",
                                "UNKNOWN"
                            ),
                            "defect_class": defect_class,
                            "confidence": confidence,
                            "num_detections": result.get(
                                "num_detections",
                                0
                            ),
                            "inspection_id": result.get(
                                "inspection_id",
                                None
                            ),
                            "api_status": "SUCCESS"
                        }
                    )

                else:
                    batch_results.append(
                        {
                            "image_name": uploaded_file.name,
                            "inspection_status": "ERROR",
                            "defect_class": None,
                            "confidence": None,
                            "num_detections": None,
                            "inspection_id": None,
                            "api_status": f"FAILED: {response.status_code}"
                        }
                    )

            except requests.exceptions.RequestException as e:
                batch_results.append(
                    {
                        "image_name": uploaded_file.name,
                        "inspection_status": "ERROR",
                        "defect_class": None,
                        "confidence": None,
                        "num_detections": None,
                        "inspection_id": None,
                        "api_status": str(e)
                    }
                )

            progress_bar.progress((index + 1) / total_files)

        st.session_state["batch_results"] = batch_results
        status_text.write("Batch inspection completed.")
        st.success(f"Completed batch inspection for {len(batch_results)} image(s).")

batch_results = st.session_state["batch_results"]

if len(batch_results) > 0:
    st.markdown("### Batch Inspection Results")

    df_batch = pd.DataFrame(batch_results)

    if "confidence" in df_batch.columns:
        df_batch["confidence"] = pd.to_numeric(
            df_batch["confidence"],
            errors="coerce"
        )

    if "num_detections" in df_batch.columns:
        df_batch["num_detections"] = pd.to_numeric(
            df_batch["num_detections"],
            errors="coerce"
        ).fillna(0).astype(int)

    df_batch["defect_class"] = df_batch["defect_class"].fillna("None")

    total_batch_images = len(df_batch)

    batch_success_count = (
        df_batch["api_status"] == "SUCCESS"
    ).sum()

    batch_error_count = (
        df_batch["inspection_status"] == "ERROR"
    ).sum()

    batch_defect_count = (
        df_batch["inspection_status"] == "DEFECT_DETECTED"
    ).sum()

    batch_no_defect_count = (
        df_batch["inspection_status"] == "NO_DEFECT_DETECTED"
    ).sum()

    batch_defect_rate = (
        batch_defect_count / total_batch_images * 100
        if total_batch_images > 0
        else 0
    )

    batch_average_confidence = df_batch["confidence"].mean()

    col_b1, col_b2, col_b3, col_b4 = st.columns(4)

    with col_b1:
        st.metric("Batch Images", total_batch_images)

    with col_b2:
        st.metric("Successful", batch_success_count)

    with col_b3:
        st.metric("Defect Detected", batch_defect_count)

    with col_b4:
        st.metric("Errors", batch_error_count)

    col_b5, col_b6, col_b7 = st.columns(3)

    with col_b5:
        st.metric("No Defect Detected", batch_no_defect_count)

    with col_b6:
        st.metric("Batch Defect Rate", f"{batch_defect_rate:.2f}%")

    with col_b7:
        if pd.isna(batch_average_confidence):
            st.metric("Avg Confidence", "N/A")
        else:
            st.metric("Avg Confidence", f"{batch_average_confidence:.4f}")

    display_columns = [
        "image_name",
        "inspection_status",
        "defect_class",
        "confidence",
        "num_detections",
        "inspection_id",
        "api_status"
    ]

    existing_display_columns = [
        column for column in display_columns if column in df_batch.columns
    ]

    st.dataframe(
        df_batch[existing_display_columns],
        use_container_width=True
    )

    defect_only_batch = df_batch[
        df_batch["inspection_status"] == "DEFECT_DETECTED"
    ].copy()

    if len(defect_only_batch) > 0:
        st.markdown("### Batch Defect Class Distribution")

        batch_defect_class_counts = (
            defect_only_batch["defect_class"]
            .value_counts()
            .reset_index()
        )

        batch_defect_class_counts.columns = ["defect_class", "count"]

        st.dataframe(
            batch_defect_class_counts,
            use_container_width=True
        )

        st.bar_chart(
            batch_defect_class_counts.set_index("defect_class")
        )
    else:
        st.info("No defect class distribution to show because no defects were detected in this batch.")

    batch_csv = df_batch.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Batch Results as CSV",
        data=batch_csv,
        file_name="batch_inspection_results.csv",
        mime="text/csv"
    )


# =========================
# Version 8A: OCR Prototype
# =========================

st.divider()
st.subheader("🔤 OCR Prototype - Product / Batch ID Reading")

st.write(
    "Upload an image with visible text, such as a product label, serial number, or batch number. "
    "The OCR module will try to extract readable text from the image."
)

ocr_uploaded_file = st.file_uploader(
    "Upload image for OCR",
    type=["jpg", "jpeg", "png"],
    key="ocr_uploaded_file"
)

ocr_min_confidence = st.slider(
    "OCR Minimum Confidence",
    min_value=0.0,
    max_value=1.0,
    value=0.30,
    step=0.05,
    key="ocr_min_confidence"
)

if "ocr_result" not in st.session_state:
    st.session_state["ocr_result"] = None

if ocr_uploaded_file is not None:
    st.image(
        ocr_uploaded_file,
        caption="OCR input image",
        use_container_width=True
    )

if st.button("Run OCR"):
    if ocr_uploaded_file is None:
        st.warning("Please upload an image with visible text first.")
    else:
        try:
            with st.spinner("Running OCR... The first run may take longer."):
                image_bytes = ocr_uploaded_file.getvalue()

                ocr_result = run_ocr_on_image_bytes(
                    image_bytes=image_bytes,
                    min_confidence=ocr_min_confidence
                )

                st.session_state["ocr_result"] = ocr_result

            st.success("OCR completed.")

        except ModuleNotFoundError:
            st.error(
                "EasyOCR is not installed. Please run: pip install easyocr"
            )

        except Exception as e:
            st.error(f"OCR failed: {e}")

ocr_result = st.session_state["ocr_result"]

if ocr_result is not None:
    st.markdown("### OCR Result")

    col_ocr1, col_ocr2 = st.columns(2)

    with col_ocr1:
        st.metric("OCR Status", ocr_result.get("ocr_status", "UNKNOWN"))

    with col_ocr2:
        st.metric(
            "Text Regions",
            ocr_result.get("num_text_regions", 0)
        )

    extracted_text = ocr_result.get("extracted_text", "")

    st.markdown("### Extracted Text")

    if extracted_text:
        st.text_area(
            "OCR Text Output",
            value=extracted_text,
            height=120
        )
    else:
        st.info("No text detected above the selected confidence threshold.")

    detections = ocr_result.get("detections", [])

    if len(detections) > 0:
        st.markdown("### OCR Detection Details")

        df_ocr = pd.DataFrame(detections)

        st.dataframe(
            df_ocr,
            use_container_width=True
        )

    with st.expander("Show Raw OCR JSON"):
        st.json(ocr_result)