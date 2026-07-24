import pytest
from logging_manager import LoggingManager
from pathlib import Path

def test_syntax_validation():
    valid_code = "print('hello')"
    invalid_code = "print('hello"
    assert LoggingManager.validate_syntax(valid_code) == True
    assert LoggingManager.validate_syntax(invalid_code) == False

def test_backup_creation():
    test_file = Path("test_target.py")
    test_file.write_text("print('test')")
    
    manager = LoggingManager()
    backup = manager.create_backup(test_file)
    
    assert backup.exists()
    assert backup.read_text() == "print('test')"
    
    test_file.unlink()
    backup.unlink()
