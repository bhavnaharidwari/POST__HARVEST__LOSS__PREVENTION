import streamlit as st
import pandas as pd
from pathlib import Path

from utils.dashboard.chart_builder import dynamic_chart_builder


# Dynamic Chart Builder Page

def chart_builder_page():


    # Load Dataset


    dataset_path = Path("dataset") / "Produce_Dataset.csv"

    try:

        df = pd.read_csv(dataset_path)

    except Exception as e:

        st.error(f"Dataset Loading Error: {e}")

        return


    # Dynamic Chart Builder


    

    dynamic_chart_builder(df)

    st.divider()

    st.caption(
        "Charts are generated dynamically from the Produce Dataset."
    )