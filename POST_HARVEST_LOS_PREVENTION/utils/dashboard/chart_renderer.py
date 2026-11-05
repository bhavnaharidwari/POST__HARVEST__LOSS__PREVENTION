import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from typing import Optional

from utils.dashboard.chart_validator import AGGREGATIONS


# Chart Renderer


def render_chart(
    df: pd.DataFrame,
    chart_type: str,
    x_axis: str,
    y_axis: Optional[str] = None,
    aggregation: Optional[str] = None,
    color: Optional[str] = None,
    theme: str = "plotly",
    height: int = 550,
):
    """
    Render charts for Dynamic Chart Builder.
    """

    # Basic Dataset Validation
    

    if df is None or df.empty:
        raise ValueError(
            "No data available for chart generation."
        )

    plot_df = df.copy()

    
    # X Axis Validation
    

    if not x_axis:
        raise ValueError(
            "Please select an X Axis."
        )

    if x_axis not in plot_df.columns:
        raise ValueError(
            f"X Axis column '{x_axis}' not found."
        )

    
    # Normalize Y Axis
    

    if y_axis is not None:

        if str(y_axis).strip() == "":
            y_axis = None

    
    # Normalize Color
    

    if color is not None:

        if str(color).strip() == "":
            color = None

        elif color == "None":
            color = None

        elif color not in plot_df.columns:
            color = None

    
    # Chart Types Requiring Y Axis
    

    y_required = [
        "Bar Chart",
        "Horizontal Bar",
        "Line Chart",
        "Scatter Plot",
        "Box Plot",
        "Violin Plot",
        "Area Chart",
    ]

    if chart_type in y_required:

        if y_axis is None:
            raise ValueError(
                f"Please select a Y Axis for {chart_type}."
            )

        if y_axis not in plot_df.columns:
            raise ValueError(
                f"Y Axis column '{y_axis}' not found."
            )

    
    # Numeric Validation
    

    numeric_y_charts = [
        "Bar Chart",
        "Horizontal Bar",
        "Line Chart",
        "Scatter Plot",
        "Box Plot",
        "Violin Plot",
        "Area Chart",
    ]

    if chart_type in numeric_y_charts:

        if not pd.api.types.is_numeric_dtype(
            plot_df[y_axis]
        ):

            converted = pd.to_numeric(
                plot_df[y_axis],
                errors="coerce"
            )

            if converted.notna().sum() == 0:

                raise ValueError(
                    f"Y Axis '{y_axis}' must contain numeric data."
                )

            plot_df[y_axis] = converted

    
    # Histogram Validation
    

    if chart_type == "Histogram":

        if not pd.api.types.is_numeric_dtype(
            plot_df[x_axis]
        ):

            converted = pd.to_numeric(
                plot_df[x_axis],
                errors="coerce"
            )

            if converted.notna().sum() == 0:

                raise ValueError(
                    f"Histogram requires a numeric X Axis. "
                    f"'{x_axis}' is not numeric."
                )

            plot_df[x_axis] = converted

    
    # Scatter Validation
    

    if chart_type == "Scatter Plot":

        plot_df[x_axis] = pd.to_numeric(
            plot_df[x_axis],
            errors="coerce"
        )

        plot_df[y_axis] = pd.to_numeric(
            plot_df[y_axis],
            errors="coerce"
        )

        plot_df = plot_df.dropna(
            subset=[x_axis, y_axis]
        )

        if plot_df.empty:

            raise ValueError(
                "No valid numeric data available "
                "for the Scatter Plot."
            )

    
    # Aggregation
    

    aggregation_charts = [
        "Bar Chart",
        "Horizontal Bar",
        "Line Chart",
        "Area Chart",
    ]

    if (
        aggregation
        and y_axis is not None
        and chart_type in aggregation_charts
    ):

        if aggregation not in AGGREGATIONS:

            aggregation = "Mean"

        agg_func = AGGREGATIONS.get(
            aggregation,
            "mean"
        )

        
        # Remove invalid values before aggregation
        

        temp_df = plot_df[
            [x_axis, y_axis]
        ].copy()

        temp_df[y_axis] = pd.to_numeric(
            temp_df[y_axis],
            errors="coerce"
        )

        temp_df = temp_df.dropna(
            subset=[x_axis, y_axis]
        )

        if temp_df.empty:

            raise ValueError(
                "No valid data available after aggregation."
            )

        
        # Group and Aggregate
        

        try:

            plot_df = (
                temp_df
                .groupby(
                    x_axis,
                    as_index=False
                )[y_axis]
                .agg(agg_func)
            )

        except Exception as e:

            raise ValueError(
                f"Unable to apply {aggregation} aggregation: {e}"
            )

        # Aggregated dataframe does not contain
        # the original color column.

        color = None

    
    # PIE / DONUT Validation
    

    if chart_type in [
        "Pie Chart",
        "Donut Chart"
    ]:

        if plot_df[x_axis].dropna().empty:

            raise ValueError(
                "No valid categorical data available."
            )

    
    # Create Chart
    
    # Bar Chart
    

    if chart_type == "Bar Chart":

        fig = px.bar(
            plot_df,
            x=x_axis,
            y=y_axis,
            color=color,
            template=theme,
            text_auto=True,
            height=height,
        )

    
    # Horizontal Bar
    

    elif chart_type == "Horizontal Bar":

        fig = px.bar(
            plot_df,
            x=y_axis,
            y=x_axis,
            orientation="h",
            color=color,
            template=theme,
            text_auto=True,
            height=height,
        )

    
    # Line Chart
    

    elif chart_type == "Line Chart":

        fig = px.line(
            plot_df,
            x=x_axis,
            y=y_axis,
            color=color,
            markers=True,
            template=theme,
            height=height,
        )

    
    # Scatter Plot
    

    elif chart_type == "Scatter Plot":

        fig = px.scatter(
            plot_df,
            x=x_axis,
            y=y_axis,
            color=color,
            template=theme,
            height=height,
        )

    
    # Histogram
    

    elif chart_type == "Histogram":

        fig = px.histogram(
            plot_df,
            x=x_axis,
            color=color,
            template=theme,
            height=height,
        )

    
    # Box Plot
    

    elif chart_type == "Box Plot":

        fig = px.box(
            plot_df,
            x=x_axis,
            y=y_axis,
            color=color,
            template=theme,
            height=height,
        )

    
    # Violin Plot
    

    elif chart_type == "Violin Plot":

        fig = px.violin(
            plot_df,
            x=x_axis,
            y=y_axis,
            color=color,
            box=True,
            points="outliers",
            template=theme,
            height=height,
        )

    
    # Pie Chart
    

    elif chart_type == "Pie Chart":

        pie_df = (
            plot_df[x_axis]
            .dropna()
            .value_counts()
            .reset_index()
        )

        pie_df.columns = [
            x_axis,
            "Count"
        ]

        fig = px.pie(
            pie_df,
            names=x_axis,
            values="Count",
            template=theme,
            height=height,
        )

    
    # Donut Chart
    

    elif chart_type == "Donut Chart":

        donut_df = (
            plot_df[x_axis]
            .dropna()
            .value_counts()
            .reset_index()
        )

        donut_df.columns = [
            x_axis,
            "Count"
        ]

        fig = px.pie(
            donut_df,
            names=x_axis,
            values="Count",
            hole=0.55,
            template=theme,
            height=height,
        )

    
    # Area Chart
    

    elif chart_type == "Area Chart":

        fig = px.area(
            plot_df,
            x=x_axis,
            y=y_axis,
            color=color,
            markers=True,
            template=theme,
            height=height,
        )

    
    # Unsupported Chart
    

    else:

        raise ValueError(
            f"Unsupported chart type: {chart_type}"
        )

    
    # Layout
    

    fig.update_layout(

        title=dict(
            text=chart_type,
            x=0.5,
            font=dict(
                size=22
            ),
        ),

        template=theme,

        height=height,

        margin=dict(
            l=40,
            r=40,
            t=80,
            b=40,
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    return fig