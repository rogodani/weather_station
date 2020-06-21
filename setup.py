from weather_station.collecting_data.collecting_data import CollectingData
from weather_station.wind_speed.speed_test import Speed

CollectingData()._db_checkup()
Speed().run()
