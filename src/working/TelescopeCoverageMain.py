'''
=========================================
Telescope coverage of satellites in orbit
=========================================

Displays the coverage that telescopes on Earth have over the satellites in orbit at a particular orbital, given the degree which the telescopes can view.
'''

# Math tools
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# Constants
radius_earth = 6371
distance_satellites = 35786
satellite_angle = 30
telescopeAngle = 15
theta_density = 30
phi_density = 5

# Vector arrows
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

# From stack overflow (proper sourcing to come). Renders the arrows that reopresent the telescopes.
class Arrow3D(FancyArrowPatch):

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

# Creates a sphere given ranges for theta and phi and a radius.
def create_sphere(min_phi = 0, max_phi = np.pi, min_theta = 0, max_theta = 2 * np.pi, x_coord = 0, y_coord = 0, z_coord = 0, radius = 1):
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

# Models a telescope on the surface of the Earth.
class Telescope:

    # Constructs a telescope.
    def __init__(self, origin=np.array([0,0,0]), angle=0):
        self.origin = origin
        self.angle = angle
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
        thresholdY = radius_earth + self.slope * distX

        return thresholdY < distY

# Creates scene.
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

# Creates Earth.
earth = create_sphere(radius = radius_earth)
ax.plot_surface(earth[0], earth[1], earth[2], color='blue', rstride=1, cstride=1, alpha=.8)

# Adds telescopes vertices to Earth.
fib = fibonacci_sphere(samples=5)
ax.scatter(fib[0], fib[1], fib[2], color='green', s=10)

# Creates telescopes from vertices.
randian_telescope_angle = telescopeAngle * np.pi / 180

telescopes = []
for i in range(fib[0].size):
    point = np.array((fib[0][i], fib[1][i], fib[2][i]))
    telescopes.append(Telescope(origin=point, angle=randian_telescope_angle))

    multiplier = 50000
    
    x = fib[0][i]
    y = fib[1][i]
    z = fib[2][i]

    b = Arrow3D([x, x * multiplier], [y, y * multiplier], [z, z * multiplier], mutation_scale = 20, lw = 1, arrowStyle = "-|>", color = "k")
    ax.add_artist(b)

# Creates satellite band.
distance = radius_earth + distance_satellites

radian_angle = satellite_angle * np.pi / 180
satellite_zone = create_sphere(min_phi = np.pi / 2 - radian_angle, max_phi = np.pi / 2 + radian_angle, radius = distance)

# Checks if points in satellite band are within telescope view.
for i in range(phi_density):
    for j in range(theta_density):
        point = np.array((satellite_zone[0][i][j], satellite_zone[1][i][j], satellite_zone[2][i][j]))

        c = 'red'

        for telescope in telescopes:
            if telescope.can_view(point): c = 'green'
        
        ax.scatter(point[0], point[1], point[2], color=c, s=20)

# Plotted for scaling
ax.scatter([0], [0], [radius_earth + distance_satellites], color="black", s=10, alpha=0.0)
ax.scatter([0], [0], [-(radius_earth + distance_satellites)], color="black", s=10, alpha=0.0)

plt.show()