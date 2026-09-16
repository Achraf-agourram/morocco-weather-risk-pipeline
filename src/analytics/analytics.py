import pandas as pd


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

def get_highest_precipitation(connection):
    query = """
        SELECT
            c.city_name,
            MAX(wf.precipitation) AS total_precipitation
        FROM cities c
        JOIN weather_forecasts wf
            ON c.city_id = wf.city_id
        GROUP BY c.city_id, c.city_name
        ORDER BY total_precipitation DESC;
    """

    return pd.read_sql_query(query, connection)

def get_highest_average_risk(connection):
    query = """
        SELECT
            c.city_name,
            ROUND(
                AVG(wr.weather_risk_score),
                2
            ) AS average_risk
        FROM cities c
        JOIN weather_forecasts wf
            ON c.city_id = wf.city_id
        JOIN weather_risks wr
            ON wf.forecast_id = wr.forecast_id
        GROUP BY c.city_id, c.city_name
        ORDER BY average_risk DESC;
    """

    return pd.read_sql_query(query, connection)

def get_highest_risk_periods(connection):
    query = """
        SELECT
            wf.forecast_date,
            ROUND(
                AVG(wr.weather_risk_score),
                2
            ) AS average_risk
        FROM weather_forecasts wf
        JOIN weather_risks wr
            ON wf.forecast_id = wr.forecast_id
        GROUP BY wf.forecast_date
        ORDER BY average_risk DESC;
    """

    return pd.read_sql_query(query, connection)

def get_highest_risk_period_per_city(connection):
    query = """
        SELECT
            city_name,
            forecast_date,
            weather_risk_score,
            risk_category
        FROM (
            SELECT
                c.city_name,
                wf.forecast_date,
                wr.weather_risk_score,
                wr.risk_category,
                ROW_NUMBER() OVER (
                    PARTITION BY c.city_id
                    ORDER BY wr.weather_risk_score DESC
                ) AS rank
            FROM cities c
            JOIN weather_forecasts wf
                ON c.city_id = wf.city_id
            JOIN weather_risks wr
                ON wf.forecast_id = wr.forecast_id
        ) ranked
        WHERE rank = 1
        ORDER BY weather_risk_score DESC;
    """

    return pd.read_sql_query(query, connection)