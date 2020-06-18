class Converter:
    """Convert the wind speed from km/h in m/s"""

    def __init__(self, speed):
        self.speed = speed

    @property
    def get_speed_in_ms(self):
        return self.speed * 3.6
