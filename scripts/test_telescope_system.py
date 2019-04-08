import unittest
from models.telescope_system import TelescopeSystem
from models.telescope import Telescope
import numpy as np

class TestTelescopeSystem(unittest.TestCase):

    def test_poles(self):  
        telescope_system = TelescopeSystem()

        telescope_system.telescopes = [Telescope([0, 0, -telescope_system.RADIUS_EARTH], np.pi / 6)]
        telescope_system.create_satellites()
        south = telescope_system.num_in_view

        telescope_system.telescopes = [Telescope([0, 0, telescope_system.RADIUS_EARTH], np.pi / 6)]
        telescope_system.create_satellites()
        north = telescope_system.num_in_view

        self.assertEqual(south, north)

    def test_mirrored_tilted(self):  
        telescope_system = TelescopeSystem()

        telescope_system.telescopes = [Telescope([0, 0, -telescope_system.RADIUS_EARTH], np.pi / 6)]
        telescope_system.create_satellites()
        south = telescope_system.num_in_view

        telescope_system.telescopes = [Telescope([0, 0, telescope_system.RADIUS_EARTH], np.pi / 6)]
        telescope_system.create_satellites()
        north = telescope_system.num_in_view

        self.assertEqual(south, north)

if __name__ == "__main__":
    unittest.main()