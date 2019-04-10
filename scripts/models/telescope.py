import numpy as np


# Models a telescope on the surface of the Earth.
class Telescope:
    # Constructs a telescope.
    def __init__(self, origin=np.array([0, 0, 0]), angle=0):
        self.origin = origin
        self.rad_angle = (angle * np.pi) / 180
        self.dist_origin = np.linalg.norm(origin)
        self.slope = np.tan((np.pi / 2) - self.rad_angle)

    def can_view(self, point):
        # Check if point is in correct direction
        if (np.dot(point, self.origin) / np.linalg.norm(point) / np.linalg.norm(self.origin)) < 0:
            return False

        # Distance of point from center line
        intersection_point = np.cross(point, self.origin)
        dist_x = np.linalg.norm(intersection_point / np.linalg.norm(self.origin))

        # Distance along line from origin
        dist_point = np.linalg.norm(point)
        dist_y = np.sqrt(np.abs(np.power(dist_point, 2) - np.power(dist_x, 2)))

        # Distance threshold for being withint the view of the telescope
        threshold_y = self.dist_origin + self.slope * dist_x

        return threshold_y < dist_y
