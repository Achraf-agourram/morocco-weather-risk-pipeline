from src.extraction  import *
from src.transformation.cleaning import *
from src.transformation.validating import *
from src.loading import *


save_silver_data(SILVER_FILE, join_cities(BRONZE_CITIES, remove_duplicates(handle_missing_values(standardize_types(transform_weather(load_weather(BRONZE_WEATHER)))))))
