import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Helper Functions

def get_numeric_dataframe(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Return only numeric columns.
    """

    return df.select_dtypes(
        include=np.number
    )


def get_high_correlations(
    corr_matrix: pd.DataFrame,
    threshold: float
) -> pd.DataFrame:

    """
    Return highly correlated feature pairs.
    """

    results = []

    columns = corr_matrix.columns.tolist()

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            value = corr_matrix.iat[i, j]

            if pd.isna(value):
                continue

            corr = float(value)

            if abs(corr) >= threshold:

                results.append(
                    {
                        "Feature 1": columns[i],
                        "Feature 2": columns[j],
                        "Correlation": round(corr, 4)
                    }
                )

    if not results:

        return pd.DataFrame()

    result_df = pd.DataFrame(
        results
    )

    result_df = result_df.reindex(
        result_df["Correlation"]
        .abs()
        .sort_values(
            ascending=False
        )
        .index
    )

    result_df.reset_index(
        drop=True,
        inplace=True
    )

    return result_df



# Main Correlation Dashboard


def correlation_dashboard(
    df: pd.DataFrame
):

    st.subheader("Correlation Analysis")

    # Numeric Data

    numeric_df = get_numeric_dataframe(df)

    if numeric_df.shape[1] < 2:

        st.write(
            "At least two numeric columns are required "
            "for correlation analysis."
        )

        return

    
    # Correlation Settings
    

    left, right = st.columns([2, 1])

    with left:

        method = st.selectbox(
            "Correlation Method",
            [
                "pearson",
                "spearman",
                "kendall"
            ],
            key="corr_method"
        )

    with right:

        threshold = st.slider(
            "Correlation Threshold",
            min_value=0.00,
            max_value=1.00,
            value=0.80,
            step=0.05,
            key="corr_threshold"
        )

    
    # Correlation Matrix
    

    corr_matrix = numeric_df.corr(
        method=str(method)
    )

    # Correlation Heatmap
    st.markdown(
        "### Correlation Heatmap"
    )

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto"
    )

    fig.update_layout(
        height=650,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Highly Correlated Features

    st.markdown(
        "### Highly Correlated Features"
    )

    high_corr = get_high_correlations(
        corr_matrix,
        threshold
    )

    if high_corr.empty:

        st.write(
            "No highly correlated feature pairs found."
        )

    else:

        st.dataframe(
            high_corr,
            hide_index=True,
            use_container_width=True
        )    
    # Correlation Matrix

    st.markdown(
        "### Correlation Matrix"
    )

    st.dataframe(
        corr_matrix.round(3),
        use_container_width=True,
        hide_index=True
    )
    # Download Correlation Matrix
    csv = (
        corr_matrix
        .round(4)
        .to_csv(index=True)
        .encode("utf-8")
    )

    st.download_button(
        label="Download Correlation Matrix",
        data=csv,
        file_name="correlation_matrix.csv",
        mime="text/csv",
        use_container_width=True
    )