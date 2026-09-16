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

