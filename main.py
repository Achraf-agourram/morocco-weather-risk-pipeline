from src.extraction  import *
from src.transformation import *
from src.loading import *


r = quality_checks(remove_duplicates(handle_missing_values(standardize_types(transform_weather(load_weather(BRONZE_WEATHER))))))
print(r)