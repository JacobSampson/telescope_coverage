'''
=========================================
Telescope coverage of satellites in orbit
=========================================

Displays the coverage that telescopes on Earth have over the satellites in orbit at a particular orbital, given the degree which the telescopes can view.
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from models.telescope import Telescope
from models.telescope_system import TelescopeSystem

def main():
    # Creates scene
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect("equal")

    telescope_system = TelescopeSystem(satellite_angle = 90, telescope_angle = 90, phi_density = 30, theta_density = 30)
    #telescope_system.create_system()
    telescope_system.create_earth()

    y = telescope_system.RADIUS_EARTH / 2
    z = np.sqrt(3) * y

    telescope_system.telescopes = [Telescope([0, y, z], angle=80)]
    telescope_system.create_satellites()

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

        b = Arrow3D([x, x * multiplier], [y, y * multiplier], [z, z * multiplier], mutation_scale = 20, lw = 1, arrowStyle = "-|>", color = "k")
        ax.add_artist(b)

    # Create satellites
    satellites = telescope_system.satellites
    for sat in satellites:
        c = "green" if sat.in_view else "red"
        point = sat.origin  
        ax.scatter(point[0], point[1], point[2], color=c, s=10)
    
    # Plotted for scaling
    ax.scatter([0], [0], [telescope_system.RADIUS_EARTH + telescope_system.DISTANCE_SATELLITES], color="black", s=10, alpha=0.0)
    ax.scatter([0], [0], [-(telescope_system.RADIUS_EARTH + telescope_system.DISTANCE_SATELLITES)], color="black", s=10, alpha=0.0)

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