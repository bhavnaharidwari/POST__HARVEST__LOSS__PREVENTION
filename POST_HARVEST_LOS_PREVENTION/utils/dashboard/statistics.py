import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np



# Helper Functions


def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    """
    Return numeric columns only.
    """
    return df.select_dtypes(include=np.number).columns.tolist()


def calculate_statistics(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Calculate descriptive statistics for a numeric column.
    """

    series = pd.to_numeric(df[column], errors="coerce").dropna()

    if series.empty:
        return pd.DataFrame()

    mode_value = (
        float(series.mode().iloc[0])
        if not series.mode().empty
        else np.nan
    )

    statistics = [
        ("Count", int(series.count())),
        ("Missing Values", int(df[column].isna().sum())),
        ("Mean", float(series.mean())),
        ("Median", float(series.median())),
        ("Mode", mode_value),
        ("Standard Deviation", float(series.std())),
        ("Variance", float(series.var())),
        ("Minimum", float(series.min())),
        ("25 %", float(series.quantile(0.25))),
        ("50 %", float(series.quantile(0.50))),
        ("75 %", float(series.quantile(0.75))),
        ("Maximum", float(series.max())),
        ("Skewness", float(series.skew())),
        ("Kurtosis", float(series.kurt())),
    ]

    stats_df = pd.DataFrame(
        statistics,
        columns=["Metric", "Value"]
    )

    stats_df["Value"] = stats_df["Value"].round(3)

    return stats_df



# Dashboard

def show_statistics(df: pd.DataFrame):
    st.write("Statistics Loaded")
    st.write("Statistics Function Called")
    st.subheader("Statistical Summary")

    numeric_columns = get_numeric_columns(df)

    if not numeric_columns: 
        st.warning("No numeric columns available.")         
        return

    column = st.selectbox(
        "Numeric Column",
        numeric_columns,
        key="dataset_statistics_numeric_column_selector"
    )

    stats_df = calculate_statistics(df, column)

    if stats_df.empty:
        st.warning("No valid numeric data found.")
        return

    left, right = st.columns([1, 2])

    with left:

        st.dataframe(
            stats_df,
            hide_index=True,
            use_container_width=True
        )

        csv = stats_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Statistics",
            csv,
            f"{column}_statistics.csv",
            "text/csv",
            use_container_width=True,
            key="dataset_statistics_download"   
        )

    with right:

        fig = px.histogram(
            df,
            x=column,
            nbins=30,
            marginal="box",
            template="plotly_white",
            title=f"Distribution of {column}"
        )

        fig.update_layout(
            height=500
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )