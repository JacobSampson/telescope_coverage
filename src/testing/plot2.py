import numpy as np


import math, random

def fibonacci_sphere(samples=100,randomize=True):
    rnd = 1.
    if randomize:
        rnd = random.random() * samples

    x = []
    y = []
    z = []
    offset = 2./samples
    increment = math.pi * (3. - np.sqrt(5.))

    for i in range(samples):
        temp =((i * offset) - 1) + (offset / 2)
        y.append(temp)
        r = math.sqrt(1 - y * y)

        phi = ((i + rnd) % samples) * increment

        x.append(float(math.cos(phi) * r))
        z.append(float(math.sin(phi) * r))

    return x, y, z

def sample_spherical(npoints, ndim=3):
    vec = np.random.randn(ndim, npoints)

    vec /= np.linalg.norm(vec, axis=0)

    i = np.append(vec[0], 1.)
    j = np.append(vec[1], 1.)
    k = np.append(vec[2], 1.)
    vec = [i, j, k]

    return vec
    
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d

phi = np.linspace(0, np.pi, 20)
theta = np.linspace(0, 2 * np.pi, 40)
x = np.outer(np.sin(theta), np.cos(phi))
y = np.outer(np.sin(theta), np.sin(phi))
z = np.outer(np.cos(theta), np.ones_like(phi))

p = np.linspace(np.pi / -2, 0, 20)
t = np.linspace(0, 2 * np.pi, 40)

multiplier = 1.5

x2 = multiplier * np.outer(np.sin(t), np.cos(p))
y2 = multiplier * np.outer(np.sin(t), np.sin(p))
z2 = multiplier * np.outer(np.cos(t), np.ones_like(p))

xi, yi, zi = sample_spherical(0)

fig, ax = plt.subplots(1, 1, subplot_kw={'projection':'3d', 'aspect':'equal'})
ax.plot_wireframe(x, y, z, color='k', rstride=1, cstride=1)
ax.plot_wireframe(x2, y2, z2, color='yellow', rstride=1, cstride=1)
ax.scatter(xi, yi, zi, s=200, c='red', zorder=1)

i, j, k = fibonacci_sphere()

ax.scatter(i, j, k, s=200, c='r', zorder=1)


plt.show()














# import numpy as np

# def generate_sphere(npoints, ndim=3):
#     vec = np.random.randn(ndim, npoints)
#     vec /= np.linalg.norm(vec, axis=0)
#     return vec

# def generate_cone(range):
#     phi = np.linspace(0, range, 20)
#     theta = np.linspace(0, 2 * np.pi, 40)

#     x = 1.5 * np.outer(np.sin(theta), np.cos(phi))
#     y = 1.5 * np.outer(np.sin(theta), np.sin(phi))
#     z = 1.5 * np.outer(np.cos(theta), np.ones_like(phi))

#     vec = x, y, z

#     return vec
    
# from matplotlib import pyplot as plt



# xi, yi, zi = generate_sphere(1)

# phi = np.linspace(0, np.pi / 4, 20)
# theta = np.linspace(0, 2 * np.pi, 40)

# x2 = 1.5 * np.outer(np.sin(theta), np.cos(phi))
# y2 = 1.5 * np.outer(np.sin(theta), np.sin(phi))
# z2 = 1.5 * np.outer(np.cos(theta), np.ones_like(phi))

# # x2i, y2i, z2i = generate_cone(np.pi / 4)

# fig, ax = plt.subplots(1, 1, subplot_kw={'projection':'3d', 'aspect':'equal'})
# ax.plot_wireframe(x, y, z, color='k', rstride=1, cstride=1)
# ax.plot_wireframe(x2, y2, z2, color='yellow', rstride=1, cstride=1)
# ax.scatter(xi, yi, zi, s=100, c='r', zorder=10)