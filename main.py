from src.extraction  import *
from src.transformation.cleaning import *
from src.transformation.validating import *
from src.transformation.features import *
from src.loading import *


# save_gold_data(GOLD_FILE, add_risk_category(add_risk_score(add_date_features(add_wind_category(add_precipitation_category(add_temperature_category(load_silver_data(SILVER_FILE))))))))

db = connect_database(HOST, PORT, DATABASE, USER, PASSWORD)

store_data(load_gold_data(GOLD_FILE), db)