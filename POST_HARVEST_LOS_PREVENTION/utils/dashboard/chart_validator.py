import pandas as pd



# Column Detection


def get_numeric_columns(df):

    ignore_columns = [
        "Record_ID"
    ]

    return [
        col for col in df.select_dtypes(include="number").columns
        if col not in ignore_columns
    ]


def get_categorical_columns(df):

    ignore_columns = [
        "Record_ID"
    ]

    return [
        col for col in df.select_dtypes(include="object").columns
        if col not in ignore_columns
    ]



# Aggregation Functions


AGGREGATIONS = {
    "Mean": "mean",
    "Sum": "sum",
    "Median": "median",
    "Maximum": "max",
    "Minimum": "min",
    "Count": "count"
}



# Chart Rules


CHART_RULES = {

    "Bar Chart": {
        "x": "categorical",
        "y": "numeric",
        "aggregation": True
    },

    "Horizontal Bar": {
        "x": "categorical",
        "y": "numeric",
        "aggregation": True
    },

    "Line Chart": {
        "x": "categorical",
        "y": "numeric",
        "aggregation": True
    },

    "Area Chart": {
        "x": "categorical",
        "y": "numeric",
        "aggregation": True
    },

    "Scatter Plot": {
        "x": "numeric",
        "y": "numeric",
        "aggregation": False
    },

    "Bubble Chart": {
        "x": "numeric",
        "y": "numeric",
        "aggregation": False
    },

    "Histogram": {
        "x": "numeric",
        "aggregation": False
    },

    "Box Plot": {
        "x": "categorical",
        "y": "numeric",
        "aggregation": False
    },

    "Violin Plot": {
        "x": "categorical",
        "y": "numeric",
        "aggregation": False
    },

    "Pie Chart": {
        "x": "categorical",
        "aggregation": False
    },

    "Donut Chart": {
        "x": "categorical",
        "aggregation": False
    },

    "Treemap": {
        "x": "categorical",
        "aggregation": False
    },

    "Sunburst": {
        "x": "categorical",
        "aggregation": False
    },

    "Correlation Heatmap": {
        "aggregation": False
    }

}