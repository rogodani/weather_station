from gpiozero import Button
from time import sleep
from tools.setupparser import SetupParser


class Speed:

    def __init__(self):
        self.recording_interval = SetupParser("collecting_data").get_param()["interval"]
        self.half_spin_count = 0
        self.wind_speed_sensor = Button(5)
        self.wind_speed_sensor.when_pressed = self.count_spinning

    def count_spinning(self):
        """Count the number of half spins"""
        self.half_spin_count += 1

    def calculate_wind_speed(self):
        return self.half_spin_count / self.recording_interval / 2.0 * 2.4

    def run(self):
        while True:
            self.half_spin_count = 0
            sleep(self.recording_interval)
            print("{0:.2f} km/h - {1:.2f} m/s".format(self.calculate_wind_speed))

if __name__ == '__main__':
    X = Speed()
    Speed.run()

