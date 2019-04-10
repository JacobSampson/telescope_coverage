import unittest
import numpy as np

from models.telescope import Telescope
from models.telescope_system import (TelescopeSystem, convert_long_lat, RADIUS_EARTH)

class TestTelescopeSystem(unittest.TestCase):

    def test_poles(self):
        telescope_system = TelescopeSystem()

        telescope_system.telescopes = [Telescope([0, 0, -RADIUS_EARTH], 30)]
        telescope_system.create_satellites()
        south = telescope_system.num_in_view

        telescope_system.telescopes = [Telescope([0, 0, RADIUS_EARTH], 30)]
        telescope_system.create_satellites()
        north = telescope_system.num_in_view

        self.assertEqual(south, north)

    def test_mirrored_tilted_explicitly_defined(self):
        telescope_system = TelescopeSystem()
        telescope_system.create_satellites()

        y = RADIUS_EARTH / 2
        z = np.sqrt(3) / y

        telescope_system.telescopes = [Telescope([0, y - 1, z], angle=80)]
        percent_top = telescope_system.update_satellites()

        telescope_system.telescopes = [Telescope([0, -y, -z], angle=80)]
        percent_bottom = telescope_system.update_satellites()

        self.assertEqual(percent_top, percent_bottom)

    def test_zero_scope(self):
        telescope_system = TelescopeSystem()
        telescope_system.create_satellites()

        expected = 0

        telescope_system.telescopes = [Telescope([0, 0, RADIUS_EARTH], angle=0)]
        percent_visible = telescope_system.update_satellites()

        self.assertEqual(expected, percent_visible)

    def test_mirrored_tilted_angularly_defined(self):
        telescope_system = TelescopeSystem()
        telescope_system.create_satellites()

        point1 = convert_long_lat(long=0, lat=90)
        point2 = convert_long_lat(long=180, lat=90)

        telescope_system.telescopes = [Telescope(point1, angle=60)]
        percent_top = telescope_system.update_satellites()

        telescope_system.telescopes = [Telescope(point2, angle=60)]
        percent_bottom = telescope_system.update_satellites()

        self.assertEqual(percent_top, percent_bottom)

if __name__ == "__main__":
    unittest.main()