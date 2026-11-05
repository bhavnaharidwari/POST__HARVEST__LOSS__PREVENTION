import streamlit as st

from views.dashboard import dashboard_page
from views.dataset import dataset_page
from views.EDA import chart_builder_page
from views.prediction import prediction_page
from views.reports import reports_page
from views.model_performance import performance_page
from views.storage_tips import storage_tips_page
from views.about import about_page


# Page Configuration
st.set_page_config(
    page_title="Post-Harvest Loss Prevention System",
    layout="wide"
)

# Sidebar Navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Dataset",
        "EDA",
        "Prediction",
        "reports",
        "Model Performance",
        "Important Storage Tips",
        "About"
    ]
)

# Page Routing
if page == "Dashboard":
    dashboard_page()

elif page == "Dataset":
    dataset_page()

elif page == "EDA":
    chart_builder_page()

elif page == "Prediction":
    prediction_page()

elif page == "reports":
    reports_page()

elif page == "Model Performance":
    performance_page()

elif page == "Important Storage Tips":
    storage_tips_page()

elif page == "About":
    about_page()
