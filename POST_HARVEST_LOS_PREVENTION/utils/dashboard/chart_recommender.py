import pandas as pd
import numpy as np

# AI Smart Chart Recommendation


def recommend_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str | None = None
):
    """
    Recommend the best chart based on selected columns.
    """

    x_numeric = pd.api.types.is_numeric_dtype(df[x_column])

    y_numeric = False

    if y_column:
        y_numeric = pd.api.types.is_numeric_dtype(df[y_column])

    # Numeric vs Numeric
    if y_column and x_numeric and y_numeric:

        return {
            "chart": "Scatter Plot",
            "reason": "Both selected columns are numeric. Scatter Plot is best to identify relationships."
        }

    # Category vs Numeric
    if y_column and (not x_numeric) and y_numeric:

        unique = df[x_column].nunique()

        if unique <= 10:

            return {
                "chart": "Bar Chart",
                "reason": "Categorical vs Numeric data is best represented using Bar Chart."
            }

        return {
            "chart": "Horizontal Bar",
            "reason": "Large number of categories detected."
        }

    # Numeric only
    if x_numeric:

        return {
            "chart": "Histogram",
            "reason": "Histogram is best for understanding distribution."
        }

    # Category only

    unique = df[x_column].nunique()

    if unique <= 8:

        return {
            "chart": "Pie Chart",
            "reason": "Small number of categories detected."
        }

    return {
        "chart": "Bar Chart",
        "reason": "Bar Chart works best for categorical comparison."
    }