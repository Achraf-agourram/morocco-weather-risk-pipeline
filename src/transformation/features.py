import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

SILVER_FILE = os.getenv("SILVER_FILE")
GOLD_FILE = os.getenv("GOLD_FILE")


def load_silver_data(file):
    return pd.read_csv(file)

def add_temperature_category(df):

    df["temperature_category"] = pd.cut(
        df["temperature_max"],
        bins=[-float("inf"), 5, 15, 25, 35, float("inf")],
        labels=["very_cold", "cold", "mild", "warm", "hot"],
        right=False
    )

    return df

def add_precipitation_category(df):
    
    df["precipitation_category"] = pd.cut(
        df["precipitation"],
        bins=[-float("inf"), 0, 2.5, 10, float("inf")],
        labels=["none", "light", "moderate", "heavy"],
        right=False,
        include_lowest=True
    )

    return df

def add_wind_category(df):

    df["wind_category"] = pd.cut(
        df["wind_speed_max"],
        bins=[-float("inf"), 20, 40, 60, float("inf")],
        labels=["low", "moderate", "strong", "very_strong"],
        right=False,
        include_lowest=True
    )

    return df

def add_date_features(df):
    df["date"] = pd.to_datetime(df["date"])

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.day_name()

    return df

def calculate_rain_risk(precipitation):
    if precipitation == 0:
        return 0

    if precipitation < 2.5:
        return 25

    if precipitation < 10:
        return 60

    return 100

def calculate_wind_risk(wind_speed):
    if wind_speed < 20:
        return 0

    if wind_speed < 40:
        return 30

    if wind_speed < 60:
        return 70

    return 100

def calculate_temperature_risk(temperature):
    if 15 <= temperature <= 25:
        return 0

    if 10 <= temperature < 15 or 25 < temperature <= 30:
        return 25

    if 5 <= temperature < 10 or 30 < temperature <= 35:
        return 60

    return 100

def calculate_rain_probability_risk(probability):
    if probability < 20:
        return 0

    if probability < 50:
        return 30

    if probability < 80:
        return 60

    return 100

def add_risk_score(df):

    df["rain_risk"] = df["precipitation"].apply(calculate_rain_risk)
    df["wind_risk"] = df["wind_speed_max"].apply(calculate_wind_risk)
    df["temperature_risk"] = df["temperature_max"].apply(calculate_temperature_risk)
    df["rain_probability_risk"] = df["rain_probability"].apply(calculate_rain_probability_risk)

    df["weather_risk_score"] = (
        df["rain_risk"] * 0.35
        + df["wind_risk"] * 0.35
        + df["temperature_risk"] * 0.15
        + df["rain_probability_risk"] * 0.15
    )

    df["weather_risk_score"] = df["weather_risk_score"].round(2)

    return df

def add_risk_category(df):
    df["risk_category"] = pd.cut(
        df["weather_risk_score"],
        bins=[-float("inf"), 25, 50, 75, float("inf")],
        labels=["low", "moderate", "high", "very_high"],
        include_lowest=True,
        right=False
    )

    return df

def save_gold_data(file, df):
    df.to_csv(file, index=False)