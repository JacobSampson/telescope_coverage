import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as axes3d
import math, random
import vispy.plot as vp

def fibonacci_sphere(samples=1,randomize=True):
    rnd = 1.
    if randomize:
        rnd = random.random() * samples

    points = []
    i = []
    j = []
    k = []

    offset = 2./samples
    increment = math.pi * (3. - math.sqrt(5.))

    for q in range(samples):
        y = ((q * offset) - 1) + (offset / 2)
        j.append(y)

        r = math.sqrt(1 - pow(y,2))

        phi = ((q + rnd) % samples) * increment

        x = math.cos(phi) * r
        i.append(x)

        z = math.sin(phi) * r
        k.append(z)

        points.append([x,y,z])

    return i, j, k

i, j, k = fibonacci_sphere(500) 

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

# draw sphere
u, v = np.mgrid[0:2*np.pi:360j, 0:np.pi:181j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_surface(x, y, z, alpha = 0.5, facecolor = "blue", edgecolor = "green", zorder = 5)

ax.scatter(i, j, k, s = 200, color = 'red', zorder = 10)
ax.set_aspect('equal')
plt.show()