"""
Kimi-Code: Six Hats Engine Tests
"""
import unittest
from core.six_hats import SixHatsEngine, HatPrompt

class TestSixHatsEngine(unittest.TestCase):
    def setUp(self):
        self.hats = SixHatsEngine()

    def test_all_hats_exist(self):
        """Test all 6 hats are defined."""
        all_hats = self.hats.get_all_hats()
        self.assertEqual(len(all_hats), 6)
        self.assertIn("white", all_hats)
        self.assertIn("red", all_hats)
        self.assertIn("black", all_hats)
        self.assertIn("yellow", all_hats)
        self.assertIn("green", all_hats)
        self.assertIn("blue", all_hats)

    def test_hat_structure(self):
        """Test hat configuration structure."""
        white = self.hats.get_hat("white")
        self.assertIsInstance(white, HatPrompt)
        self.assertEqual(white.hat, "white")
        self.assertIsNotNone(white.color)
        self.assertIsNotNone(white.emoji)
        self.assertGreater(len(white.questions), 0)
        self.assertIsNotNone(white.analysis_template)

    def test_sequence_generation(self):
        """Test different sequence modes."""
        standard = self.hats.generate_sequence("standard")
        self.assertEqual(len(standard), 6)
        self.assertEqual(standard[-1], "blue")  # Always ends with blue

        quick = self.hats.generate_sequence("quick")
        self.assertEqual(len(quick), 4)

        deep = self.hats.generate_sequence("deep")
        self.assertEqual(len(deep), 7)
        self.assertEqual(deep[0], "blue")  # Starts with blue
        self.assertEqual(deep[-1], "blue")  # Ends with blue

    def test_prompt_generation(self):
        """Test prompt generation for hats."""
        code = "def hello(): print('world')"
        prompt = self.hats.generate_prompt_for_hat("white", code)
        self.assertIn("White Hat", prompt)
        self.assertIn(code, prompt)
        self.assertIn("questions", prompt.lower())

    def test_full_analysis_prompt(self):
        """Test full analysis prompt."""
        code = "def add(a, b): return a + b"
        prompt = self.hats.generate_full_analysis_prompt(code)
        self.assertIn("Six Thinking Hats", prompt)
        self.assertIn("white", prompt.lower())
        self.assertIn("blue", prompt.lower())

    def test_challenge_generation(self):
        """Test hat-specific challenge generation."""
        challenge = self.hats.get_challenge_for_hat("black", 5, "python")
        self.assertEqual(challenge["hat"], "black")
        self.assertEqual(challenge["difficulty"], 5)
        self.assertEqual(challenge["language"], "python")
        self.assertIn("success_criteria", challenge)

    def test_hat_balance_report(self):
        """Test hat balance analysis."""
        hat_stats = {
            "white": {"level": 5, "xp": 100, "challenges": 10},
            "red": {"level": 2, "xp": 30, "challenges": 3},
            "black": {"level": 6, "xp": 150, "challenges": 15},
            "yellow": {"level": 3, "xp": 60, "challenges": 6},
            "green": {"level": 2, "xp": 40, "challenges": 4},
            "blue": {"level": 4, "xp": 80, "challenges": 8}
        }

        report = self.hats.get_hat_balance_report(hat_stats)
        self.assertIn("weakest_hats", report)
        self.assertIn("strongest_hats", report)
        self.assertIn("balance_score", report)
        self.assertIn("red", report["weakest_hats"])
        self.assertIn("black", report["strongest_hats"])

if __name__ == '__main__':
    unittest.main()
