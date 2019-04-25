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
        self.rad_angle = (angle * np.pi) / 360

        self.unit_vec = self.origin / np.linalg.norm(self.origin)

    # Determines if the telescope can view a satellite
    def can_view(self, point):
        # Determines angle between the telescope and satellite along the line between them
        sight_vec = point - self.origin
        sight_vec = sight_vec / np.linalg.norm(sight_vec)
        angle = math.acos(np.dot(sight_vec, self.unit_vec))

        return angle < self.rad_angle