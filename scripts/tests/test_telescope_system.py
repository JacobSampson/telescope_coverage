import unittest
import numpy as np

from models.telescope import Telescope
from models.telescope_system import TelescopeSystem
from utility.angle_conversions import (spherical_to_coords, RADIUS_EARTH)

class TestTelescopeSystem(unittest.TestCase):

    # Test create_satellites
    def test_update_satellites_create_satellites_with_poles_for_equality(self):
        telescope_system = TelescopeSystem()

        telescope_system.telescopes = [Telescope(origin=[0, 0, -RADIUS_EARTH], angle=180)]
        telescope_system.create_satellites()
        south = telescope_system.num_in_view

        telescope_system.telescopes = [Telescope(origin=[0, 0, RADIUS_EARTH], angle=180)]
        telescope_system.create_satellites()
        north = telescope_system.num_in_view

        self.assertEqual(south, north)

    def test_update_satellites_with_poles_for_non_visibility(self):
        telescope_system = TelescopeSystem(satellite_angle=10)
        expected = 0

        telescope_system.telescopes = [Telescope(origin=[0, 0, -RADIUS_EARTH], angle=10)]
        telescope_system.create_satellites()
        result = telescope_system.num_in_view

        self.assertEqual(expected, result)

    def test_update_satellites_with_mirrored_tilted_explicitly_defined(self):
        telescope_system = TelescopeSystem()
        telescope_system.create_satellites()

        y = RADIUS_EARTH / 2
        z = np.sqrt(3) / y

        telescope_system.telescopes = [Telescope(origin=[0, y - 1, z], angle=80)]
        percent_top = telescope_system.update_satellites()

        telescope_system.telescopes = [Telescope(origin=[0, -y, -z], angle=80)]
        percent_bottom = telescope_system.update_satellites()

        self.assertEqual(percent_top, percent_bottom)

    def test_update_satellites_with_zero_scope(self):
        telescope_system = TelescopeSystem()
        telescope_system.create_satellites()

        expected = 0

        telescope_system.telescopes = [Telescope(origin=[0, 0, RADIUS_EARTH], angle=0)]
        percent_visible = telescope_system.update_satellites()

        self.assertEqual(expected, percent_visible)

    def test_update_satellites_with_mirrored_tilted_angularly_defined(self):
        telescope_system = TelescopeSystem(theta_density=1000, phi_density=100)
        telescope_system.create_satellites()

        point1 = spherical_to_coords(theta=0, phi=100)
        point2 = spherical_to_coords(theta=180, phi=80)

        telescope_system.telescopes = [Telescope(origin=point1, angle=60)]
        percent_top = telescope_system.update_satellites()

        telescope_system.telescopes = [Telescope(origin=point2, angle=60)]
        percent_bottom = telescope_system.update_satellites()

        diff = percent_top - percent_bottom

        self.assertLessEqual(diff, 0.01)

if __name__ == "__main__":
    unittest.main()