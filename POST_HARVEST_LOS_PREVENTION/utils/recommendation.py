def get_recommendations(data, prediction, risk_level):
    """
    Generate professional storage recommendations
    based on prediction and storage conditions.
    """

    recommendations = []

    
    # Prediction Based Recommendation
    

    if risk_level == "High":

        recommendations.append(
            "High spoilage risk detected. Immediate corrective action is recommended."
        )

    elif risk_level == "Medium":

        recommendations.append(
            "Moderate spoilage risk detected. Increase monitoring frequency."
        )

    else:

        recommendations.append(
            "Storage conditions appear satisfactory. Continue regular monitoring."
        )

    
    # Temperature
    

    temperature = data.get("Temperature", 0)

    if temperature > 30:

        recommendations.append(
            "Reduce storage temperature to slow down spoilage."
        )

    elif temperature < 2:

        recommendations.append(
            "Increase storage temperature to prevent chilling injury."
        )

    
    # Humidity
    

    humidity = data.get("Humidity", 0)

    if humidity > 90:

        recommendations.append(
            "High humidity detected. Improve ventilation to reduce fungal growth."
        )

    elif humidity < 50:

        recommendations.append(
            "Increase humidity to reduce moisture loss."
        )

    
    # Storage Duration
    

    duration = data.get("Storage_Duration", 0)

    if duration > 30:

        recommendations.append(
            "Storage duration is high. Dispatch produce as soon as possible."
        )

    
    # Storage Type
    

    storage = data.get("Storage_Type", "")

    if storage == "Ambient Storage":

        recommendations.append(
            "Cold storage is recommended for improved shelf life."
        )

    
    # Disease Detection
    

    disease = data.get("Disease_Detected", "No")

    if disease == "Yes":

        recommendations.append(
            "Separate infected produce immediately to prevent contamination."
        )

    
    # Cold Chain
    

    cold_chain = data.get("Cold_Chain_Available", "No")

    if cold_chain == "No":

        recommendations.append(
            "Use cold-chain transportation whenever available."
        )

    
    # Sensor Battery
    

    battery = data.get("Sensor_Battery_Level", 100)

    if battery < 20:

        recommendations.append(
            "Recharge or replace the IoT sensor battery."
        )

    
    # Ethylene
    

    ethylene = data.get("Ethylene_Level", 0)

    if ethylene > 10:

        recommendations.append(
            "High ethylene concentration detected. Improve air circulation."
        )

    
    # CO₂
    

    co2 = data.get("CO2_Level", 0)

    if co2 > 3000:

        recommendations.append(
            "Reduce carbon dioxide concentration inside the storage area."
        )

    
    # Moisture
    

    moisture = data.get("Moisture_Content", 0)

    if moisture > 30:

        recommendations.append(
            "High moisture detected. Improve air circulation and drying."
        )

    
    # Default Recommendation
    

    if not recommendations:

        recommendations.append(
            "No corrective action is required. Current storage conditions are acceptable."
        )

    return recommendations