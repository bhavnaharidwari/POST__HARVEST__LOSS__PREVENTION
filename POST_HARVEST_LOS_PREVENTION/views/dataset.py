import streamlit as st
import pandas as pd
from pathlib import Path

from utils.dashboard.kpi import show_kpi_cards
from utils.dashboard.filters import apply_filters
from utils.dashboard.statistics import show_statistics
from utils.dashboard.correlation import correlation_dashboard
from utils.dashboard.insights import show_dataset_insights
from utils.dashboard.missing_analysis import missing_value_dashboard
from utils.dashboard.outlier import outlier_dashboard
from utils.dashboard.quick_dashboard import show_quick_dashboard


# Dataset Analytics Dashboard

def dataset_page():

    st.title("Dataset Analytics Dashboard")

    st.markdown(
        "Interactive analytics and insights for the Produce Dataset."
    )

    st.divider()


    
    # Load Dataset
    

    dataset_path = (
        Path("dataset") / "Produce_Dataset.csv"
    )

    try:

        df = pd.read_csv(dataset_path)

    except Exception as e:

        st.error(
            f"Dataset Loading Error: {e}"
        )

        return


    
    # Executive Summary
    

    st.subheader("Executive Summary")

    show_kpi_cards(df)

    st.divider()


    
    # Smart Filters
    
    filtered_df, selected_filters = apply_filters(df)

    st.divider()


    
    # Dataset Preview
    

    st.subheader("Dataset Preview")

    col1, col2 = st.columns([3, 1])


    
    # Search


    with col1:

        search = st.text_input(
            "Search Dataset"
        )



    # Number of Rows
    

    with col2:

        rows = st.selectbox(
            "Rows",
            [10, 25, 50, 100],
            index=1
        )


    
    # Apply Search
    

    if search:

        filtered_df = filtered_df[
            filtered_df
            .astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    search,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]



    # Display Dataset
    

    st.dataframe(
        filtered_df.head(rows),
        use_container_width=True,
        hide_index=True
    )

    st.divider()



    # Download Dataset


    st.subheader("Download Dataset")

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="Download Filtered Dataset (CSV)",
        data=csv,
        file_name="filtered_produce_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )