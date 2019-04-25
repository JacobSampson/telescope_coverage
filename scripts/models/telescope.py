import numpy as np
import math

# Models a telescope
class Telescope:
    # Constructs a telescope
    def __init__(self, name="", origin=np.array([0, 0, 0]), angle=0):
        # The telescopes name
        self.name = name

        # The location of the telescope in cartesian coordinates
        self.origin = origin

        # Half of the telescope's viewing angle in radians
        self.rad_angle = (angle * np.pi) / 180

        # The telescope's distance from the center of the Earth
        self.dist_origin = np.linalg.norm(origin)

    # Determines if the telescope can view a satellite
    def can_view(self, point):
        # Determines angle between the telescope and satellite along the line between them
        angle = np.dot(point, self.origin) / np.linalg.norm(point) / self.dist_origin

        if angle > (self.rad_angle / 2):
            return True