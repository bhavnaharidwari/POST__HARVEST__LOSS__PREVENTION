import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from pathlib import Path
from utils.prediction_form import prediction_form
from utils.prediction import predict, predict_bulk
from utils.recommendation import get_recommendations
from database.history import save_prediction
# Helper: Shelf Life
def get_shelf_life(risk):

    risk = str(risk).lower()

    if risk == "low":
        return "7 - 10 Days"

    elif risk == "medium":
        return "3 - 6 Days"

    return "1 - 2 Days"
# Helper: Download CSV


def dataframe_to_csv(df):

    return df.to_csv(


        
        index=False
    ).encode("utf-8")

# Helper: Generate Bulk PDF Report


def generate_bulk_prediction_pdf(result_df, prediction_time=""):

    from fpdf import FPDF

    class BulkPDF(FPDF):

        def header(self):

            self.set_font("Helvetica", "B", 16)

            self.set_text_color(30, 58, 138)

            self.cell(
                0, 10,
                "Post-Harvest Loss Prevention System",
                new_x="LMARGIN", new_y="NEXT",
                align="C"
            )

            self.set_font("Helvetica", "B", 12)

            self.set_text_color(71, 85, 105)

            self.cell(
                0, 7,
                "Bulk Prediction Analysis Report",
                new_x="LMARGIN", new_y="NEXT",
                align="C"
            )

            if prediction_time:

                self.set_font("Helvetica", "", 9)

                self.cell(
                    0, 5,
                    f"Generated On: {prediction_time}",
                    new_x="LMARGIN", new_y="NEXT",
                    align="C"
                )

            self.ln(4)

        def footer(self):

            self.set_y(-15)

            self.set_font("Helvetica", "I", 8)

            self.set_text_color(128, 128, 128)

            self.cell(
                0, 10,
                f"Page {self.page_no()}",
                align="C"
            )

    pdf = BulkPDF(orientation="L", unit="mm", format="A4")

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    total = len(result_df)

    low = (
        result_df["Risk Level"]
        .astype(str)
        .str.lower()
        .eq("low")
        .sum()
        if "Risk Level" in result_df else 0
    )

    med = (
        result_df["Risk Level"]
        .astype(str)
        .str.lower()
        .eq("medium")
        .sum()
        if "Risk Level" in result_df else 0
    )
    high = (
        result_df["Risk Level"]
        .astype(str)
        .str.lower()
        .eq("high")
        .sum()
        if "Risk Level" in result_df else 0
    )

    avg_conf = (
        pd.to_numeric(
            result_df["Confidence"],
            errors="coerce"
        ).mean()
        if "Confidence" in result_df else 0
    )

    pdf.set_font("Helvetica", "B", 10)

    pdf.set_fill_color(241, 245, 249)

    pdf.set_text_color(30, 41, 59)

    metrics_str = (
        f" Summary Metrics: Total Records: {total}   |   "
        f"Low Risk: {low}   |   "
        f"Medium Risk: {med}   |   "
        f"High Risk: {high}   |   "
        f"Avg Confidence: {avg_conf:.2f}%"
    )

    pdf.cell(
        0, 8,
        metrics_str,
        fill=True, border=1,
        new_x="LMARGIN", new_y="NEXT"
    )

    pdf.ln(5)

    cols = [
        "#",
        "Produce Name",
        "Category",
        "Prediction",
        "Risk Level",
        "Confidence",
        "Shelf Life"
    ]

    widths = [12, 55, 45, 50, 35, 35, 45]

    pdf.set_font("Helvetica", "B", 9)

    pdf.set_fill_color(37, 99, 235)

    pdf.set_text_color(255, 255, 255)

    for c, w in zip(cols, widths):

        pdf.cell(
            w, 7, c,
            border=1, align="C", fill=True
        )

    pdf.ln()

    pdf.set_font("Helvetica", "", 8.5)

    pdf.set_text_color(30, 41, 59)

    for idx, row in result_df.iterrows():

        p_name = str(row.get("Produce_Name", row.get("produce_name", "N/A")))[:28]

        cat = str(row.get("Category", row.get("category", "N/A")))[:22]

        pred = str(row.get("Prediction", "N/A"))[:25]

        risk = str(row.get("Risk Level", "N/A"))

        conf = f"{float(row.get('Confidence', 0)):.2f}%"

        shelf = str(row.get("Shelf Life", "N/A"))

        fill_flag = (idx % 2 == 1)

        if fill_flag:

            pdf.set_fill_color(248, 250, 252)

        else:

            pdf.set_fill_color(255, 255, 255)

        pdf.cell(widths[0], 6.5, str(idx + 1), border=1, align="C", fill=fill_flag)

        pdf.cell(widths[1], 6.5, p_name, border=1, fill=fill_flag)

        pdf.cell(widths[2], 6.5, cat, border=1, fill=fill_flag)

        pdf.cell(widths[3], 6.5, pred, border=1, fill=fill_flag)

        pdf.cell(widths[4], 6.5, risk, border=1, align="C", fill=fill_flag)

        pdf.cell(widths[5], 6.5, conf, border=1, align="C", fill=fill_flag)

        pdf.cell(widths[6], 6.5, shelf, border=1, align="C", fill=fill_flag)

        pdf.ln()

    return bytes(pdf.output())




