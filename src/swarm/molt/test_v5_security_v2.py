import unittest
import os
import shutil
from logging_manager import LoggingManager
from model_switcher import ModelSwitcher

class TestMoltV5Core(unittest.TestCase):
    def setUp(self):
        self.test_dir = "/storage/emulated/0/RootBase/molt_v5_test_log"
        self.logger = LoggingManager(log_dir=self.test_dir)
        from pathlib import Path
        self.target_file = Path("/storage/emulated/0/RootBase/test_target.py"
        with open(self.target_file, "w") as f:
            f.write("print('Hello World')\n")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.target_file):
            os.remove(self.target_file)
        if os.path.exists(self.target_file + ".bak"):
            os.remove(self.target_file + ".bak")

    def test_ast_validation_valid(self):
        valid_code = "def test_func():\n    return True"
        self.assertTrue(self.logger.validate_syntax(valid_code))

    def test_ast_validation_invalid(self):
        invalid_code = "def test_func([\n    return True"
        self.assertFalse(self.logger.validate_syntax(invalid_code))

    def test_backup_creation(self):
        bak_path = self.logger.create_backup(self.target_file)
        self.assertTrue(os.path.exists(bak_path))

if __name__ == "__main__":
    unittest.main(verbosity=2)
