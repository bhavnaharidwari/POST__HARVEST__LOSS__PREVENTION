"""
AI Post Harvest Loss Prevention System
Dataset Generator using Faker
"""
from faker import Faker
import pandas as pd
import random
from datetime import timedelta

# Faker Object
fake = Faker("en_IN")

# Number of Records
NUM_ROWS = 100000

print("Modules Loaded Successfully")


# Categories


produce_data = {
    
    "Fruit": {

        "Apple": [
            "Red Delicious",
            "Fuji", 
            "Gala",
            "Granny Smith"
        ],

        "Banana": [
            "Cavendish",
            "Robusta",
            "Dwarf"
        ],

        "Mango": [
            "Alphonso",
            "Kesar",
            "Dasheri",
            "Langra"
        ],

        "Orange": [
            "Nagpur",
            "Valencia",
            "Blood Orange"
        ],

        "Grapes": [
            "Green",
            "Black",
            "Red"
        ],

        "Pomegranate": [
            "Bhagwa",
            "Ganesh"
        ],

        "Guava": [
            "Allahabad",
            "Lucknow-49"
        ],

        "Papaya": [
            "Red Lady",
            "Pusa"
        ]
    },

    "Vegetable": {

        "Tomato": [
            "Roma",
            "Cherry",
            "Hybrid"
        ],

        "Potato": [
            "Kufri",
            "Jyoti",
            "Lalima"
        ],

        "Onion": [
            "Red",
            "White",
            "Yellow"
        ],

        "Carrot": [
            "Nantes",
            "Imperator"
        ],

        "Cabbage": [
            "Green",
            "Purple"
        ],

        "Cauliflower": [
            "Snowball",
            "Pusa"
        ],

        "Capsicum": [
            "Green",
            "Yellow",
            "Red"
        ],

        "Brinjal": [
            "Purple",
            "Long Green"
        ]
    }
}



states = [
    "Gujarat",
    "Maharashtra",
    "Punjab",
    "Rajasthan",
    "Karnataka",
    "Tamil Nadu",
    "Uttar Pradesh",
    "Madhya Pradesh"
]

storage_types = [
    "Cold Storage",
    "Ambient Storage",
    "Controlled Atmosphere",
    "Warehouse"
]

package_types = [
    "Plastic Crate",
    "Wooden Box",
    "Carton Box",
    "Jute Bag"
]

weather_conditions = [
    "Sunny",
    "Rainy",
    "Cloudy",
    "Foggy"
]
# --------------------------------------------------
# Additional Master Data
# --------------------------------------------------

produce_grades = [
    "A",
    "B",
    "C"
]

transport_modes = [
    "Truck",
    "Mini Truck",
    "Rail",
    "Container",
    "Pickup Van"
]

market_demand = [
    "Low",
    "Medium",
    "High"
]

cold_chain = [
    "Yes",
    "No"
]

sensor_status = [
    "Active",
    "Inactive",
    "Maintenance"
]

districts = {

    "Gujarat": [
        "Ahmedabad",
        "Surat",
        "Vadodara",
        "Rajkot"
    ],

    "Maharashtra": [
        "Mumbai",
        "Pune",
        "Nagpur",
        "Nashik"
    ],

    "Punjab": [
        "Ludhiana",
        "Amritsar",
        "Patiala"
    ],

    "Rajasthan": [
        "Jaipur",
        "Jodhpur",
        "Kota"
    ],

    "Karnataka": [
        "Bengaluru",
        "Mysuru",
        "Hubli"
    ],

    "Tamil Nadu": [
        "Chennai",
        "Coimbatore",
        "Madurai"
    ],

    "Uttar Pradesh": [
        "Lucknow",
        "Kanpur",
        "Agra"
    ],

    "Madhya Pradesh": [
        "Bhopal",
        "Indore",
        "Gwalior"
    ]
}

seasons = [
    "Summer",
    "Winter",
    "Monsoon",
    "Spring"
]
# --------------------------------------------------
# Ideal Storage Conditions
# --------------------------------------------------

ideal_storage = {

    "Apple": {
        "temp": (0, 4),
        "humidity": (90, 95)
    },

    "Banana": {
        "temp": (13, 15),
        "humidity": (85, 90)
    },

    "Mango": {
        "temp": (10, 13),
        "humidity": (85, 90)
    },

    "Orange": {
        "temp": (3, 8),
        "humidity": (85, 90)
    },

    "Grapes": {
        "temp": (0, 2),
        "humidity": (90, 95)
    },

    "Pomegranate": {
        "temp": (5, 8),
        "humidity": (90, 95)
    },

    "Guava": {
        "temp": (8, 10),
        "humidity": (85, 90)
    },

    "Papaya": {
        "temp": (10, 13),
        "humidity": (85, 90)
    },

    "Tomato": {
        "temp": (10, 15),
        "humidity": (85, 90)
    },

    "Potato": {
        "temp": (4, 8),
        "humidity": (90, 95)
    },

    "Onion": {
        "temp": (0, 4),
        "humidity": (65, 75)
    },

    "Carrot": {
        "temp": (0, 2),
        "humidity": (95, 98)
    },

    "Cabbage": {
        "temp": (0, 2),
        "humidity": (95, 98)
    },

    "Cauliflower": {
        "temp": (0, 2),
        "humidity": (95, 98)
    },

    "Capsicum": {
        "temp": (7, 10),
        "humidity": (90, 95)
    },

    "Brinjal": {
        "temp": (10, 12),
        "humidity": (90, 95)
    }
}


