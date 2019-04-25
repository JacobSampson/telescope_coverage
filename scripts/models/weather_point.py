import numpy as np

# Models a point of weather data around Earth
class WeatherPoint:
    # Constructs a weather point
    def __init__(self, blocked=False):
        # The level of blocking of the weather point
        self.blocked = blocked

    def blocks(self):
        return self.blocked