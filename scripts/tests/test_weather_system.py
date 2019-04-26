import unittest
import numpy as np

from models.weather_system import (coords_to_spherical, WeatherSystem)

class TestWeatherSystem(unittest.TestCase):

    # Test coords_to_spherical
    
    def test_coords_to_spherical_with_first_octant(self):
        coords = np.array([1, 3, 5])

        expected_theta = 1.2490
        expected_phi = 0.5639
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)
    
    def test_coords_to_spherical_with_second_octant(self):
        coords = np.array([-1, 3, 5])

        expected_theta = 1.8925
        expected_phi = 0.5639
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)

    def test_coords_to_spherical_with_third_octant(self):
        coords = np.array([-1, -3, 5])

        expected_theta = 4.3906
        expected_phi = 0.5639
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)
    
    def test_coords_to_spherical_with_fourth_octant(self):
        coords = np.array([1, -3, 5])

        expected_theta = 5.0341
        expected_phi = 0.5639
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)

    def test_coords_to_spherical_with_fifth_octant(self):
        coords = np.array([1, 3, -5])

        expected_theta = 1.2490
        expected_phi = 2.5777
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)
    
    def test_coords_to_spherical_with_sixth_octant(self):
        coords = np.array([-1, 3, -5])

        expected_theta = 1.8925
        expected_phi = 2.5777
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)

    def test_coords_to_spherical_with_seventh_octant(self):
        coords = np.array([-1, -3, -5])

        expected_theta = 4.3906
        expected_phi = 2.5777
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)

    def test_coords_to_spherical_with_eighth_octant(self):
        coords = np.array([1, -3, -5])

        expected_theta = 5.0341
        expected_phi = 2.5777
        epsilon = 4

        spherical_coords = coords_to_spherical(coords=coords)

        theta = spherical_coords[0]
        phi = spherical_coords[1]

        self.assertAlmostEqual(expected_theta, theta, epsilon)
        self.assertAlmostEqual(expected_phi, phi, epsilon)

    # Test get_closest_index

    def test_get_closest_index_with_middling_degree(self):
        angle_density = 11
        weather_system = WeatherSystem(theta_density=angle_density, phi_density=angle_density)

        angle = 2.145
        expected_index = 4

        index = weather_system.get_closest_index(data_range=2 * np.pi, density=angle_density, value=angle)

        self.assertEquals(expected_index, index)

    def test_get_closest_index_with_beginning_degree(self):
        angle_density = 11
        weather_system = WeatherSystem(theta_density=angle_density, phi_density=angle_density)

        angle = 0.002
        expected_index = 0

        index = weather_system.get_closest_index(data_range=2 * np.pi, density=angle_density, value=angle)

        self.assertEquals(expected_index, index)

    def test_get_closest_index_with_ending_degree(self):
        angle_density = 11
        weather_system = WeatherSystem(theta_density=angle_density, phi_density=angle_density)

        angle = 2 * np.pi - 0.002
        expected_index = 0

        index = weather_system.get_closest_index(data_range=2 * np.pi, density=angle_density, value=angle)

        self.assertEquals(expected_index, index)

    # Test blocks_line

    def test_blocks_line_with_actual_telescope(self):
        angle_density = 50

        # Setup test weather system
        altitude = 8000
        thetas = np.ones(shape=(angle_density, angle_density), dtype=np.bool)
        thetas.fill(False)
        thetas[24][25] = True
        altitude_weather = {
            altitude: thetas
        }

        weather_system = WeatherSystem(altitude_weather=altitude_weather, theta_density=angle_density, phi_density=angle_density)

        origin = np.array([-6346.756421542511, 555.2692370453332, 3.9011123786838936e-13])
        point1 = np.array([-12000, 555, 0])
        point2 = np.array([-12000, 555, 100])
        point3 = np.array([-12000, 555, 2000])

        self.assertTrue(weather_system.blocks_line(origin=origin, point=point1))
        self.assertTrue(weather_system.blocks_line(origin=origin, point=point2))
        self.assertFalse(weather_system.blocks_line(origin=origin, point=point3))

if __name__ == "__main__":
    unittest.main()