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


def standardize_types(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    numeric_columns = [
        "latitude",
        "longitude",
        "elevation",
        "temperature_max",
        "temperature_min",
        "precipitation",
        "rain_probability",
        "wind_speed_max",
        "wind_gust_max",
        "weather_code"
    ]

    for column in numeric_columns: df[column] = pd.to_numeric(df[column], errors="coerce")

    return df

