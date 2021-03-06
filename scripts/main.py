"""
=========================================
Telescope coverage of satellites in orbit
=========================================

Displays the coverage that telescopes on Earth have over the satellites in orbit at a particular orbital,
given the degree which the telescopes can view.
"""

import numpy as np
import matplotlib.pyplot as plt

from models.telescope import Telescope
from models.telescope_system import (TelescopeSystem)
from models.weather_system import (WeatherSystem, get_weather_system_grid)

from utility.angle_conversions import (spherical_to_coords, long_lat_to_coords, RADIUS_EARTH, DISTANCE_SATELLITES)

def main():
    # Creates scene
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect("equal")

    telescope_system = TelescopeSystem(satellite_angle=30, telescope_angle=100, theta_density=50, phi_density=5)
    # telescope_system.create_system()
    telescope_system.create_earth()
    telescope_system.create_satellites()

    # Add existing telescopes
    existing_tels = []
    tel_angle = 130
    existing_tels.append(Telescope(name="Maui, Hawaii", origin=long_lat_to_coords("20 47 54 N 156 19 55 W"), angle=tel_angle))
    existing_tels.append(Telescope(name="Socorro, New Mexico", origin=long_lat_to_coords("34 06 52 N 106 48 46 W"), angle=tel_angle))
    existing_tels.append(Telescope(name="Diego Garcia, British Indian Ocean Territory", origin=long_lat_to_coords("7 21 50 S 72 41 43 E"), angle=tel_angle))
    existing_tels.append(Telescope(name="Learmonth, Australia", origin=long_lat_to_coords("22 14 05 S 114 05 16 E"), angle=tel_angle))

    tel = Telescope(name="TEST", origin=long_lat_to_coords("20 0 0 S 90 0 0 W"), angle=90)
    existing_tels.append(tel)
    telescope_system.add_telescopes(existing_tels)



    # Plot points representing cloud data
    angle_density = 10
    altitude = 10000

    weather_system = WeatherSystem(theta_density=angle_density, phi_density=angle_density)
    weather_data = weather_system.create_altitude(altitude = altitude)
    # TESTING
    weather_data[3][3] = True
    weather_data[3][4] = True
    weather_data[3][5] = True
    weather_data[3][6] = True
    weather_data[3][7] = True
    ###
    telescope_system.add_weather_system(weather_system=weather_system)
    data_points = get_weather_system_grid(weather_system=weather_system)

    # Plot weather data
    for data_point in data_points:
        ax.scatter(data_point[0], data_point[1], data_point[2], color = "black", s = 20)

    telescope_system.update_satellites()



    # Create Earth
    earth = telescope_system.earth
    ax.plot_surface(earth[0], earth[1], earth[2], color='blue', rstride=1, cstride=1, alpha=.8)

    # Create telescopes
    telescopes = telescope_system.telescopes

    for tel in telescopes:
        point = tel.origin
        ax.scatter(point[0], point[1], point[2], color='yellow', s=100)

        multiplier = 5

        x = point[0]
        y = point[1]
        z = point[2]

        b = Arrow3D([x, x * multiplier], [y, y * multiplier], [z, z * multiplier], mutation_scale=20, lw=1,
                    arrowStyle="-|>", color="k")
        ax.add_artist(b)

    # Create satellites
    satellites = telescope_system.satellites
    for sat in satellites:
        c = "green" if sat.in_view else "red"
        point = sat.origin
        ax.scatter(point[0], point[1], point[2], color=c, s=10)

    # Plotted for scaling
    ax.scatter([0], [0], [RADIUS_EARTH + DISTANCE_SATELLITES], color="black", s=10,
               alpha=0.0)
    ax.scatter([0], [0], [-(RADIUS_EARTH + DISTANCE_SATELLITES)], color="black", s=10,
               alpha=0.0)

    # Coverage
    num_satellites = len(satellites)
    print(telescope_system.num_in_view / num_satellites)

    plt.show()


# Vector arrows
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


# From stack overflow (proper sourcing to come). Renders the arrows that reopresent the telescopes
class Arrow3D(FancyArrowPatch):

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

if __name__ == "__main__":
    main()