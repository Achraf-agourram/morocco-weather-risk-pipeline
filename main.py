from src.extraction  import *
from src.transformation import *
from src.loading import *


d = transform_weather(load_weather(BRONZE_WEATHER))
print(d)