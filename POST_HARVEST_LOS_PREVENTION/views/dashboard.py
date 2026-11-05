import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# Dashboard Page

def dashboard_page():

    st.title("Post-Harvest Loss Prevention System")

    st.markdown(
        """
        The Post-Harvest Loss Prevention System is an AI-powered solution
        designed to reduce spoilage and minimize food losses during
        post-harvest storage and handling.

        The system analyzes produce-related data and storage conditions such
        as temperature, humidity, environmental conditions, and other relevant
        factors to identify spoilage risk.

        Machine Learning models are used to predict the condition of stored
        produce and support better storage decisions. The system also provides
        data analytics, model performance evaluation, storage recommendations,
        prediction history, and reports.

        The system supports both the default trained model and models trained
        from user-uploaded datasets, allowing the prediction process to adapt
        to new datasets.
        """
    )

    st.divider()

    # Database Path

    db_path = (
        Path(__file__).resolve().parent.parent
        / "database"
        / "post_harvest.db"
    )

    # Current Weather 
        
    st.subheader("Current Weather")

    temperature = st.session_state.get("temperature", 20.0)
    humidity = st.session_state.get("humidity", 70)
    weather = st.session_state.get("weather", "Sunny")
    wind = st.session_state.get("wind_speed", 0)
    latitude = st.session_state.get("latitude", 0.0)
    longitude = st.session_state.get("longitude", 0.0)

    weather_col1, weather_col2, weather_col3, weather_col4 = st.columns(4)

    weather_col1.metric(
        "Temperature",
        f"{temperature} °C"
    )

    weather_col2.metric(
        "Humidity",
        f"{humidity}%"
    )

    weather_col3.metric(
        "Weather",
        weather
    )

    weather_col4.metric(
        "Wind Speed",
        f"{wind} km/h"
    )

    st.caption(
        f"Location: {latitude}, {longitude}"
    )