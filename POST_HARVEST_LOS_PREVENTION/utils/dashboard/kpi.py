import streamlit as st
import pandas as pd


def show_kpi_cards(df: pd.DataFrame):

    
    # Dataset Statistics

    total_records = len(df)

    total_columns = len(df.columns)

    numerical_columns = len(
        df.select_dtypes(include="number").columns
    )

    categorical_columns = len(
        df.select_dtypes(include="object").columns
    )

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )


    # KPI Display


    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Total Records",
            f"{total_records:,}"
        )

    with c2:
        st.metric(
            "Total Columns",
            total_columns
        )

    with c3:
        st.metric(
            "Missing Values",
            missing_values
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        st.metric(
            "Duplicate Rows",
            duplicate_rows
        )

    with c5:
        st.metric(
            "Numerical Columns",
            numerical_columns
        )

    with c6:
        st.metric(
            "Categorical Columns",
            categorical_columns
        )