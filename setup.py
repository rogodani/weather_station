from weather_station.collecting_data.collecting_data import CollectingData
from weather_station.sensors_data.sensors_test import SensorsData

CollectingData()._db_checkup()
SensorsData().run()