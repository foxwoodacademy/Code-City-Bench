# tests/test_document_ingestion.py
import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
import requests.exceptions
from modules.document_ingestion import DocumentIngestionPipeline

@pytest.fixture
def doc_pipeline():
    """Provides a DocumentIngestionPipeline instance with a temporary storage directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield DocumentIngestionPipeline(storage_dir=tmpdir)

@pytest.fixture
def mock_requests_get():
    """Mocks requests.get for URL downloading."""
    with patch('requests.get') as mock_get:
        yield mock_get

@pytest.fixture
def mock_tika_parser_from_file():
    """Mocks tika.parser.from_file."""
    with patch('tika.parser.from_file') as mock_from_file:
        yield mock_from_file

def test_init(doc_pipeline):
    """Test that the DocumentIngestionPipeline initializes correctly."""
    assert os.path.isdir(doc_pipeline.storage_dir)

def test_download_from_url_success(doc_pipeline, mock_requests_get):
    """Test successful document download from URL."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.iter_content.return_value = [b"test content"]
    mock_requests_get.return_value = mock_response

    temp_filepath = os.path.join(doc_pipeline.storage_dir, "test_file.txt")
    result = doc_pipeline._download_from_url("http://example.com/doc.txt", temp_filepath)

    assert result is True
    assert os.path.exists(temp_filepath)
    with open(temp_filepath, 'rb') as f:
        assert f.read() == b"test content"
    mock_requests_get.assert_called_once_with("http://example.com/doc.txt", stream=True, timeout=30)

def test_download_from_url_failure(doc_pipeline, mock_requests_get):
    """Test failed document download from URL due to request error."""
    mock_requests_get.side_effect = requests.exceptions.RequestException("Download failed")

    temp_filepath = os.path.join(doc_pipeline.storage_dir, "test_file.txt")
    result = doc_pipeline._download_from_url("http://example.com/doc.txt", temp_filepath)

    assert result is False
    assert not os.path.exists(temp_filepath)
    mock_requests_get.assert_called_once()

def test_parse_document_content_success(doc_pipeline, mock_tika_parser_from_file):
    """Test successful parsing of document content with Tika."""
    mock_tika_parser_from_file.return_value = {
        "content": "This is the document content.",
        "metadata": {"title": "Test Doc"}
    }
    
    dummy_filepath = os.path.join(doc_pipeline.storage_dir, "dummy.pdf")
    # Create a dummy file for Tika to "read"
    with open(dummy_filepath, 'w') as f:
        f.write("dummy content") 

    result = doc_pipeline._parse_document_content(dummy_filepath)

    assert result["content"] == "This is the document content."
    assert result["metadata"]["title"] == "Test Doc"
    mock_tika_parser_from_file.assert_called_once_with(dummy_filepath)
    os.remove(dummy_filepath) # Clean up dummy file

def test_parse_document_content_empty(doc_pipeline, mock_tika_parser_from_file):
    """Test parsing of an empty document or Tika returning None."""
    mock_tika_parser_from_file.return_value = None
    
    dummy_filepath = os.path.join(doc_pipeline.storage_dir, "empty.pdf")
    with open(dummy_filepath, 'w') as f:
        f.write("")

    result = doc_pipeline._parse_document_content(dummy_filepath)
    assert result["content"] == ""
    assert result["metadata"] == {}
    mock_tika_parser_from_file.assert_called_once_with(dummy_filepath)
    os.remove(dummy_filepath) # Clean up dummy file

def test_parse_document_content_tika_error(doc_pipeline, mock_tika_parser_from_file):
    """Test Tika parsing error handling."""
    mock_tika_parser_from_file.side_effect = Exception("Tika parsing error")

    dummy_filepath = os.path.join(doc_pipeline.storage_dir, "error.pdf")
    with open(dummy_filepath, 'w') as f:
        f.write("corrupt content")

    result = doc_pipeline._parse_document_content(dummy_filepath)
    assert result["content"] == ""
    assert "Tika parsing error" in result["metadata"]["error"]
    mock_tika_parser_from_file.assert_called_once_with(dummy_filepath)
    os.remove(dummy_filepath) # Clean up dummy file

def test_ingest_document_from_url(doc_pipeline, mock_requests_get, mock_tika_parser_from_file):
    """Integration test for ingesting document from URL."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.iter_content.return_value = [b"url content"]
    mock_requests_get.return_value = mock_response

    mock_tika_parser_from_file.return_value = {
        "content": "Parsed URL content.",
        "metadata": {"source": "URL"}
    }

    url = "http://example.com/report.pdf"
    result = doc_pipeline.ingest_document(url=url)

    assert result["content"] == "Parsed URL content."
    assert result["metadata"]["source"] == "URL"
    mock_requests_get.assert_called_once()
    mock_tika_parser_from_file.assert_called_once()
    # Ensure temporary file is cleaned up
    assert not any(f.startswith("tmp") for f in os.listdir(doc_pipeline.storage_dir))

def test_ingest_document_from_file_path(doc_pipeline, mock_tika_parser_from_file):
    """Integration test for ingesting document from file path."""
    mock_tika_parser_from_file.return_value = {
        "content": "Parsed file path content.",
        "metadata": {"source": "local_file"}
    }
    
    local_file_path = os.path.join(doc_pipeline.storage_dir, "local_doc.txt")
    with open(local_file_path, 'w') as f:
        f.write("local file content")

    result = doc_pipeline.ingest_document(file_path=local_file_path)

    assert result["content"] == "Parsed file path content."
    assert result["metadata"]["source"] == "local_file"
    mock_tika_parser_from_file.assert_called_once_with(local_file_path)
    # Local file should still exist as it wasn't a temp file created by pipeline
    assert os.path.exists(local_file_path)
    os.remove(local_file_path) # Clean up local file

def test_ingest_document_from_file_content(doc_pipeline, mock_tika_parser_from_file):
    """Integration test for ingesting document from raw content."""
    mock_tika_parser_from_file.return_value = {
        "content": "Parsed raw content.",
        "metadata": {"source": "raw_content"}
    }

    raw_content = b"This is raw byte content."
    result = doc_pipeline.ingest_document(file_content=raw_content)

    assert result["content"] == "Parsed raw content."
    assert result["metadata"]["source"] == "raw_content"
    mock_tika_parser_from_file.assert_called_once()
    # Ensure temporary file is cleaned up
    assert not any(f.startswith("tmp") for f in os.listdir(doc_pipeline.storage_dir))

def test_ingest_document_invalid_input(doc_pipeline):
    """Test ingesting document with invalid input (multiple sources)."""
    result = doc_pipeline.ingest_document(file_path="a.txt", url="http://b.com")
    assert "Invalid input" in result["metadata"]["error"]
    result = doc_pipeline.ingest_document()
    assert "Invalid input" in result["metadata"]["error"]

def test_ingest_document_file_not_found(doc_pipeline):
    """Test ingesting document from non-existent file path."""
    result = doc_pipeline.ingest_document(file_path="/non/existent/path/file.pdf")
    assert "File not found" in result["metadata"]["error"]

def test_get_supported_extensions(doc_pipeline):
    """Test that supported extensions list is returned."""
    extensions = doc_pipeline.get_supported_extensions()
    assert isinstance(extensions, list)
    assert ".pdf" in extensions
    assert ".txt" in extensions
    assert ".docx" in extensions

