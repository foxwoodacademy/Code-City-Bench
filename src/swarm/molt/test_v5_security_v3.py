import unittest
import os
import shutil
from pathlib import Path
from logging_manager import LoggingManager
from model_switcher import ModelSwitcher

class TestMoltV5Core(unittest.TestCase):
    def setUp(self):
        self.test_dir = "/storage/emulated/0/RootBase/molt_v5_test_log"
        self.logger = LoggingManager(log_dir=self.test_dir)
        # Using Path object to satisfy logging_manager requirements
        self.target_file = Path("/storage/emulated/0/RootBase/test_target.py")
        
        # Ensure parent directories exist, then create test target
        os.makedirs(os.path.dirname(str(self.target_file)), exist_ok=True)
        with open(self.target_file, "w") as f:
            f.write("print('Hello World')\n")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(str(self.target_file)):
            os.remove(str(self.target_file))
        bak_file = str(self.target_file) + ".bak"
        if os.path.exists(bak_file):
            os.remove(bak_file)

    def test_ast_validation_valid(self):
        valid_code = "def test_func():\n    return True"
        self.assertTrue(self.logger.validate_syntax(valid_code))

    def test_ast_validation_invalid(self):
        invalid_code = "def test_func([\n    return True"
        self.assertFalse(self.logger.validate_syntax(invalid_code))

    def test_backup_creation(self):
        bak_path = self.logger.create_backup(self.target_file)
        self.assertIsNotNone(bak_path)
        if bak_path:
            self.assertTrue(os.path.exists(str(bak_path)))

if __name__ == "__main__":
    unittest.main(verbosity=2)
