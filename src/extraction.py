import requests as re
import json
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

BRONZE_WEATHER = os.getenv("BRONZE_WEATHER")
BRONZE_CITIES = os.getenv("BRONZE_CITIES")
WEATHER_URL = os.getenv("WEATHER_URL")
CITIES_URL = os.getenv("CITIES_URL")

def extract_cities (url=CITIES_URL, file=BRONZE_CITIES):

    response = re.get(url)

    with open(file, "wb") as file:
        file.write(response.content)

    return True

def extract_weather (cities=pd.read_csv(BRONZE_CITIES), url=WEATHER_URL, file=BRONZE_WEATHER):

    params = {
        "latitude": ",".join(cities["latitude"].astype(str)),
        "longitude": ",".join(cities["longitude"].astype(str)),
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "weather_code"
        ],
        "forecast_days": 7,
        "timezone": "Africa/Casablanca"
    }

    response = re.get(url, params=params)
    data = response.json()

    with open(file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return True
