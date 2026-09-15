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

        df = df.rename(columns={
            "time": "date",
            "temperature_2m_max": "temperature_max",
            "temperature_2m_min": "temperature_min",
            "precipitation_sum": "precipitation",
            "precipitation_probability_max": "rain_probability",
            "wind_speed_10m_max": "wind_speed_max",
            "wind_gusts_10m_max": "wind_gust_max"
        })

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


def handle_missing_values(df):
    df = df.dropna(subset=["date"])
    df = df.dropna(subset=["latitude", "longitude"])

    return df


def remove_duplicates(df):
    return df.drop_duplicates(
        subset=[
            "latitude",
            "longitude",
            "date"
        ]
    )

def quality_checks(df):
    results = {
        "valid_dates": df["date"].notna().all(),
        "valid_latitudes": df["latitude"].notna().all(),
        "valid_longitudes": df["longitude"].notna().all(),
        "valid_temperatures": (df["temperature_min"] <= df["temperature_max"]).all(),
        "valid_precipitation": (df["precipitation"] >= 0).all(),
        "valid_rain_probability": ((df["rain_probability"] >= 0) & (df["rain_probability"] <= 100)).all(),
        "valid_wind_speed": (df["wind_speed_max"] >= 0).all()
    }

    return results