# Generate Produce Details


def generate_produce():

    category = random.choice(list(produce_data.keys()))

    produce = random.choice(list(produce_data[category].keys()))

    variety = random.choice(produce_data[category][produce])

    return category, produce, variety



# Generate Environmental Conditions


# Generate Environment (Produce Specific)


def generate_environment(produce_name):

    # Ideal Range
    temp_range = ideal_storage[produce_name]["temp"]
    humidity_range = ideal_storage[produce_name]["humidity"]

    # 80% records ideal storage
    if random.random() < 0.80:

        temperature = round(
            random.uniform(temp_range[0], temp_range[1]),
            1
        )

        humidity = round(
            random.uniform(humidity_range[0], humidity_range[1]),
            1
        )

    # 20% records poor storage
    else:

        temperature = round(
            random.uniform(
                temp_range[1] + 3,
                temp_range[1] + 12
            ),
            1
        )

        humidity = round(
            random.uniform(
                max(40, humidity_range[0] - 25),
                min(98, humidity_range[1] + 10)
            ),
            1
        )

    light = round(random.uniform(100, 900), 1)

    co2 = round(random.uniform(250, 1500), 1)

    ethylene = round(random.uniform(0, 10), 2)

    moisture = round(random.uniform(5, 35), 1)

    return (
        temperature,
        humidity,
        light,
        co2,
        ethylene,
        moisture
    )

# Weather Adjustment


def apply_weather_effect(
    temperature,
    humidity,
    weather,
    storage_type
):

    # Cold storage is less affected
    if storage_type == "Cold Storage":
        return (
            round(temperature, 1),
            round(humidity, 1)
        )

    # Ambient storage adjustments
    if weather == "Sunny":
        temperature += random.uniform(2, 5)

    elif weather == "Rainy":
        humidity += random.uniform(5, 10)

    elif weather == "Foggy":
        humidity += random.uniform(3, 6)

    elif weather == "Cloudy":
        temperature += random.uniform(0, 2)

    # Keep values within limits
    temperature = max(0, min(45, temperature))
    humidity = max(40, min(98, humidity))

    return (
        round(temperature, 1),
        round(humidity, 1)
    )


# Generate Storage Information


def generate_storage():
    

    storage_type = random.choice(storage_types)

    package = random.choice(package_types)

    duration = random.randint(1, 45)

    season = random.choice(seasons)

    weather = random.choice(weather_conditions)

    return (
        storage_type,
        package,
        duration,
        season,
        weather
    )
def generate_additional_data():

    grade = random.choices(
        produce_grades,
        weights=[50, 35, 15]
    )[0]
    

    quality_score = random.randint(60, 100)

    market_price = round(
        random.uniform(10, 300),
        2
    )

    transport = random.choice(
        transport_modes
    )

    distance = random.randint(
        5,
        600
    )

    cold = random.choice(
        cold_chain
    )

    battery = random.randint(
        40,
        100
    )

    device_id = f"IOT-{random.randint(1000,9999)}"

    latitude = round(
        random.uniform(8.0, 37.0),
        6
    )

    longitude = round(
        random.uniform(68.0, 97.0),
        6
    )

    demand = random.choice(
        market_demand
    )

    storage_cost = round(
        random.uniform(20, 500),
        2
    )

    return (
        grade,
        quality_score,
        market_price,
        transport,
        distance,
        cold,
        battery,
        device_id,
        latitude,
        longitude,
        demand,
        storage_cost
    )


# --------------------------------------------------
# AI Rule Engine
# --------------------------------------------------
# --------------------------------------------------
# Health Score Calculation
# --------------------------------------------------

def calculate_health_score(
    temperature,
    humidity,
    co2,
    ethylene,
    storage_duration,
    quality_score,
    storage_type,
    produce_name
):

    score = quality_score

    # Ideal values for selected produce
    temp_min, temp_max = ideal_storage[produce_name]["temp"]
    hum_min, hum_max = ideal_storage[produce_name]["humidity"]

    # Temperature penalty
    if temperature < temp_min or temperature > temp_max:
        score -= 15

    # Humidity penalty
    if humidity < hum_min or humidity > hum_max:
        score -= 10

    # CO2 penalty
    if co2 > 1000:
        score -= 10

    # Ethylene penalty
    if ethylene > 6:
        score -= 15
    elif ethylene > 3:
        score -= 8

    # Storage duration penalty
    if storage_duration > 30:
        score -= 15
    elif storage_duration > 15:
        score -= 8

    # Cold storage bonus
    if storage_type == "Cold Storage":
        score += 5

    score = max(0, min(100, score))

    return round(score, 1)

