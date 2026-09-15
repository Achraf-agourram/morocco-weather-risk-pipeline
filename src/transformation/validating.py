
def quality_checks(df):
    results = {
        "valid_dates": df["date"].notna().all(),
        "valid_latitudes": df["latitude"].notna().all(),
        "valid_longitudes": df["longitude"].notna().all(),
        "valid_temperatures": (df["temperature_min"] <= df["temperature_max"]).all(),
        "valid_precipitation": (df["precipitation"] >= 0).all(),
        "valid_rain_probability": ((df["rain_probability"] >= 0) & (df["rain_probability"] <= 100)).all(),
        "valid_wind_speed": (df["wind_speed_max"] >= 0).all()
    }

    return results