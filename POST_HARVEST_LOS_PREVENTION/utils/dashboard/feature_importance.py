import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from pathlib import Path


# Feature Importance Dashboard


def show_feature_importance():
    model_path = Path("models") / "spoilage_risk_pipeline.pkl"
    if not model_path.exists():
        model_path = Path("models") / "best_model.pkl"

    try:
        model = joblib.load(model_path)
    except Exception as e:
        st.error(f"Unable to load model file.\n{e}")
        return

    # Extract model and feature columns from Pipeline
    classifier = None
    if hasattr(model, "named_steps") and "classifier" in model.named_steps:
        classifier = model.named_steps["classifier"]
    elif hasattr(model, "steps"):
        classifier = model.steps[-1][1]
    else:
        classifier = model

    if classifier is None or not hasattr(classifier, "feature_importances_"):
        st.warning("Current model does not support Feature Importance.")
        return

    if hasattr(model, "feature_names_in_"):
        feature_columns = list(model.feature_names_in_)
    else:
        feature_columns = [f"Feature_{i}" for i in range(len(classifier.feature_importances_))]

    # Build DataFrame
    importance_df = pd.DataFrame({
        "Feature": feature_columns,
        "Importance": classifier.feature_importances_
    }).sort_values("Importance", ascending=False)

    st.subheader("Feature Importance")

    st.dataframe(
        importance_df,
        use_container_width=True,
        hide_index=True
    )

    # Plot
    fig = px.bar(
        importance_df.head(15),
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        text="Importance",
        title="Top 15 Most Important Features"
    )

    fig.update_layout(
        height=650,
        yaxis=dict(categoryorder="total ascending")
    )

    fig.update_traces(texttemplate="%{text:.4f}")

    st.plotly_chart(
        fig,
        use_container_width=True
    )