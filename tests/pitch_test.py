import unittest
from app.models import Pitch

class PitchTest(unittest.TestCase):
    def setUp(self):
        self.new_pitch = Pitch(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 
            "Business Pitches", 
            "2021-12-13T20:19:00Z", 
            0,
            0, 
        )

    def test_instance(self):
        self.assertTrue(isinstance(self.new_user, Pitch))

if __name__ == "__main__":
    unittest.main()