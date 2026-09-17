import psycopg2, os, streamlit
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

def connect_database(host, port, database, user, password):
    return psycopg2.connect(host=host, port=port, database=database, user=user, password=password)

@streamlit.cache_data(ttl=3600)
def load_data(_connection):
    query = """
        SELECT
            c.city_name,
            c.latitude,
            c.longitude,
            wf.forecast_date,
            wf.temperature_max,
            wf.temperature_min,
            wf.precipitation,
            wf.rain_probability,
            wf.wind_speed_max,
            wf.wind_gust_max,
            wr.weather_risk_score,
            wr.risk_category
        FROM cities c
        JOIN weather_forecasts wf
            ON c.city_id = wf.city_id
        JOIN weather_risks wr
            ON wf.forecast_id = wr.forecast_id
        ORDER BY wf.forecast_date;
    """

    return pd.read_sql_query(query, _connection)