# Prediction Page


def prediction_page():

    st.title("Prediction System")

    st.info(
        "Predict spoilage risk using the default AI model "
        "for individual produce or multiple records."
    )

    st.divider()

    
    # Prediction Mode


    prediction_mode = st.radio(
        "Prediction Mode",
        [
            "Single Prediction",
            "Bulk Prediction"
        ],
        horizontal=True,
        key="prediction_mode"
    )

    st.divider()

    
    # SINGLE PREDICTION
    

    if prediction_mode == "Single Prediction":

        st.subheader(
            "Single Prediction"
        )

        
        # Input Form
        

        form_data = prediction_form()

        st.divider()

        # Run Prediction
        

        if st.button(
            "Run Prediction",
            use_container_width=True,
            key="single_prediction_button"
        ):

            with st.spinner(
                "Generating Prediction..."
            ):

                try:

                    
                    # Run Model
                    

                    prediction, confidence, risk = predict(
                        form_data
                    )

                    model_name = (
                        "Default Random Forest Model"
                    )

                    prediction_time = (
                        datetime.now()
                        .strftime(
                            "%d-%m-%Y %H:%M:%S"
                        )
                    )

                    
                    # Save History


                    save_prediction(

                        produce_name=form_data.get(
                            "Produce_Name",
                            ""
                        ),

                        category=form_data.get(
                            "Category",
                            ""
                        ),

                        prediction=prediction,

                        confidence=confidence,

                        risk_level=risk

                    )

                    
                    # Recommendations
                    

                    recommendations = (
                        get_recommendations(
                            form_data,
                            prediction,
                            risk
                        )
                    )

                    if recommendations is None:
                        recommendations = []

                    
                    # Shelf Life
                    

                    shelf_life = get_shelf_life(
                        risk
                    )

                    
                    # Store Complete Result
                    

                    st.session_state[
                        "latest_prediction_result"
                    ] = {

                        "prediction_time":
                            prediction_time,

                        "input_data":
                            dict(form_data),

                        "prediction":
                            str(prediction),

                        "confidence":
                            float(confidence),

                        "risk":
                            str(risk),

                        "shelf_life":
                            shelf_life,

                        "recommendations":
                            list(recommendations),

                        "model_name":
                            model_name
                    }

                    
                    # Success
                    

                    st.success(
                        "Prediction Completed Successfully"
                    )

                    
                    # Prediction Summary
                    

                    st.subheader(
                        "Prediction Summary"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.caption(
                            "Prediction Status"
                        )

                        st.metric(
                            "Status",
                            prediction
                        )

                    with col2:

                        st.caption(
                            "Confidence Score"
                        )

                        st.metric(
                            "Confidence",
                            f"{float(confidence):.2f}%"
                        )

                    with col3:

                        st.caption(
                            "Risk Level"
                        )

                        st.metric(
                            "Risk",
                            risk
                        )

                    st.divider()

                    
                    # Shelf Life
                    

                    st.subheader(
                        "Estimated Shelf Life"
                    )

                    st.metric(
                        "Estimated Remaining Shelf Life",
                        shelf_life
                    )

                    st.divider()

                    
                    # Recommendations
                    

                    st.subheader(
                        "Storage Recommendations"
                    )

                    if recommendations:

                        for item in recommendations:

                            st.write(
                                str(item)
                            )

                    else:

                        st.write(
                            "Current storage conditions are acceptable."
                        )

                    st.divider()

                    
                    # Model Information
                    

                    st.subheader(
                        "Model Information"
                    )

                    info1, info2, info3 = st.columns(3)

                    with info1:

                        st.caption(
                            "Model Used"
                        )

                        st.write(
                            model_name
                        )

                    with info2:

                        st.caption(
                            "Prediction Date & Time"
                        )

                        st.write(
                            prediction_time
                        )

                    with info3:

                        st.caption(
                            "Prediction Status"
                        )

                        st.write(
                            "Completed"
                        )

                    st.divider()

                    st.info(
                        "Your complete prediction result is available "
                        "in the Results section."
                    )

                except Exception as e:

                    st.error(
                        f"Prediction Error: {e}"
                    )

    
    # BULK PREDICTION
    

    else:

        st.subheader(
            "Bulk Prediction"
        )

        st.write(
            "Upload a CSV file containing multiple produce records. "
            "The AI model will automatically generate predictions for all records."
        )

        st.divider()

        
        # Show Sample CSV Format Card BEFORE Upload (ONLY if NO file uploaded)
        

        has_uploaded_file = st.session_state.get("bulk_prediction_file") is not None

        if not has_uploaded_file:

            st.markdown(
                """
                <div style="
                    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
                    border: 1px solid #cbd5e1;
                    border-left: 5px solid #2563eb;
                    border-radius: 10px;
                    padding: 18px 22px;
                    margin-top: 5px;
                    margin-bottom: 15px;
                ">
                    <h4 style="margin: 0 0 6px 0; color: #1e293b; font-size: 17px; font-weight: 700;">
                        Download CSV Format for Testing
                    </h4>
                    <p style="margin: 0; color: #475569; font-size: 13.5px; line-height: 1.5;">
                        New to Bulk Prediction? Download our sample CSV format containing all required dataset column names (32 features) and pre-filled test records to evaluate bulk predictions instantly.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            try:
                from utils.prediction import feature_columns

                sample_csv_path = Path(__file__).resolve().parent.parent / "dataset" / "sample_bulk_prediction_template.csv"

                if sample_csv_path.exists():
                    sample_df = pd.read_csv(sample_csv_path)
                else:
                    sample_df = pd.DataFrame(columns=feature_columns)

                st.download_button(
                    label="Download Sample CSV (With Testing Data)",
                    data=sample_df.to_csv(index=False).encode("utf-8"),
                    file_name="sample_bulk_prediction_test.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_sample_testing_csv",
                    help="Click to download pre-filled sample CSV template matching dataset features."
                )

            except Exception as e:
                st.error(f"Error preparing sample CSV: {e}")

            st.divider()

        
        # CSV Upload
        

        uploaded_file = st.file_uploader(

            "Upload Prediction CSV",

            type=["csv"],

            help=(
                "Upload a CSV containing the input features "
                "required by the prediction model."
            ),

            key="bulk_prediction_file"

        )

        st.divider()

        
        # Process Uploaded File & Automatically Run Predictions
    

        if uploaded_file is not None:

            try:

                
                # Read CSV


                bulk_df = pd.read_csv(uploaded_file)

                if bulk_df.empty:

                    st.error("The uploaded CSV contains no records.")

                    return


                # Required Columns Validation
                

                try:
                    from utils.prediction import feature_columns
                    required_columns = list(feature_columns)
                except Exception:
                    required_columns = []

                existing_normalized = {
                    str(c).strip().lower().replace(" ", "_").replace("-", "_")
                    for c in bulk_df.columns
                }

                missing_columns = [
                    column
                    for column in required_columns
                    if column not in bulk_df.columns and
                       column.lower().replace(" ", "_").replace("-", "_") not in existing_normalized
                ]

                if missing_columns:

                    st.error("Required prediction columns are missing.")

                    st.write("Missing Columns:")

                    st.code("\n".join(missing_columns))

                    st.info("Please upload a CSV containing all required prediction input columns.")

                    return

                
                # Automatic Bulk Prediction Execution
                

                with st.spinner("Generating bulk predictions for all records..."):

                    result_df = predict_bulk(bulk_df)

                    result_df["Shelf Life"] = result_df["Risk Level"].apply(get_shelf_life)

                    st.session_state["bulk_prediction_results"] = result_df

                    st.session_state["bulk_prediction_time"] = (
                        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    )

            except Exception as e:

                st.error(f"Unable to process uploaded CSV: {e}")

        
        # Display Bulk Prediction Results


        if "bulk_prediction_results" in st.session_state and uploaded_file is not None:

            result_df = st.session_state["bulk_prediction_results"]

            prediction_time = st.session_state.get("bulk_prediction_time", "")

            st.success("Bulk Prediction Completed Successfully")

            st.divider()

            st.subheader("Bulk Prediction Results")

            
            # Summary Metrics

            total_predictions = len(result_df)

            low_count = (
                result_df["Risk Level"]
                .astype(str)
                .str.lower()
                .eq("low")
                .sum()
            )

            medium_count = (
                result_df["Risk Level"]
                .astype(str)
                .str.lower()
                .eq("medium")
                .sum()
            )

            high_count = (
                result_df["Risk Level"]
                .astype(str)
                .str.lower()
                .eq("high")
                .sum()
            )

            avg_confidence = (
                pd.to_numeric(
                    result_df["Confidence"],
                    errors="coerce"
                ).mean()
            )

            m1, m2, m3, m4, m5 = st.columns(5)

            with m1:
                st.metric("Total Predictions", total_predictions)

            with m2:
                st.metric("Low Risk", low_count)

            with m3:
                st.metric("Medium Risk", medium_count)

            with m4:
                st.metric("High Risk", high_count)

            with m5:
                st.metric("Avg Confidence", f"{avg_confidence:.2f}%")

            st.divider()


            # Result Table


            st.subheader("Prediction Result Table")

            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            
            # Download CSV & PDF Results
            

            st.subheader("Download Bulk Results")

            dl_col1, dl_col2 = st.columns(2)

            with dl_col1:

                csv_data = dataframe_to_csv(result_df)

                st.download_button(
                    label="Download Prediction Results CSV",
                    data=csv_data,
                    file_name="bulk_prediction_results.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_bulk_results_csv"
                )

            with dl_col2:

                try:

                    pdf_bytes = generate_bulk_prediction_pdf(
                        result_df,
                        prediction_time
                    )

                    st.download_button(
                        label="Download Prediction Results PDF",
                        data=pdf_bytes,
                        file_name="bulk_prediction_results.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key="download_bulk_results_pdf"
                    )

                except Exception as pdf_err:

                    st.warning(f"Unable to generate PDF report: {pdf_err}")

            st.divider()
            
            # Prediction Time
            
            if "bulk_prediction_time" in st.session_state:

                st.caption("Bulk Prediction Completed At")

                st.write(st.session_state["bulk_prediction_time"])