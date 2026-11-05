import streamlit as st
import pandas as pd

from utils.dashboard.chart_validator import (
    get_numeric_columns,
    get_categorical_columns,
    AGGREGATIONS,
)

from utils.dashboard.chart_renderer import render_chart
from utils.dashboard.chart_recommender import recommend_chart


# Dynamic Chart Builder

def dynamic_chart_builder(df: pd.DataFrame):

    st.subheader("Dynamic Exploratory Data Analysis (EDA)")

    # Validate Dataset

    if df is None or df.empty:

        st.warning("No data available for chart generation.")

        return

    # Get Columns

    numeric_columns = get_numeric_columns(df)

    categorical_columns = get_categorical_columns(df)

    all_columns = list(df.columns)

    if not all_columns:

        st.warning("No columns available in the dataset.")

        return

    # Chart Types

    chart_types = [

        "Bar Chart",
        "Horizontal Bar",
        "Line Chart",
        "Scatter Plot",
        "Histogram",
        "Box Plot",
        "Violin Plot",
        "Pie Chart",
        "Donut Chart",
        "Area Chart",

    ]

    # Chart Configuration

    st.markdown("### Chart Configuration")

    col1, col2, col3 = st.columns(3)

    # Chart Type

    with col1:

        chart_type = st.selectbox(
            "Chart Type",
            chart_types,
            key="chart_builder_type"
        )

    # X Axis

    with col2:

        if chart_type == "Histogram":

            x_options = numeric_columns

        elif chart_type in [
            "Pie Chart",
            "Donut Chart"
        ]:

            x_options = categorical_columns

        elif chart_type == "Scatter Plot":

            x_options = numeric_columns

        else:

            x_options = all_columns

        if not x_options:

            st.warning(
                "No suitable columns available for X Axis."
            )

            return

        x_axis = st.selectbox(
            "X Axis",
            x_options,
            key="chart_builder_x"
        )

    # Y Axis

    y_axis = None

    with col3:

        y_chart_types = [

            "Bar Chart",
            "Horizontal Bar",
            "Line Chart",
            "Scatter Plot",
            "Box Plot",
            "Violin Plot",
            "Area Chart",

        ]

        if chart_type in y_chart_types:

            y_options = [

                col
                for col in numeric_columns
                if col != x_axis

            ]

            if not y_options:

                st.warning(
                    "No suitable numeric column available for Y Axis."
                )

                return

            y_axis = st.selectbox(
                "Y Axis",
                y_options,
                key="chart_builder_y"
            )

        else:

            st.info(
                "Y Axis is not required for this chart."
            )

    st.divider()

    # Aggregation

    aggregation = None

    if chart_type in [

        "Bar Chart",
        "Horizontal Bar",
        "Line Chart",
        "Area Chart",

    ]:

        aggregation = st.selectbox(

            "Aggregation",

            list(AGGREGATIONS.keys()),

            key="chart_builder_aggregation"

        )

    # Color

    color_options = ["None"] + categorical_columns

    color = st.selectbox(

        "Color",

        color_options,

        key="chart_builder_color"

    )

    if color == "None":

        color = None

    st.divider()

    # Chart Recommendation

    st.markdown("### Chart Recommendation")

    try:

        recommendation = recommend_chart(

            df=df,

            x_column=x_axis,

            y_column=y_axis

        )

        if recommendation:

            recommended_chart = recommendation.get(
                "chart",
                "Not available"
            )

            reason = recommendation.get(
                "reason",
                ""
            )

            st.info(

                f"Recommended Chart: {recommended_chart}\n\n"
                f"Reason: {reason}"

            )

    except Exception as e:

        st.warning(
            f"Chart recommendation unavailable: {e}"
        )

    st.divider()

    # Chart Appearance

    col1, col2 = st.columns(2)

    with col1:

        theme = st.selectbox(

            "Theme",

            [

                "plotly",
                "plotly_white",
                "plotly_dark",
                "ggplot2",
                "presentation",
                "simple_white",

            ],

            key="chart_builder_theme"

        )

    with col2:

        height = st.slider(

            "Chart Height",

            min_value=400,

            max_value=900,

            value=550,

            step=50,

            key="chart_builder_height"

        )

    st.divider()

    # Generate Chart Button

    generate_chart = st.button(

        "Generate Selected Chart",

        use_container_width=True,

        key="generate_selected_chart"

    )

    # Generate Chart (on button click: validate, render, store in session state)

    if generate_chart:

        # Basic Validation

        if not x_axis:

            st.error(
                "Please select an X Axis."
            )

            return

        if chart_type not in [

            "Histogram",
            "Pie Chart",
            "Donut Chart"

        ] and not y_axis:

            st.error(
                "Please select a Y Axis."
            )

            return

        # Generate and persist result in session state

        with st.spinner(
            "Generating chart..."
        ):

            try:

                fig = render_chart(

                    df=df,

                    chart_type=chart_type,

                    x_axis=x_axis,

                    y_axis=y_axis,

                    aggregation=aggregation,

                    color=color,

                    theme=theme,

                    height=height,

                )

                # Store figure and status so it survives Streamlit reruns
                st.session_state["eda_chart_fig"] = fig
                st.session_state["eda_chart_success"] = True
                st.session_state["eda_chart_error"] = None

            except Exception as e:

                st.session_state["eda_chart_fig"] = None
                st.session_state["eda_chart_success"] = False
                st.session_state["eda_chart_error"] = e

    # ----------------------------------------------------------------
    # Display persisted chart (renders on every rerun, not just on the
    # button-click rerun, so the chart stays visible after any widget
    # interaction that triggers a rerun).
    # ----------------------------------------------------------------

    if st.session_state.get("eda_chart_error") is not None:

        st.error(
            "Unable to generate the selected chart."
        )

        st.exception(st.session_state["eda_chart_error"])

    elif (
        st.session_state.get("eda_chart_success")
        and st.session_state.get("eda_chart_fig") is not None
    ):

        st.success(
            "Chart generated successfully."
        )

        st.plotly_chart(

            st.session_state["eda_chart_fig"],

            use_container_width=True

        )
