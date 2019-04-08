import numpy as np
from models.telescope import Telescope
from models.satellite import Satellite

class TelescopeSystem():
    # Constants
    RADIUS_EARTH = 6371
    DISTANCE_SATELLITES = 35786
    phi_density = 100
    theta_density = 100

    # Statistics
    num_in_view = 0

    # Constructs a telescope.
    def __init__(self, satellite_angle = 15, telescope_angle = 150):
        self.satellite_angle = satellite_angle
        self.telescope_angle = telescope_angle

        self.earth = self.create_earth()
        self.telescopes = self.create_telescopes()
        self.satellites = self.create_satellites()
        
    def create_earth(self):
        # Creates Earth.
        self.earth = create_sphere(radius = self.RADIUS_EARTH, phi_density = self.phi_density, theta_density = self.theta_density)
        return self.earth

    def create_telescopes(self):
        # Adds telescopes vertices to Earth.
        self.fib = fibonacci_sphere(samples=5)

        # Creates telescopes from vertices.
        radian_telescope_angle = self.telescope_angle * np.pi / 180

        telescopes = []
        for i in range(self.fib[0].size):
            point = self.RADIUS_EARTH * np.array((self.fib[0][i], self.fib[1][i], self.fib[2][i]))
            telescopes.append(Telescope(origin=point, angle=radian_telescope_angle))
        return telescopes

    def create_satellites(self):
        # Creates satellite band.
        distance = self.RADIUS_EARTH + self.DISTANCE_SATELLITES

        radian_angle = self.satellite_angle * np.pi / 180
        min_phi = np.pi / 2 - radian_angle
        max_phi = np.pi / 2 + radian_angle
        satellite_zone = create_sphere(min_phi = min_phi, max_phi = max_phi, radius = distance, phi_density = self.phi_density, theta_density = self.theta_density)

        satellites = []
        # Creates satellites and checks if point is within telescope view.
        for i in range(self.phi_density):
            for j in range(self.theta_density):
                point = np.array((satellite_zone[0][i][j], satellite_zone[1][i][j], satellite_zone[2][i][j]))

                for telescope in self.telescopes:
                    in_view = telescope.can_view(point)
                    if (in_view):
                        self.num_in_view += 1
                        break
                satellites.append(Satellite(point, in_view))
        return satellites
                    
# Creates a sphere given ranges for theta and phi and a radius.
def create_sphere(min_phi = 0, max_phi = np.pi, phi_density = 180, min_theta = 0, max_theta = 2 * np.pi, theta_density = 360, x_coord = 0, y_coord = 0, z_coord = 0, radius = 1):
    phi = np.linspace(min_phi, max_phi, phi_density)
    theta = np.linspace(min_theta, max_theta, theta_density)

    x = radius * np.outer(np.sin(phi), np.cos(theta))
    y = radius * np.outer(np.sin(phi), np.sin(theta))
    z = radius * np.outer(np.cos(phi), np.ones_like(theta))

    return (x, y, z)

import random

# Modified from stack overflow (proper sourcing to come). Places roughly evenly distributed points along the surface of a sphere.
def fibonacci_sphere(samples=100,randomize=True):
    rnd = 1.
    if randomize:
        rnd = random.random() * samples

    x = []
    y = []
    z = []

    offset = 2./samples
    increment = np.pi * (3. - np.sqrt(5.))

    for i in range(samples):
        temp = ((i * offset) - 1) + (offset / 2)
        y.append(temp)
        r = np.sqrt(1 - temp * temp)

        phi = ((i + rnd) % samples) * increment

        x.append(float(np.cos(phi) * r))
        z.append(float(np.sin(phi) * r))

    return [np.array(x), np.array(y), np.array(z)]