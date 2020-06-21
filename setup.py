from weather_station.collecting_data.collecting_data import CollectingData
from weather_station.wind_speed.speed_test import Speed
from datetime import datetime

CollectingData()._db_checkup()
Speed().run()
CollectingData.insert_data(datetime.now().isoformat(1, 1, 1, "N", 1))