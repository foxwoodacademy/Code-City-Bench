"""
Kimi-Code: Progression Engine Tests
"""
import unittest
import tempfile
import shutil
from core.state_engine import StateEngine
from core.progression_engine import ProgressionEngine

class TestProgressionEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state = StateEngine(self.temp_dir)
        self.progression = ProgressionEngine(self.state)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_xp_calculation(self):
        """Test XP reward calculation."""
        xp = self.progression.calculate_xp_reward(
            complexity=5, success=True, time_taken=200, 
            hints_used=1, hat_bonus=True
        )
        self.assertGreater(xp, 0)
        # Base: 5*25=125, time bonus ~1.5, hint penalty ~0.85, hat bonus 1.3
        self.assertGreater(xp, 100)

    def test_level_up(self):
        """Test level progression."""
        initial_level = self.state.state["global_level"]
        self.progression.add_xp(150)  # Should hit level 2
        self.assertEqual(self.state.state["global_level"], 2)

    def test_difficulty_recommendation(self):
        """Test adaptive difficulty."""
        tier, complexity = self.progression.get_recommended_difficulty("python")
        self.assertIn(tier, ["novice", "apprentice"])
        self.assertGreaterEqual(complexity, 1)
        self.assertLessEqual(complexity, 15)

    def test_track_unlock(self):
        """Test track progression unlocks."""
        # Set up language state
        lang_state = self.state.get_language_state("python")
        lang_state["current_track"] = "basics"

        # Simulate completing enough challenges
        for _ in range(10):
            self.state.log_challenge({
                "type": "challenge",
                "language": "python",
                "track": "basics",
                "success": True,
                "time_taken": 60,
                "complexity": 3
            })

        lang_state["mastery_score"] = 0.8
        unlocked = self.progression.check_track_unlock("python", "basics")
        self.assertTrue(unlocked)
        self.assertIn("data_structures", lang_state["tracks_unlocked"])

    def test_progress_summary(self):
        """Test progress summary generation."""
        summary = self.progression.get_progress_summary()
        self.assertIn("global", summary)
        self.assertIn("difficulty_recommendation", summary)
        self.assertIn("skills", summary)
        self.assertIn("hats", summary)

if __name__ == '__main__':
    unittest.main()
