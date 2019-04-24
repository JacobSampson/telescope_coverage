import unittest
import numpy as np

from models.weather_system import coords_to_spherical

class TestWeatherSystem(unittest.TestCase):
    def test_first_octant(self):
        coords = np.array([1, 3, 5])

        expected_theta = 1.2490
        expected_phi = 0.5639
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)
    
    def test_second_octant(self):
        coords = np.array([-1, 3, 5])

        expected_theta = 1.8925
        expected_phi = 0.5639
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)

    def test_third_octant(self):
        coords = np.array([-1, -3, 5])

        expected_theta = 4.3906
        expected_phi = 0.5639
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)
    
    def test_fourth_octant(self):
        coords = np.array([1, -3, 5])

        expected_theta = 5.0341
        expected_phi = 0.5639
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)

    def test_fifth_octant(self):
        coords = np.array([1, 3, -5])

        expected_theta = 1.2490
        expected_phi = 2.5777
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)
    
    def test_sixth_octant(self):
        coords = np.array([-1, 3, -5])

        expected_theta = 1.8925
        expected_phi = 2.5777
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)

    def test_seventh_octant(self):
        coords = np.array([-1, -3, -5])

        expected_theta = 4.3906
        expected_phi = 2.5777
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)

    def test_eight_octant(self):
        coords = np.array([1, -3, -5])

        expected_theta = 5.0341
        expected_phi = 2.5777
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)

if __name__ == "__main__":
    unittest.main()