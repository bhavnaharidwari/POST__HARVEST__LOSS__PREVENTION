import streamlit as st
import pandas as pd
from pathlib import Path
from services.location_service import get_coordinates
from services.weather_service import get_weather

def prediction_form():

# Session State Initialization


    if "weather_loaded" not in st.session_state:

        st.session_state.weather_loaded = False

        st.session_state.temperature = 20.0

        st.session_state.humidity = 70.0

        st.session_state.weather = "Sunny"

        st.session_state.latitude = 23.0225

        st.session_state.longitude = 72.5714

        st.session_state.wind_speed = 0.0
    
    # Load Dataset
    

    BASE_DIR = Path(__file__).resolve().parent.parent
    dataset_path = BASE_DIR / "dataset" / "Produce_Dataset.csv"

    df = pd.read_csv(dataset_path)

    # Clean string columns
    string_columns = [
        "Category",
        "Produce_Name",
        "Variety",
        "State",
        "District"
    ]

    for col in string_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

    # Remove duplicates
    df = df.drop_duplicates()

    
    # Produce Information
    

    st.subheader(" Produce Information")

    col1, col2 = st.columns(2)

    with col1:

        category_list = sorted(df["Category"].dropna().unique())

        category = st.selectbox(
            "Category",
            category_list
        )

        produce_df = df[df["Category"] == category]

        produce_name = st.selectbox(
            "Produce Name",
            sorted(produce_df["Produce_Name"].dropna().unique())
        )

        variety_df = produce_df[
            produce_df["Produce_Name"] == produce_name
        ]

        variety = st.selectbox(
            "Variety",
            sorted(variety_df["Variety"].dropna().unique())
        )

        produce_grade = st.selectbox(
            "Produce Grade",
            ["A", "B", "C"]
        )

        quality_score = st.slider(
            "Quality Score",
            0,
            100,
            80
        )

        health_score = st.slider(
            "Health Score",
            0,
            100,
            80
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=0.1,
            max_value=500.0,
            value=10.0
        )

    with col2:

        state = st.selectbox(
            "State",
            sorted(df["State"].dropna().unique())
        )

        district_df = df[df["State"] == state]

        district = st.selectbox(
            "District",
            sorted(district_df["District"].dropna().unique())
        )

        storage_type = st.selectbox(
            "Storage Type",
            [
                "Cold Storage",
                "Warehouse",
                "Ambient Storage",
                "Controlled Atmosphere"
            ]
        )

        package_type = st.selectbox(
            "Package Type",
            [
                "Plastic Crate",
                "Carton Box",
                "Wooden Box",
                "Jute Bag"
            ]
        )

        storage_duration = st.slider(
            "Storage Duration (Days)",
            1,
            60,
            7
        )

    
    # Live Weather
    

    st.divider()
    st.subheader(" Live Weather")

    st.info(
        "Fetch current weather automatically using your selected district."
    )

    if st.button(
        "Fetch Live Weather",
        use_container_width=True
    ):

        try:

            with st.spinner("Fetching Live Weather..."):

                # Get Latitude & Longitude
                location = get_coordinates(district)

                # Get Weather
                weather = get_weather(
                    location["latitude"],
                    location["longitude"]
                )

                # Save in Session
                st.session_state.temperature = weather["temperature"]
                st.session_state.humidity = weather["humidity"]
                st.session_state.latitude = location["latitude"]
                st.session_state.longitude = location["longitude"]
                st.session_state.wind_speed = weather["wind_speed"]

                code = weather["weather_code"]

                if code <= 1:
                    st.session_state.weather = "Sunny"
                elif code <= 3:
                    st.session_state.weather = "Cloudy"
                elif code <= 67:
                    st.session_state.weather = "Rainy"
                else:
                    st.session_state.weather = "Foggy"

                st.session_state.weather_loaded = True

            st.success(" Live Weather Loaded Successfully")

        except Exception as e:

            st.error(f"Weather API Error: {e}")

    c1, c2 = st.columns(2)

    with c1:

        temperature = st.slider(
            "Temperature (°C)",
            0.0,
            50.0,
            float(st.session_state.temperature)
        )

        humidity = st.slider(
            "Humidity (%)",
            0.0,
            100.0,
            float(st.session_state.humidity)
        )

        light_intensity = st.slider(
            "Light Intensity (Lux)",
            0,
            2000,
            500
        )

        weather = st.selectbox(
            "Weather",
            [
                "Sunny",
                "Cloudy",
                "Rainy",
                "Foggy"
            ],
            index=[
                "Sunny",
                "Cloudy",
                "Rainy",
                "Foggy"
            ].index(st.session_state.weather)
        )

        season = st.selectbox(
            "Season",
            [
                "Summer",
                "Winter",
                "Monsoon",
                "Spring"
            ]
        )

    with c2:

        co2_level = st.slider(
            "CO₂ Level (ppm)",
            0,
            5000,
            400
        )

        ethylene_level = st.slider(
            "Ethylene Level (ppm)",
            0.0,
            20.0,
            1.5
        )

        moisture_content = st.slider(
            "Moisture Content (%)",
            0.0,
            50.0,
            10.0
        )

        disease_detected = st.selectbox(
            "Disease Detected",
            [
                "No",
                "Yes"
            ]
        )

        sensor_status = st.selectbox(
            "Sensor Status",
            [
                "Active",
                "Inactive",
                "Maintenance"
            ]
        )
    
    # Market & Logistics
    

    st.divider()
    st.subheader(" Market & Logistics")

    l1, l2 = st.columns(2)

    with l1:

        market_price = st.number_input(
            "Market Price",
            min_value=0.0,
            max_value=1000.0,
            value=50.0
        )

        market_demand = st.selectbox(
            "Market Demand",
            [
                "Low",
                "Medium",
                "High"
            ]
        )

        storage_cost = st.number_input(
            "Storage Cost",
            min_value=0.0,
            max_value=500.0,
            value=20.0
        )

        transport_mode = st.selectbox(
            "Transport Mode",
            [
                "Truck",
                "Rail",
                "Mini Truck",
                "Pickup"
            ]
        )

    with l2:

        distance_to_market = st.number_input(
            "Distance to Market (km)",
            min_value=0,
            max_value=5000,
            value=50
        )

        cold_chain_available = st.selectbox(
            "Cold Chain Available",
            [
                "Yes",
                "No"
            ]
        )

        sensor_battery_level = st.slider(
            "Sensor Battery (%)",
            0,
            100,
            90
        )

        iot_device_id = st.text_input(
            "IoT Device ID",
            value="IOT001"
        )

    
    # GPS Information
    

    st.divider()
    st.subheader(" GPS Location")

    g1, g2 = st.columns(2)

    with g1:
        gps_latitude = st.number_input(
            "Latitude",
            value=float(st.session_state.latitude),
            format="%.6f"
        )

    with g2:
        gps_longitude = st.number_input(
            "Longitude",
            value=float(st.session_state.longitude),
            format="%.6f"
        )

    
    # Return Form Data
    

    return {

        "Category": category,
        "Produce_Name": produce_name,
        "Variety": variety,
        "Produce_Grade": produce_grade,
        "Quality_Score": quality_score,
        "Health_Score": health_score,
        "Weight": weight,

        "State": state,
        "District": district,
        "Storage_Type": storage_type,
        "Package_Type": package_type,
        "Storage_Duration": storage_duration,

        "Temperature": temperature,
        "Humidity": humidity,
        "Light_Intensity": light_intensity,
        "CO2_Level": co2_level,
        "Ethylene_Level": ethylene_level,
        "Moisture_Content": moisture_content,
        "Weather": weather,
        "Season": season,
        "Disease_Detected": disease_detected,
        "Sensor_Status": sensor_status,

        "Market_Price": market_price,
        "Market_Demand": market_demand,
        "Storage_Cost": storage_cost,
        "Transport_Mode": transport_mode,
        "Distance_to_Market": distance_to_market,
        "Cold_Chain_Available": cold_chain_available,

        "Sensor_Battery_Level": sensor_battery_level,
        "IoT_Device_ID": iot_device_id,

        "GPS_Latitude": gps_latitude,
        "GPS_Longitude": gps_longitude
    }