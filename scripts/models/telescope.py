import numpy as np

# Models a telescope on the surface of the Earth.
class Telescope:
    # Constructs a telescope.
    def __init__(self, origin=np.array([0,0,0]), angle=0):
        self.origin = origin
        self.angle = angle
        self.dist_origin = np.linalg.norm(origin)
        self.slope = np.tanh(np.pi / 2 - angle)

    def can_view(self, point):
        # Distance of point from center line
        intersection_point = np.cross(point, self.origin)
        distX =  np.linalg.norm(intersection_point / np.linalg.norm(self.origin))
        dist_origin = np.linalg.norm(point)

        # Distance along line from origin
        distY = np.sqrt(np.power(dist_origin, 2) - np.power(distX, 2))
        if (point[0] - self.origin[0] + point[1] - self.origin[1] + point[2] - self.origin[2]) < 0:
            distY *= -1

        # Distance threshold for being withint the view of the telescope
        thresholdY = self.dist_origin + self.slope * distX

        return thresholdY < distY