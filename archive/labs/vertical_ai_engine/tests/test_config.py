# tests/test_config.py
import os
import logging
from config import GEMINI_API_KEY, LOGGING_CONFIG

def test_gemini_api_key_exists():
    """Test that GEMINI_API_KEY is retrieved, even if empty."""
    # This test will pass even if GEMINI_API_KEY is an empty string
    # as it's designed to be provided by the runtime environment.
    assert isinstance(GEMINI_API_KEY, str)

def test_logging_config_format():
    """Test that LOGGING_CONFIG has expected keys and types."""
    assert isinstance(LOGGING_CONFIG, dict)
    assert 'level' in LOGGING_CONFIG
    assert 'format' in LOGGING_CONFIG
    assert 'handlers' in LOGGING_CONFIG
    
    assert isinstance(LOGGING_CONFIG['level'], int)
    assert isinstance(LOGGING_CONFIG['format'], str)
    assert isinstance(LOGGING_CONFIG['handlers'], list)
    assert LOGGING_CONFIG['level'] == logging.INFO

def test_logging_config_handlers_present():
    """Test that at least one file handler and one stream handler are configured."""
    file_handler_present = any(isinstance(h, logging.FileHandler) for h in LOGGING_CONFIG['handlers'])
    stream_handler_present = any(isinstance(h, logging.StreamHandler) for h in LOGGING_CONFIG['handlers'])
    
    assert file_handler_present
    assert stream_handler_present

