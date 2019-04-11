import numpy as np

# Models a telescope
class Telescope:
    # Constructs a telescope
    def __init__(self, name="", origin=np.array([0, 0, 0]), angle=0):
        # The telescopes name
        self.name = name

        # The location of the telescope in cartesian coordinates
        self.origin = origin

        # Half of the telescope's viewing angle in radians
        rad_angle = (angle * np.pi) / 360

        # The telescope's distance from the center of the Earth
        self.dist_origin = np.linalg.norm(origin)

        # The slope of the telescope's viewing cone relative to a line passing through the 
        # Earth's center and the telescope
        self.slope = np.tan((np.pi / 2) - self.rad_angle)

    # Determines if the telescope can view a sattelite
    def can_view(self, point):
        # Determines if sattelite is in front of telescope
        if (np.dot(point, self.origin) / np.linalg.norm(point) / self.dist_origin) < 0:
            return False

        # Sattelite's distance from center line of the telescope's viewing cone
        intersection_point = np.cross(point, self.origin)
        dist_x = np.linalg.norm(intersection_point / self.origin)

        # Sattelite's distance from the center of the Earth
        dist_point = np.linalg.norm(point)
        dist_y = np.sqrt(np.abs(np.power(dist_point, 2) - np.power(dist_x, 2)))

        # Distance threshold for being in view of the telescope
        threshold_y = self.dist_origin + self.slope * dist_x

        return threshold_y < dist_y
