import pandas as pd
import numpy as np
import json, os

BRONZE_WEATHER = "data/bronze/weather.json"
BRONZE_CITIES = "data/bronze/cities.csv"
SILVER_FILE = "data/silver/clean_weather.csv"


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

def join_cities(file, df):
    if not os.path.exists(file):
        return df

    cities = pd.read_csv(file)

    df["latitude_join"] = df["latitude"].round(4)
    df["longitude_join"] = df["longitude"].round(4)

    cities["latitude_join"] = cities["lat"].round(4)
    cities["longitude_join"] = cities["lng"].round(4)

    df = pd.merge(
        df,
        cities[
            [
                "city",
                "latitude_join",
                "longitude_join"
            ]
        ],
        on=[
            "latitude_join",
            "longitude_join"
        ]
    )

    return df.drop(
        columns=[
            "latitude_join",
            "longitude_join"
        ]
    )

def save_silver_data(file, df):
    df.to_csv(file, index=False, encoding="utf-8")