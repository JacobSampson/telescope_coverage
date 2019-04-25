import numpy as np

from models.telescope import Telescope
from models.satellite import Satellite
from models.weather_system import WeatherSystem

RADIUS_EARTH = 6371
DISTANCE_SATELLITES = 35786

# Models a system of telescopes and satellites in orbit around Earth
class TelescopeSystem:
    # Constants
    num_telescopes = 3

    # Fields 
    earth = []
    satellites = []
    telescopes = []

    weather_systems = []

    # Statistics
    num_in_view = 0

    # Constructs a system of telescopes and satellites
    def __init__(self, weather_systems = [WeatherSystem()], satellite_angle = 15, telescope_angle = 150, phi_density = 20, theta_density = 20):
        self.satellite_angle = satellite_angle / 2
        self.telescope_angle = telescope_angle
        self.phi_density = phi_density
        self.theta_density = theta_density

        self.weather_systems = weather_systems

    # Generates a complete system
    def create_system(self):
        self.create_earth()
        self.create_telescopes()
        self.create_satellites()

    # Creates Earth
    def create_earth(self):
        earth = create_sphere(radius = RADIUS_EARTH, phi_density = self.phi_density, theta_density = self.theta_density)
        self.earth = earth
        return earth

    # Creates telescopes
    def create_telescopes(self):
        # Adds telescopes vertices to Earth
        self.fib = fibonacci_sphere(samples=self.num_telescopes)

        # Creates telescopes from vertices
        radian_telescope_angle = self.telescope_angle * np.pi / 180

        # Adds telescopes
        telescopes = []
        for i in range(self.fib[0].size):
            point = RADIUS_EARTH * np.array((self.fib[0][i], self.fib[1][i], self.fib[2][i]))
            telescopes.append(Telescope(origin=point, angle=radian_telescope_angle))
        self.telescopes = telescopes
        return telescopes

    # Creates satellites with visibility subject to existing telescopes
    def create_satellites(self):
        # Creates satellite band
        distance = RADIUS_EARTH + DISTANCE_SATELLITES

        radian_angle = self.satellite_angle * np.pi / 180
        min_phi = np.pi / 2 - radian_angle
        max_phi = np.pi / 2 + radian_angle
        satellite_zone = create_sphere(min_phi = min_phi, max_phi = max_phi, radius = distance, phi_density = self.phi_density, theta_density = self.theta_density)

        # Creates satellites and checks if they are within telescope view
        satellites = []
        for i in range(self.phi_density):
            for j in range(self.theta_density):
                point = np.array((satellite_zone[0][i][j], satellite_zone[1][i][j], satellite_zone[2][i][j]))
                satellites.append(Satellite(origin = point, in_view = False))
        self.satellites = satellites

        self.update_satellites()

        return satellites

    # Checks through satelites and updates their visibility
    def update_satellites(self):
        self.num_in_view = 0

        for sat in self.satellites:
            sat.in_view = False
            point = sat.origin
            for tel in self.telescopes:
                if (tel.can_view(point)):
                    if (self.weather_systems[0].blocks_line(origin=tel.origin, point=point)): 
                        sat.in_view = True
                        self.num_in_view += 1
                        break
        return self.num_in_view / len(self.satellites)

    # Adds telescopes
    def add_telescopes(self, telescopes=[]):
        for tel in telescopes:
            self.telescopes.append(tel)
            


# Creates a sphere given ranges for theta and phi and a radius
def create_sphere(min_phi = 0, max_phi = np.pi, phi_density = 180, min_theta = 0, max_theta = 2 * np.pi, theta_density = 360, x_coord = 0, y_coord = 0, z_coord = 0, radius = 1):
    phi = np.linspace(min_phi, max_phi, phi_density)
    theta = np.linspace(min_theta, max_theta, theta_density)

    x = radius * np.outer(np.sin(phi), np.cos(theta))
    y = radius * np.outer(np.sin(phi), np.sin(theta))
    z = radius * np.outer(np.cos(phi), np.ones_like(theta))

    return (x, y, z)

import random

# Places roughly evenly distributed points along the surface of a sphere
# Modified from stack overflow (proper sourcing to come)
def fibonacci_sphere(samples=100,randomize=False):
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

# Converts degrees, minutes, seconds to cartesian coordinates
def long_lat_to_coords(long_lat="0 0 0 N 0 0 0 W"):
    identifiers = long_lat.split(" ")

    phi = 90
    phi -= int(identifiers[0])
    phi -= int(identifiers[1]) / 60
    phi -= int(identifiers[2]) / 360
    if (identifiers[3] == "S"):
        phi = 180 - phi

    theta = int(identifiers[4])
    theta += int(identifiers[5]) / 60
    theta += int(identifiers[6]) / 360
    if (identifiers[7] == "W"):
        theta = 360 - theta

    return degrees_to_coords(theta, phi)

# Converts spherical coordinates to cartesian coordinates
def degrees_to_coords(theta=0, phi=0):
    rad_theta = np.pi * theta / 180.  
    rad_phi = np.pi * phi / 180.

    x = RADIUS_EARTH * np.sin(rad_phi) * np.cos(rad_theta)
    y = RADIUS_EARTH * np.sin(rad_phi) * np.sin(rad_theta)
    z = RADIUS_EARTH * np.cos(rad_phi)

    return np.array([x, y, z])