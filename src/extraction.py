def extract_cities ():
    return True

def extract_weather ():
    return True












# url = "https://api.open-meteo.com/v1/forecast"

# params = {
#     "latitude": 32.2833,
#     "longitude": -9.2333,
#     "daily": [
#         "temperature_2m_max",
#         "temperature_2m_min",
#         "precipitation_sum",
#         "precipitation_probability_max",
#         "wind_speed_10m_max",
#         "wind_gusts_10m_max",
#         "weather_code"
#     ],
#     "forecast_days": 7,
#     "timezone": "Africa/Casablanca"
# }

# response = re.get(url, params=params, timeout=10)

# data = response.json()

# with open("src/bronze/weather.json", "w", encoding="utf-8") as file:
#     json.dump(data, file, indent=4, ensure_ascii=False)