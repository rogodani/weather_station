from weather_station.collecting_data.collecting_data import CollectingData
from weather_station.wind_speed.speed_test import Speed
from datetime import datetime
from time import sleep

CollectingData()._db_checkup()
# Speed().run()

while True:
    Speed.half_spin_count = 0
    sleep(5)
    print("{0:.2f} km/h".format(Speed.calculate_wind_speed()))

CollectingData.insert_data(datetime.now().isoformat(1, 1, 1, "N", 1))