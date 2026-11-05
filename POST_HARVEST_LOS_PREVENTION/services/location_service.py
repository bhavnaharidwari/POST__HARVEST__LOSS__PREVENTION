import requests


def get_coordinates(city):

    url = (
        "https://nominatim.openstreetmap.org/search"
        f"?q={city}"
        "&format=json"
        "&limit=1"
    )

    headers = {
        "User-Agent": "PostHarvestSystem/1.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    if response.status_code != 200:
        raise Exception("Location API Error")

    data = response.json()

    if len(data) == 0:
        raise Exception("City not found")

    return {

        "latitude": float(data[0]["lat"]),

        "longitude": float(data[0]["lon"]),

        "display_name": data[0]["display_name"]

    }
if __name__ == "__main__":

    location = get_coordinates("Ahmedabad")

    print(location)