import pandas as pd
import numpy as np
import json, os
from dotenv import load_dotenv

load_dotenv()

BRONZE_WEATHER = os.getenv("BRONZE_WEATHER")
BRONZE_CITIES = os.getenv("BRONZE_CITIES")
SILVER_FILE = os.getenv("SILVER_FILE")


def load_weather(file=BRONZE_WEATHER):
    with open(file, "r", encoding="utf-8") as file:
        return json.load(file)

def transform_weather(data):
    rows = []

    for city in data:
        daily = city["daily"]

        df = pd.DataFrame(daily)

        df["city"] = city["city"]
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

def join_cities(df, file=BRONZE_CITIES):

    cities = pd.read_csv(file)

    return pd.merge(df, cities[["city"]], on="city", how="inner")

def save_silver_data(df, file=SILVER_FILE):
    df.to_csv(file, index=False, encoding="utf-8")


if __name__ == "__main__":
    save_silver_data(join_cities(remove_duplicates(handle_missing_values(standardize_types(transform_weather(load_weather()))))))