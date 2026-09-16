import pandas as pd
import psycopg2


def get_highest_temperatures(connection):
    query = """
        SELECT
            c.city_name,
            MAX(wf.temperature_max) AS highest_temperature
        FROM cities c
        JOIN weather_forecasts wf
            ON c.city_id = wf.city_id
        GROUP BY c.city_id, c.city_name
        ORDER BY highest_temperature DESC
        FETCH FIRST 1 ROWS WITH TIES;
    """

    return pd.read_sql_query(query, connection)