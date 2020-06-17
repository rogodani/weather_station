from gpiozero import Button
from time import sleep
from .wind_speed_converter import Converter

# interval of time for which the wind speed should be recorded
recording_interval = 5
half_spin_count = 0


def count_spinings():
    """Count the number of half spins"""
    global half_spin_count
    half_spin_count += 1


def calculate_wind_speed(interval):
    """Calculate the wind speed in km/h
    :param:
        interval: recording interval for winf speed in seconds
    :return:
        wind speed in km/h
    """
    return half_spin_count / interval / 2.0 * 2.4


wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = count_spinings

while True:
    half_spin_count = 0
    sleep(recording_interval)
    wind_speed = calculate_wind_speed(recording_interval)
    print("{0:.2f} km/h - {1:.2f} m/s".format(wind_speed, Converter(wind_speed).get_speed_in_ms))
