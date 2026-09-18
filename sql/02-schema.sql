CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    latitude NUMERIC(9,6) NOT NULL,
    longitude NUMERIC(9,6) NOT NULL,

    CONSTRAINT unique_city_coordinates
        UNIQUE (latitude, longitude)
);


CREATE TABLE weather_forecasts (
    forecast_id SERIAL PRIMARY KEY,

    city_id INTEGER NOT NULL,

    forecast_date DATE NOT NULL,

    temperature_max NUMERIC(5,2),
    temperature_min NUMERIC(5,2),

    precipitation NUMERIC(6,2),
    rain_probability NUMERIC(5,2),

    wind_speed_max NUMERIC(6,2),
    wind_gust_max NUMERIC(6,2),

    weather_code INTEGER,

    CONSTRAINT fk_weather_city
        FOREIGN KEY (city_id)
        REFERENCES cities(city_id),

    CONSTRAINT unique_city_forecast
        UNIQUE (city_id, forecast_date)
);


CREATE TABLE weather_risks (
    risk_id SERIAL PRIMARY KEY,

    forecast_id INTEGER NOT NULL,

    rain_risk NUMERIC(5,2),
    wind_risk NUMERIC(5,2),
    temperature_risk NUMERIC(5,2),
    rain_probability_risk NUMERIC(5,2),

    weather_risk_score NUMERIC(5,2) NOT NULL,

    risk_category VARCHAR(20) NOT NULL,

    CONSTRAINT fk_risk_forecast
        FOREIGN KEY (forecast_id)
        REFERENCES weather_forecasts(forecast_id)
        ON DELETE CASCADE,

    CONSTRAINT unique_forecast_risk
        UNIQUE (forecast_id)
);