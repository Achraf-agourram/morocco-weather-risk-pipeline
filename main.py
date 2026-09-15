from src.extraction  import *
from src.transformation.cleaning import *
from src.transformation.validating import *
from src.transformation.features import *
from src.loading import *



print(add_wind_category(add_precipitation_category(add_temperature_category(load_silver_data(SILVER_FILE)))))