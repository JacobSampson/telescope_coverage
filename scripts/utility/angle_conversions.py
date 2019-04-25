import numpy as np

RADIUS_EARTH = 6371
DISTANCE_SATELLITES = 35786

# Converts spherical coordinates to cartesian coordinates
def degrees_to_coords(theta=0, phi=0, radius=RADIUS_EARTH):
    rad_theta = np.pi * theta / 180.  
    rad_phi = np.pi * phi / 180.

    x = radius * np.sin(rad_phi) * np.cos(rad_theta)
    y = radius * np.sin(rad_phi) * np.sin(rad_theta)
    z = radius * np.cos(rad_phi)

    return np.array([x, y, z])

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