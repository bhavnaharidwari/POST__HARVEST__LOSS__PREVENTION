import streamlit as st
import pandas as pd


def show_dataset_insights(df: pd.DataFrame):

    # Dataset Statistics

    total_records = len(df)

    total_columns = len(df.columns)

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    # Dataset Insights
    

    st.write(
        f"Dataset contains {total_records:,} records."
    )

    st.write(
        f"Dataset has {total_columns} columns."
    )

    st.write(
        f"Missing Values: {missing_values}"
    )

    st.write(
        f"Duplicate Rows: {duplicate_rows}"
    )


    # Additional Insights


    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    categorical_columns = df.select_dtypes(
        include="object"
    ).columns

    st.write(
        f"Numerical Columns: {len(numerical_columns)}"
    )

    st.write(
        f"Categorical Columns: {len(categorical_columns)}"
    )

    # Dataset Quality
    

    if missing_values == 0 and duplicate_rows == 0:

        st.write(
            "Dataset quality check: No missing values or duplicate rows detected."
        )

    elif missing_values > 0 and duplicate_rows > 0:

        st.write(
            "Dataset quality check: Missing values and duplicate rows are present."
        )

    elif missing_values > 0:

        st.write(
            "Dataset quality check: Missing values are present."
        )

    elif duplicate_rows > 0:

        st.write(
            "Dataset quality check: Duplicate rows are present."
        )