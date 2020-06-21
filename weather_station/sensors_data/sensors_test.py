from gpiozero import Button, MCP3008
from time import sleep
from weather_station.tools.setupparser import SetupParser
from weather_station.collecting_data.collecting_data import CollectingData
from datetime import datetime

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


class SensorsData:

    def __init__(self):
        self.RECORDING_INTERVAL = int(SetupParser("collecting_data").get_param()["interval"])
        self.half_spin_count = 0
        self.WIND_SPEED_SENSOR = Button(5)
        self.WIND_SPEED_SENSOR.when_pressed = self.count_spinning
        self.ADC = MCP3008(channel=0)
        self.wind_direction_degrees = 0
        self.wind_direction_voltage = 0
        self.wind_direction = "N"

    def count_spinning(self):
        """Count the number of half spins"""
        self.half_spin_count += 1

    def calculate_wind_speed(self):
        return self.half_spin_count / self.RECORDING_INTERVAL / 2.0 * 2.4

    def find_wind_direction(self):
        wind_direction_volts = round(self.ADC.value * 3.3, 1)
        print(wind_direction_volts)
        if wind_direction_volts in VOLTS.keys():
            self.wind_direction_degrees = VOLTS[wind_direction_volts][1]
            self.wind_direction_voltage = wind_direction_volts
            self.wind_direction = VOLTS[wind_direction_volts][2]

    def run(self):
        while True:
            self.half_spin_count = 0
            sleep(self.RECORDING_INTERVAL)
            wind_speed = self.calculate_wind_speed()
            print("{0:.2f} km/h".format(wind_speed))
            self.find_wind_direction()
            CollectingData().insert_data((datetime.now().isoformat(),wind_speed,self.wind_direction_degrees,self.wind_direction_voltage,self.wind_direction,1))
