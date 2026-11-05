import requests


def get_weather(latitude, longitude):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise Exception("Unable to fetch weather data.")

    data = response.json()

    current = data["current"]

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "weather_code": current["weather_code"],
    }
if __name__ == "__main__":

    weather = get_weather(
        latitude=28.6139,
        longitude=77.2090
    )

    print(weather)