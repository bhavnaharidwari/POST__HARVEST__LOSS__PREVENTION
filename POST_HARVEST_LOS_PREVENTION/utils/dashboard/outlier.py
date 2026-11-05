import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# Outlier Dashboard

def outlier_dashboard(df: pd.DataFrame):

    st.subheader("Outlier Analysis")

    # Numeric Columns


    numeric_columns = (
        df.select_dtypes(include=np.number)
        .columns
        .tolist()
    )

    if not numeric_columns:

        st.write(
            "No numeric columns are available for outlier analysis."
        )

        return

    # Column Selection

    column = st.selectbox(
        "Select Numeric Column",
        numeric_columns,
        key="outlier_column_selector"
    )

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if series.empty:

        st.write(
            "The selected column does not contain valid numeric values."
        )

        return

    # IQR Calculation

    q1 = series.quantile(0.25)

    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr

    upper = q3 + 1.5 * iqr


    # Detect Outliers
    

    outliers = df[
        (df[column] < lower) |
        (df[column] > upper)
    ]

    outlier_count = len(outliers)

    outlier_percent = (
        (outlier_count / len(df)) * 100
        if len(df) > 0
        else 0
    )

    normal_records = len(df) - outlier_count

    # KPI Cards


    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Outliers",
            outlier_count
        )

    with c2:

        st.metric(
            "Outlier Percentage",
            f"{outlier_percent:.2f}%"
        )

    with c3:

        st.metric(
            "Normal Records",
            normal_records
        )

    st.divider()

    
    # Box Plot
    

    fig = px.box(
        df,
        y=column,
        points="outliers",
        template="plotly_white",
        title=f"Outlier Detection - {column}"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    
    # Result


    if outlier_count == 0:

        st.write(
            "No outliers detected for the selected column."
        )

        return

    
    # Outlier Records
    

    st.markdown("### Outlier Records")

    st.dataframe(
        outliers,
        use_container_width=True,
        hide_index=True
    )


    # Download Report
    

    csv = outliers.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Outlier Report",
        csv,
        "outlier_report.csv",
        "text/csv",
        use_container_width=True,
        key="outlier_download"
    )