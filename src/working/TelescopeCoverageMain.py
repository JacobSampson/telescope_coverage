import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math

radiusEarth = 6371
distanceSatellites = 35786

def generateSphere(minPhi = 0, maxPhi = np.pi, minTheta = 0, maxTheta = 2 * np.pi, xCoord = 0, yCoord = 0, zCoord = 0, radius = 1):
    phi = np.linspace(minPhi, maxPhi, 40)
    theta = np.linspace(minTheta, maxTheta, 40)

    x = radius * np.outer(np.sin(phi), np.cos(theta))
    y = radius * np.outer(np.sin(phi), np.sin(theta))
    z = radius * np.outer(np.cos(phi), np.ones_like(theta))

    return (x, y, z)

class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def getDistance(self, point):
        xDist = math.pow(self.x - point.x, 2)
        yDist = math.pow(self.y - point.y, 2)
        zDist = math.pow(self.z - point.z, 2)

        return math.sqrt(xDist + yDist + zDist)

class Telescope:
    def __init__(self, origin=Point(0, 0, 0), angle=0):
        self.origin = origin
        self.angle = angle

    def compare(self, point):
        distance = self.origin.getDistance(point)
        return distance

# Scene
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

# Earth
earth = generateSphere(radius = radiusEarth)
ax.plot_surface(earth[0], earth[1], earth[2], color='green', rstride=1, cstride=1)

# Satellite zone
angle = 15
distance = radiusEarth + distanceSatellites

radianAngle = angle * np.pi / 180
satelliteZone = generateSphere(minPhi = np.pi / 2 - radianAngle, maxPhi = np.pi / 2 + radianAngle, radius = distance)
ax.plot_wireframe(satelliteZone[0], satelliteZone[1], satelliteZone[2], cmap='Greens', rstride=1, cstride=1)

ax.scatter([0], [0], [radiusEarth], color="red", s=200)

# Telescope cone
telescopeAngle = 15

radianTelescopeAngle = telescopeAngle * np.pi / 180
telescope = Telescope()
testPoint = Point(1, 1, 1)
print(telescope.compare(testPoint))


# Telescope placement
# fib = fibonacci_sphere()
# ax.plot_wireframe(fib[0], fib[1], fib[2], cmap='Greens', rstride=1, cstride=1)


plt.show()