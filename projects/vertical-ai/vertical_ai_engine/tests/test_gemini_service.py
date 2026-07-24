# tests/test_gemini_service.py
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import requests.exceptions
import google.generativeai as genai # Import genai to mock its APIError
from modules.services.gemini_service import GeminiService

# Fixture for GeminiService
@pytest.fixture
def gemini_service_instance():
    """Provides a GeminiService instance with a mock API key."""
    return GeminiService(api_key="TEST_API_KEY")

@pytest.mark.asyncio
async def test_generate_content_success(gemini_service_instance):
    """Test successful content generation from Gemini API."""
    mock_response = MagicMock() # Use MagicMock for simpler mock object
    mock_response.text = "This is a generated response."
    mock_response.parts = [MagicMock(text="This is a generated response.")] # Ensure parts is also handled
    
    # Mock the synchronous model.generate_content call that asyncio.to_thread will use
    with patch('modules.services.gemini_service.genai.GenerativeModel') as MockGenerativeModel:
        mock_model_instance = MockGenerativeModel.return_value
        # Configure the return value of the synchronous call
        mock_model_instance.generate_content.return_value = mock_response

        prompt = "Tell me a story."
        result = await gemini_service_instance.generate_content(prompt)
        assert result == "This is a generated response."
        mock_model_instance.generate_content.assert_called_once_with(prompt)

@pytest.mark.asyncio
async def test_generate_content_api_error(gemini_service_instance):
    """Test handling of Gemini API errors."""
    with patch('modules.services.gemini_service.genai.GenerativeModel') as MockGenerativeModel:
        mock_model_instance = MockGenerativeModel.return_value
        # Simulate an API error
        mock_model_instance.generate_content.side_effect = genai.APIError("API rate limit exceeded")

        prompt = "Invalid request."
        with pytest.raises(requests.exceptions.RequestException) as excinfo:
            await gemini_service_instance.generate_content(prompt)
        assert "API rate limit exceeded" in str(excinfo.value)
        mock_model_instance.generate_content.assert_called_once_with(prompt)

@pytest.mark.asyncio
async def test_generate_content_unexpected_error(gemini_service_instance):
    """Test handling of unexpected errors during content generation."""
    with patch('modules.services.gemini_service.genai.GenerativeModel') as MockGenerativeModel:
        mock_model_instance = MockGenerativeModel.return_value
        mock_model_instance.generate_content.side_effect = Exception("Network issue")

        prompt = "Error test."
        with pytest.raises(Exception) as excinfo:
            await gemini_service_instance.generate_content(prompt)
        assert "Network issue" in str(excinfo.value)
        mock_model_instance.generate_content.assert_called_once_with(prompt)

@pytest.mark.asyncio
async def test_generate_content_empty_response(gemini_service_instance):
    """Test handling of empty or malformed API responses."""
    mock_response = MagicMock()
    mock_response.text = "" # Simulate empty text
    mock_response.parts = [] # Simulate no parts

    with patch('modules.services.gemini_service.genai.GenerativeModel') as MockGenerativeModel:
        mock_model_instance = MockGenerativeModel.return_value
        mock_model_instance.generate_content.return_value = mock_response

        prompt = "Generate nothing."
        result = await gemini_service_instance.generate_content(prompt)
        assert result == "" # Expect empty string or a default error message
        mock_model_instance.generate_content.assert_called_once_with(prompt)

@pytest.mark.asyncio
async def test_generate_content_with_parts_response(gemini_service_instance):
    """Test content generation when response has parts."""
    mock_part1 = MagicMock(text="First part.")
    mock_part2 = MagicMock(text="Second part.")

    mock_response = MagicMock()
    mock_response.parts = [mock_part1, mock_part2]
    # Ensure .text is not directly accessed if .parts exist and are prioritized
    if hasattr(mock_response, 'text'):
        del mock_response.text 

    with patch('modules.services.gemini_service.genai.GenerativeModel') as MockGenerativeModel:
        mock_model_instance = MockGenerativeModel.return_value
        mock_model_instance.generate_content.return_value = mock_response

        prompt = "Generate in parts."
        result = await gemini_service_instance.generate_content(prompt)
        assert result == "First part.Second part."
        mock_model_instance.generate_content.assert_called_once_with(prompt)

