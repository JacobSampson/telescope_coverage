import numpy as np
import math

from models.telescope import Telescope
from utility.angle_conversions import degrees_to_coords

#from telescope_system import RADIUS_EARTH
RADIUS_EARTH = 6371

# Models a weather system around the Earth
class WeatherSystem:
    altitude_weather = {}

    # Constructs a system of weather coverage data
    def __init__(self, altitude_weather={}, theta_density=0, phi_density=0):
        self.altitude_weather = altitude_weather
        self.theta_density = theta_density
        self.phi_density = phi_density

    def create_altitude(self, altitude=0):
        data_points = np.ones(shape=(self.theta_density, self.phi_density), dtype=np.bool)
        data_points.fill(False)

        # TESTING
        data_points[7][8] = True
        data_points[7][9] = True
        ###

        self.altitude_weather[altitude] = data_points
        return data_points

    def blocks_line(self, origin=np.array([0, 0, 0]), point=np.array([0, 0, 0])):
        direction = point - origin

        for altitude in self.altitude_weather:
            unit_direction = direction / np.linalg.norm(direction)

            t = -1 * np.dot(unit_direction, origin)
            t += math.sqrt(np.dot(unit_direction, origin)**2 - np.linalg.norm(origin)**2 + np.linalg.norm(origin)**2)

            coords = origin + t * unit_direction
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

        return phi_orbital[closest_phi]

    def get_closest_index(self, data_range=0, density=1, value=0):
        step = data_range / density

        index = round(value / step)

        if index == density:
            return 0
        else:
            return index

def coords_to_spherical(coords=[0, 0, 0], radius=0):
    spherical_coords = []
    if radius == 0: radius = np.linalg.norm(coords)

    theta = math.atan(coords[1] / coords[0])
    if coords[1] < 0:
        theta += np.pi
        if coords[0] > 0:
            theta += np.pi
    if theta < 0:
        theta = np.pi + theta
    spherical_coords.append(theta)

    phi = math.acos(coords[2] / radius)
    spherical_coords.append(phi)

    return spherical_coords

def get_weather_system_grid(weather_system=WeatherSystem()):
    theta_density = weather_system.theta_density
    phi_density = weather_system.phi_density

    weather_system_grid = []

    for altitude in weather_system.altitude_weather:
        data_points = weather_system.altitude_weather[altitude]

        for i in range(len(data_points)):
            for j in range(len(data_points[i])):
                if (data_points[i][j]):
                    theta = (2 * np.pi / theta_density * i) * 180 / np.pi
                    phi = (np.pi / phi_density * j) * 180 /np.pi

                    delta_theta = (np.pi / theta_density) * 180 / np.pi
                    delta_phi = (np.pi / phi_density / 2) * 180 / np.pi

                    factor = 4

                    weather_system_grid.append(factor * np.array(degrees_to_coords(theta=theta - delta_theta, phi=phi - delta_phi))) # Bottom left
                    weather_system_grid.append(factor * np.array(degrees_to_coords(theta=theta - delta_theta, phi=phi + delta_phi))) # Top left
                    weather_system_grid.append(factor * np.array(degrees_to_coords(theta=theta + delta_theta, phi=phi + delta_phi))) # Top right
                    weather_system_grid.append(factor * np.array(degrees_to_coords(theta=theta + delta_theta, phi=phi - delta_phi))) # Bottom right
    
    return weather_system_grid