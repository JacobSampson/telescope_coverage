import unittest
import numpy as np

from models.telescope import Telescope

class TestTelescope(unittest.TestCase):

    # Test can_view

    def test_can_view_with_zero_components(self):
        tel_x = Telescope(origin=np.array([4, 0, 0]), angle=90)
        point_x = np.array([8, 0, 0])
        tel_y = Telescope(origin=np.array([0, 2, 0]), angle=90)
        point_y = np.array([0, 1, 0])
        tel_z = Telescope(origin=np.array([0, 0, 8]), angle=90)
        point_z = np.array([0, 0, -3])

        result_x = tel_x.can_view(point=point_x)
        result_y = tel_y.can_view(point=point_y)
        result_z = tel_z.can_view(point=point_z)

        self.assertTrue(result_x)
        self.assertFalse(result_y)
        self.assertFalse(result_z)

    def test_can_view_with_slightly_off(self):
        tel = Telescope(origin=np.array([3, 2, 4]), angle=90)
        point = np.array([6.1, 4.1, 8.1])

        result = tel.can_view(point=point)

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()