def calculate_spoilage(
    temperature,
    humidity,
    co2,
    ethylene,
    storage_duration,
    storage_type
):
    """
    Calculate spoilage risk, shelf life, recommendation,
    and alert status using rule-based logic.
    """

    score = 0

    # Temperature
    if temperature > 30:
        score += 3
    elif temperature > 20:
        score += 2
    else:
        score += 1

    # Humidity
    if humidity > 90:
        score += 3
    elif humidity > 75:
        score += 2
    else:
        score += 1

    # CO2
    if co2 > 1000:
        score += 2

    # Ethylene
    if ethylene > 6:
        score += 3
    elif ethylene > 3:
        score += 2

    # Storage Duration
    if storage_duration > 30:
        score += 3
    elif storage_duration > 15:
        score += 2

    # Cold Storage Bonus
    if storage_type == "Cold Storage":
        score -= 2

    score = max(score, 0)

    # Final Decision
    if score >= 10:
        spoilage = "High"
        shelf_life = random.randint(1, 5)
        recommendation = "Immediate sale or processing required."
        alert = "Critical"

    elif score >= 6:
        spoilage = "Medium"
        shelf_life = random.randint(6, 12)
        recommendation = "Improve storage conditions."
        alert = "Warning"

    else:
        spoilage = "Low"
        shelf_life = random.randint(13, 30)
        recommendation = "Storage conditions are optimal."
        alert = "Normal"

    return (
        spoilage,
        shelf_life,
        recommendation,
        alert
    )

# Generate Dataset

records = []

for i in range(1, NUM_ROWS + 1):

    category, produce, variety = generate_produce()

    (
        temperature,
        humidity,
        light,
        co2,
        ethylene,
        moisture
    )  = generate_environment(produce)


    (
        storage_type,
        package,
        duration,
        season,
        weather
    ) = generate_storage()

    temperature, humidity = apply_weather_effect(
    temperature,
    humidity,
    weather,
    storage_type
    )
    spoilage, shelf_life, recommendation, alert = calculate_spoilage(
        temperature,
        humidity,
        co2,
        ethylene,
        duration,
        storage_type
    )

    harvest_date = fake.date_between(
        start_date="-90d",
        end_date="-10d"
    )

    storage_date = harvest_date + timedelta(
        days=random.randint(0, 5)
    )

    (
    grade,
    quality_score,
    market_price,
    transport,
    distance,
    cold,
    battery,
    device_id,
    latitude,
    longitude,
    demand,
    storage_cost
    ) = generate_additional_data()
    
    health_score = calculate_health_score(
    temperature,
    humidity,
    co2,
    ethylene,
    duration,
    quality_score,
    storage_type,
    produce
    )
    state = random.choice(states)
    district = random.choice(districts[state])

    record = {

        "Record_ID": i,

        "Category": category,

        "Produce_Name": produce,

        "Variety": variety,

        "Produce_Grade": grade,

        "Quality_Score": quality_score,

        "Health_Score": health_score,

        "Market_Price": market_price,

        "Transport_Mode": transport,

        "Distance_to_Market": distance,

        "Cold_Chain_Available": cold,

        "IoT_Device_ID": device_id,

        "Sensor_Battery_Level": battery,

        "GPS_Latitude": latitude,
 
        "GPS_Longitude": longitude,
 
        "Market_Demand": demand,

        "Storage_Cost": storage_cost,

        "Farmer_ID": f"F{random.randint(1000,9999)}",

        "Warehouse_ID": f"W{random.randint(100,999)}",

        "State": state,

        "District": district,
        
        "Storage_Type": storage_type,

        "Package_Type": package,

        "Harvest_Date": harvest_date,

        "Storage_Date": storage_date,

        "Storage_Duration": duration,

        "Temperature": temperature,

        "Humidity": humidity,

        "Light_Intensity": light,

        "CO2_Level": co2,

        "Ethylene_Level": ethylene,

        "Moisture_Content": moisture,

        "Weight": round(random.uniform(1,50),2),

        "Weather": weather,

        "Season": season,

        "Shelf_Life": shelf_life,

        "Disease_Detected": random.choice(["Yes","No"]),

        "Sensor_Status": random.choice(sensor_status),
        
        "Spoilage_Risk": spoilage,

        "Recommendation": recommendation,

        "Alert_Status": alert,

        "Timestamp": fake.date_time_this_year()
        

    }

    records.append(record)

print(f"Generated {len(records)} records...")


# Convert to DataFrame
df = pd.DataFrame(records)

print(df.head())


# Save Dataset


df.to_csv(
    "dataset/Produce_Dataset.csv",
    index=False
)

print("\nDataset Saved Successfully!")

print("Shape :", df.shape)
