import streamlit as st
import pandas as pd
import plotly.express as px


# Missing Value Dashboard

def missing_value_dashboard(df: pd.DataFrame):

    st.subheader("Missing Value Analysis")

    total_rows = len(df)
    total_columns = len(df.columns)

    total_cells = total_rows * total_columns
    missing_cells = int(df.isna().sum().sum())

    quality_score = (
        ((total_cells - missing_cells) / total_cells) * 100
        if total_cells > 0 else 100
    )

    columns_with_missing = int((df.isna().sum() > 0).sum())

    
    # KPI Cards
    

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Data Quality",
        f"{quality_score:.2f}%"
    )

    c2.metric(
        "Missing Cells",
        missing_cells
    )

    c3.metric(
        "Columns With Missing",
        columns_with_missing
    )

    c4.metric(
        "Dataset Size",
        f"{total_rows} × {total_columns}"
    )

    st.divider()

    
    # Missing Summary
    

    missing_df = pd.DataFrame({

        "Column": df.columns,

        "Missing Values": df.isna().sum().values,

        "Missing Percentage": (
            df.isna().mean() * 100
        ).round(2).values

    })

    missing_df = missing_df.sort_values(

        by="Missing Percentage",

        ascending=False

    )

    missing_df = missing_df[
        missing_df["Missing Values"] > 0
    ]

    if missing_df.empty:

        st.text("No missing values found in the dataset.")

        return

    st.markdown("### Missing Value Summary")

    st.dataframe(
        missing_df,
        hide_index=True,
        use_container_width=True
    )

    st.divider()


    # Charts
    

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(

            missing_df,

            x="Column",

            y="Missing Percentage",

            text="Missing Percentage",

            template="plotly_white",

            title="Missing Percentage by Column"

        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.pie(

            missing_df,

            names="Column",

            values="Missing Values",

            hole=0.55,

            title="Missing Value Distribution"

        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # Download Report


    csv = missing_df.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="Download Missing Value Report",

        data=csv,

        file_name="missing_value_report.csv",

        mime="text/csv",

        use_container_width=True,

        key="missing_report_download"

    ) 