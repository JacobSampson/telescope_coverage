import numpy as np
import math

from models.telescope import Telescope

#from telescope_system import RADIUS_EARTH
RADIUS_EARTH = 6371

# Models a weather system around the Earth
class WeatherSystem:
    altitude_weather = {}

    # Constructs a system of weather coverage data
    def __init__(self, altitude_weather={}, data_point_size=0, theta_density=0, phi_density=0):
        self.altitude_weather = altitude_weather
        self.data_point_size = data_point_size
        self.theta_density = theta_density
        self.phi_density = phi_density

    def blocks_line(self, telescope=Telescope(), point=np.array([0, 0, 0])):
        direction = telescope.origin - point

        for altitude in self.altitude_weather:
            unit_direction = direction / np.linalg.norm(direction)

            t = -1 * np.dot(unit_direction, telescope.origin)
            t += math.sqrt(np.dot(unit_direction, telescope.origin)**2 - np.linalg.norm(telescope.origin)**2 + np.linalg.norm(telescope.origin)**2)

            coords = telescope.origin + t * unit_direction
            spherical_coords = coords_to_spherical(coords=coords, radius=altitude)
            
            theta = spherical_coords[0]
            phi = spherical_coords[1]

            weather_orbital = self.altitude_weather.get(altitude)
            if (self.is_blocked(theta=theta, phi=phi, weather_orbital=weather_orbital)):
                return True

        return False

    def is_blocked(self, theta=0, phi=0, weather_orbital=[]):
        closest_theta = int(self.get_closest_index(data_range=2 * np.pi, density=self.theta_density, value=theta))
        phi_orbital = weather_orbital[closest_theta]

        closest_phi = int(self.get_closest_index(data_range=np.pi, density=self.phi_density, value=phi))

        ### TESTING
        if closest_theta == 10:
            if closest_phi == 5:
                this = 6

        if phi_orbital[closest_phi]:
            this =76
        ###

        return phi_orbital[closest_phi]

    def get_closest_index(self, data_range=0, density=1, value=0):
        step = data_range / density

        return round(value / step)

def coords_to_spherical(coords=[0, 0, 0], radius=0):
    spherical_coords = []
    if radius == 0: radius = np.linalg.norm(coords)

    theta = math.atan(coords[1] / coords[0])

    

    phi = math.acos(coords[2] / radius)


    return spherical_coords