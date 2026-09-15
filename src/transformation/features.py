import pandas as pd


SILVER_FILE = "data/silver/clean_weather.csv"
GOLD_FILE = "data/gold/weather_features.csv"


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


