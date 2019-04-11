import numpy as np

# Models a satellite orbiting Earth
class Satellite:
    # Constructs a satellite
    def __init__(self, origin=np.array([0,0,0]), in_view = False):
        # The location of the satellite in cartesian coordinates
        self.origin = origin

        # Indicates whether the satellite is in view of a telescope
        self.in_view = in_view