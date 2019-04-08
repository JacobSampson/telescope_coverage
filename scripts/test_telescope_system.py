import unittest
from models.telescope_system import TelescopeSystem
from models.telescope import Telescope

class TestTelescopeSystem(unittest.TestCase):

    def test_poles(self):  
        telescope_system = TelescopeSystem()
        telescope_system.telescopes = [Telescope([0, 0, -telescope_system.RADIUS_EARTH], 30)]
        
        expected = 20000
        telescope_system.create_satellites()
        result = telescope_system.num_in_view

        self.assertEqual(expected, result)

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == "__main__":
    unittest.main()