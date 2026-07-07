import streamlit as st
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import pandas as pd

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