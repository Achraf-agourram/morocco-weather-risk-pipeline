import pandas as pd
import psycopg2


GOLD_FILE = "data/gold/weather_features.csv"
HOST = "localhost"
PORT = "5432"
DATABASE = "weather_pipeline"
USER = "postgres"
PASSWORD = "admin"


def load_gold_data(file):
    return pd.read_csv(file)

def connect_database(host, port, database, user, password):
    return psycopg2.connect(host=host, port=port, database=database, user=user, password=password)

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