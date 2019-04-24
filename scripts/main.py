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
from models.telescope_system import (TelescopeSystem, degrees_to_coords, long_lat_to_coords, RADIUS_EARTH, DISTANCE_SATELLITES)
from models.weather_system import WeatherSystem

def main():
    # Creates scene
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect("equal")




    # Add clouds
    theta_density = 20
    phi_density = 10

    altitude = 3 * RADIUS_EARTH
    tel = Telescope(name="Maui, Hawaii", origin=long_lat_to_coords("0 0 0 N 0 0 0 W"), angle=130/2)
    # coords = np.array(long_lat_to_coords("180 0 0 N 0 0 0 W"))
    # coords *= 3

    thetas = np.ones(shape=(theta_density, phi_density), dtype=np.bool)
    thetas.fill(False)

    # thetas[int(theta_density / 2)][int(phi_density / 2)] = True
    thetas[19][4] = True

    data = {
        altitude: thetas
    }


    weather_system = WeatherSystem(altitude_weather=data, data_point_size=100, theta_density=theta_density, phi_density=phi_density)


    # Generate plotted points representing cloud data
    for i in range(len(thetas)):
        for j in range(len(thetas[i])):
            if (thetas[i][j]):
                the = (2 * np.pi / theta_density * i) * 180 / np.pi
                ph = (np.pi / phi_density * j) * 180 /np.pi

                delta_the = (np.pi / theta_density) * 180 / np.pi
                delta_ph = (np.pi / phi_density / 2) * 180 / np.pi

                factor = 3

                bottom_left = factor * np.array(degrees_to_coords(theta=the - delta_the, phi=ph - delta_ph))
                top_left = factor * np.array(degrees_to_coords(theta=the - delta_the, phi=ph + delta_ph))
                top_right = factor * np.array(degrees_to_coords(theta=the + delta_the, phi=ph + delta_ph))
                bottom_right = factor * np.array(degrees_to_coords(theta=the + delta_the, phi=ph - delta_ph))

                ax.scatter(bottom_left[0], bottom_left[1], bottom_left[2], color="black", s=30)
                ax.scatter(top_left[0], top_left[1], top_left[2], color="black", s=30)
                ax.scatter(top_right[0], top_right[1], top_right[2], color="black", s=30)
                ax.scatter(bottom_right[0], bottom_right[1], bottom_right[2], color="black", s=30)

    weather_systems = [
        weather_system
    ]

    point = 2 * long_lat_to_coords("3 0 0 N 3 0 0 W")

    result = weather_system.blocks_line(telescope=tel, point = point)





    telescope_system = TelescopeSystem(satellite_angle=30, weather_systems=weather_systems, telescope_angle=90, phi_density=5, theta_density=50)
    # telescope_system.create_system()
    telescope_system.create_earth()
    telescope_system.create_satellites()

    y = RADIUS_EARTH / 2
    z = np.sqrt(3) * y

    # Add existing telescopes
    existing_tels = []
    existing_tels.append(Telescope(name="Maui, Hawaii", origin=long_lat_to_coords("20 47 54 N 156 19 55 W"), angle=130/2))
    existing_tels.append(Telescope(name="Socorro, New Mexico", origin=long_lat_to_coords("34 06 52 N 106 48 46 W"), angle=130/2))
    existing_tels.append(Telescope(name="Diego Garcia, British Indian Ocean Territory", origin=long_lat_to_coords("7 21 50 S 72 41 43 E"), angle=130/2))
    existing_tels.append(Telescope(name="Learmonth, Australia", origin=long_lat_to_coords("22 14 05 S 114 05 16 E"), angle=130/2))
    telescope_system.add_telescopes(existing_tels)

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