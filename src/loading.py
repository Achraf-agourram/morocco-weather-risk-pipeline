import pandas as pd
from dotenv import load_dotenv
import os
from database import connect_database

load_dotenv()

GOLD_FILE = os.getenv("GOLD_FILE")

def load_gold_data(file=GOLD_FILE):
    return pd.read_csv(file)

def get_or_create_city(db, city_name, latitude, longitude):
    query = """
        INSERT INTO cities (
            city_name,
            latitude,
            longitude
        )
        VALUES (%s, %s, %s)
        ON CONFLICT (latitude, longitude)
        DO UPDATE SET
            city_name = EXCLUDED.city_name
        RETURNING city_id;
    """

    db.execute(query,(city_name, latitude, longitude))

    return db.fetchone()[0]

def upsert_forecast(db, city_id, row):
    query = """
        INSERT INTO weather_forecasts (
            city_id,
            forecast_date,
            temperature_max,
            temperature_min,
            precipitation,
            rain_probability,
            wind_speed_max,
            wind_gust_max,
            weather_code
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        ON CONFLICT (
            city_id,
            forecast_date
        )
        DO UPDATE SET
            temperature_max = EXCLUDED.temperature_max,
            temperature_min = EXCLUDED.temperature_min,
            precipitation = EXCLUDED.precipitation,
            rain_probability = EXCLUDED.rain_probability,
            wind_speed_max = EXCLUDED.wind_speed_max,
            wind_gust_max = EXCLUDED.wind_gust_max,
            weather_code = EXCLUDED.weather_code
        RETURNING forecast_id;
    """

    db.execute(query,
        (
            city_id,
            row["date"],
            row["temperature_max"],
            row["temperature_min"],
            row["precipitation"],
            row["rain_probability"],
            row["wind_speed_max"],
            row["wind_gust_max"],
            row["weather_code"]
        )
    )

    return db.fetchone()[0]

def upsert_weather_risk(db, forecast_id, row):
    query = """
        INSERT INTO weather_risks (
            forecast_id,
            rain_risk,
            wind_risk,
            temperature_risk,
            rain_probability_risk,
            weather_risk_score,
            risk_category
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (
            forecast_id
        )
        DO UPDATE SET
            rain_risk = EXCLUDED.rain_risk,
            wind_risk = EXCLUDED.wind_risk,
            temperature_risk = EXCLUDED.temperature_risk,
            rain_probability_risk = EXCLUDED.rain_probability_risk,
            weather_risk_score = EXCLUDED.weather_risk_score,
            risk_category = EXCLUDED.risk_category
        RETURNING risk_id;
    """

    db.execute(query,
        (
            forecast_id,
            row["rain_risk"],
            row["wind_risk"],
            row["temperature_risk"],
            row["rain_probability_risk"],
            row["weather_risk_score"],
            row["risk_category"]
        )
    )

    return db.fetchone()[0]

def store_data(df, connection=None):
    
    if connection is None:
        connection = connect_database()

    db = connection.cursor()

    for i, row in df.iterrows():

        city_id = get_or_create_city(db, row["city"], row["latitude"], row["longitude"])
        forecast_id = upsert_forecast(db, city_id, row)
        risk_id = upsert_weather_risk(db, forecast_id, row)

    connection.commit()
    connection.close()

    return True

if __name__ == "__main__":
    store_data(load_gold_data())