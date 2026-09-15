import pandas as pd
import numpy as np
import json, os

BRONZE_WEATHER = "src/bronze/weather.json"
BRONZE_CITIES = "src/bronze/cities.csv"
SILVER_FILE = "src/silver/clean_weather.csv"


def load_weather(file):
    with open(file, "r", encoding="utf-8") as file:
        return json.load(file)


def transform_weather(data):
    rows = []

    for city in data:
        daily = city["daily"]

        df = pd.DataFrame(daily)

        df["latitude"] = city["latitude"]
        df["longitude"] = city["longitude"]
        df["timezone"] = city["timezone"]
        df["elevation"] = city["elevation"]

        rows.append(df)

    return pd.concat(rows, ignore_index=True)

