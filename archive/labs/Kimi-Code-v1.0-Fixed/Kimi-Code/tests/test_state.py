"""
Kimi-Code: State Engine Tests
"""
import unittest
import os
import tempfile
import json
from core.state_engine import StateEngine

class TestStateEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state = StateEngine(self.temp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_initial_state(self):
        """Test fresh user state initialization."""
        self.assertEqual(self.state.state["global_level"], 1)
        self.assertEqual(self.state.state["global_xp"], 0)
        self.assertEqual(self.state.state["total_challenges_completed"], 0)
        self.assertIn("skill_tree", self.state.state)
        self.assertIn("hats_mastery", self.state.state)

    def test_language_state_creation(self):
        """Test language state initialization."""
        lang_state = self.state.get_language_state("python")
        self.assertEqual(lang_state["level"], 1)
        self.assertEqual(lang_state["xp"], 0)
        self.assertIn("basics", lang_state["tracks_unlocked"])

    def test_skill_update(self):
        """Test skill progression."""
        self.state.update_skill("problem_solving", 10)
        self.assertEqual(self.state.state["skill_tree"]["problem_solving"], 11)

        # Test cap at 100
        self.state.update_skill("problem_solving", 200)
        self.assertEqual(self.state.state["skill_tree"]["problem_solving"], 100)

    def test_hat_mastery_update(self):
        """Test hat mastery progression."""
        self.state.update_hat_mastery("white", True, 120, 5)
        self.assertGreater(self.state.state["hats_mastery"]["white"]["xp"], 0)
        self.assertEqual(self.state.state["hats_mastery"]["white"]["challenges"], 1)

    def test_challenge_logging(self):
        """Test challenge history logging."""
        self.state.log_challenge({
            "type": "test",
            "language": "python",
            "success": True,
            "time_taken": 60,
            "complexity": 3
        })

        self.assertEqual(self.state.state["total_challenges_completed"], 1)
        self.assertEqual(self.state.state["total_time_spent_minutes"], 60)

    def test_persistence(self):
        """Test state saves and loads correctly."""
        self.state.state["global_xp"] = 500
        self.state.save()

        # Create new instance with same directory
        new_state = StateEngine(self.temp_dir)
        self.assertEqual(new_state.state["global_xp"], 500)

    def test_dashboard_data(self):
        """Test dashboard data generation."""
        data = self.state.get_dashboard_data()
        self.assertIn("global_level", data)
        self.assertIn("skill_tree", data)
        self.assertIn("hats_mastery", data)
        self.assertIn("difficulty_modifier", data)

if __name__ == '__main__':
    unittest.main()
