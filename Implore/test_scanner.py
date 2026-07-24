import unittest
from implore_scanner_profile import ProfileBuilder
from pathlib import Path

class TestScanner(unittest.TestCase):
    def test_profile_builder(self):
        builder = ProfileBuilder()
        builder.update_with_file(Path("test.py"))
        profile = builder.get_profile()
        self.assertEqual(profile["languages"][".py"], 1)

if __name__ == "__main__":
    unittest.main()
