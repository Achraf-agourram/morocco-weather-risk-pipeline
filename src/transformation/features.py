import pandas as pd


SILVER_FILE = "data/silver/clean_weather.csv"
GOLD_FILE = "data/gold/weather_features.csv"


def load_silver_data(file):
    return pd.read_csv(file)