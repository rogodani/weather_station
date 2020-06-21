from gpiozero import Button, MCP3008
from time import sleep
from weather_station.tools.setupparser import SetupParser
from weather_station.collecting_data.collecting_data import CollectingData
from datetime import datetime

RECORDING_INTERVAL = int(SetupParser("collecting_data").get_param()["interval"])
WIND_DIRECTION_SENSOR_BCM = 5
MCP3008_CHANNEL = 0
VOLTS = {
    0.4: [33000, 0.0, "N"],
    1.4: [6570, 22.5, "NNE"],
    1.2: [8200, 45, "NE"],
    2.8: [891, 67.5, "ENE"],
    2.7: [1000, 90, "E"],
    2.9: [688, 112.5, "ESE"],
    2.2: [2200, 135, "SE"],
    2.6: [1410, 157.5, "SSE"],
    1.8: [3900, 180, "S"],
    2.0: [3140, 202.5, "SSW"],
    0.7: [16000, 225, "SW"],
    0.8: [14120, 247.5, "WSW"],
    0.1: [120000, 270, "W"],
    0.3: [42120, 292.5, "WNW"],
    0.2: [64900, 315, "NW"],
    0.6: [21880, 337.5, "NNW"]
}
RAIN_BUCKET_SIZE = 0.2794


class SensorsData:

    def __init__(self):
        self.wind_vane_spin_count = 0
        self.wind_speed_sensor = Button(WIND_DIRECTION_SENSOR_BCM)
        self.wind_speed_sensor.when_pressed = self.count_spinning
        self.wind_direction_sensor = MCP3008(channel=MCP3008_CHANNEL)
        self.wind_direction_degrees = 0
        self.wind_direction_voltage = 0
        self.wind_direction = "N"
        self.rain_sensor = Button(6)
        self.rain_sensor.when_pressed = self.rain_bucket_tipped
        self.rain_bucket_tipped_count = 0

    def count_spinning(self):
        """Count the number of half spins"""
        self.wind_vane_spin_count += 1

    def calculate_wind_speed(self):
        return self.wind_vane_spin_count / RECORDING_INTERVAL / 2.0 * 2.4

    def find_wind_direction(self):
        wind_direction_volts = round(self.wind_direction_sensor.value * 3.3, 1)
        print(wind_direction_volts)
        if wind_direction_volts in VOLTS.keys():
            self.wind_direction_degrees = VOLTS[wind_direction_volts][1]
            self.wind_direction_voltage = wind_direction_volts
            self.wind_direction = VOLTS[wind_direction_volts][2]

    def rain_bucket_tipped(self):
        self.rain_bucket_tipped_count += 1

    def rain_qty(self):
        return round(self.rain_bucket_tipped_count * RAIN_BUCKET_SIZE, 2)

    def run(self):
        while True:
            self.wind_vane_spin_count = 0
            sleep(RECORDING_INTERVAL)
            wind_speed = self.calculate_wind_speed()
            print("{0:.2f} km/h".format(wind_speed))
            self.find_wind_direction()

            CollectingData().insert_data((datetime.now().isoformat(),wind_speed,self.wind_direction_degrees,self.wind_direction_voltage,self.wind_direction,1))
