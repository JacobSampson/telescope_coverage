import unittest
from models.telescope_system import TelescopeSystem
from models.telescope import Telescope
import numpy as np

class TestTelescopeSystem(unittest.TestCase):

    def test_poles(self):  
        telescope_system = TelescopeSystem()

        telescope_system.telescopes = [Telescope([0, 0, -telescope_system.RADIUS_EARTH], 30)]
        telescope_system.create_satellites()
        south = telescope_system.num_in_view

        telescope_system.telescopes = [Telescope([0, 0, telescope_system.RADIUS_EARTH], 30)]
        telescope_system.create_satellites()
        north = telescope_system.num_in_view

        self.assertEqual(south, north)

    def test_mirrored_tilted(self):  
        telescope_system = TelescopeSystem()
        telescope_system.create_satellites()

        y = telescope_system.RADIUS_EARTH / 2
        z = np.sqrt(3) / y

        telescope_system.telescopes = [Telescope([0, y - 1, z], angle=80)]
        percent_top = telescope_system.update_satellites()

        telescope_system.telescopes = [Telescope([0, -y, -z], angle=80)]
        percent_bottom = telescope_system.update_satellites()

        self.assertEqual(percent_top - 1, percent_bottom)

if __name__ == "__main__":
    unittest.main()