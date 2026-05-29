import os

import requests

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_BASE_URL = os.getenv("WEATHER_API_BASE_URL")


def fetch_weather(city_name: str) -> dict:
    if not WEATHER_API_KEY:
        raise RuntimeError("WEATHER_API_KEY is not configured")

    params = {
        "key": WEATHER_API_KEY,
        "q": city_name,
        "aqi": "no"
    }

    response = requests.get(
        WEATHER_API_BASE_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return {
        "temperature": current["temp_c"],
        "feels_like": current["feelslike_c"],
        "humidity": current["humidity"],
        "description": current["condition"]["text"],
        "wind_kph": current["wind_kph"],
        "pressure_mb": current["pressure_mb"],
        "cloud": current["cloud"],
        "uv": current["uv"],
    }
