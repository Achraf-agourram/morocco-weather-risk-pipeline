from src.extraction  import *
from src.transformation.cleaning import *
from src.transformation.validating import *
from src.transformation.features import *
from src.loading import *


db = connect_database(HOST, PORT, DATABASE, USER, PASSWORD)

store_data(load_gold_data(GOLD_FILE), db)