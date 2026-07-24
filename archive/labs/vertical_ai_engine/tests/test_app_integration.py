# tests/test_app_integration.py
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import json
import asyncio # For running async functions directly if needed

# Import the Flask app and the components it uses
from app import app, doc_ingestion, entity_analyzer, foia_generator, aura_agent, gemini_service

# Fixture to set up the Flask test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Fixture to mock GeminiService's generate_content
@pytest.fixture
def mock_gemini_generate():
    with patch('modules.services.gemini_service.GeminiService.generate_content', new_callable=AsyncMock) as mock_method:
        mock_method.return_value = "AI analysis: This is a comprehensive AI report."
        yield mock_method

# Fixture to mock DocumentIngestionPipeline's ingest_document
@pytest.fixture
def mock_ingest_document():
    with patch('modules.document_ingestion.DocumentIngestionPipeline.ingest_document') as mock_method:
        mock_method.return_value = {"content": "Mocked document content.", "metadata": {}}
        yield mock_method

# Fixture to mock EntityParsingRedFlagAnalyzer's methods
@pytest.fixture
def mock_entity_analyzer_methods():
    with patch('modules.entity_analyzer.EntityParsingRedFlagAnalyzer.extract_entities_from_content') as mock_extract, \
         patch('modules.entity_analyzer.EntityParsingRedFlagAnalyzer.analyze_entities_for_red_flags') as mock_analyze:
        
        mock_extract.return_value = [("Mock Person", "PERSON"), ("Mock Org", "ORG")]
        mock_analyze.return_value = {
            "red_flags": {"financial_misconduct": ["bribe"]},
            "severity_scores": {"financial_misconduct": 8.5},
            "related_entities": {"bribe": ["Mock Person"]},
            "summary": "Mocked red flag summary: High financial risk."
        }
        yield mock_extract, mock_analyze

# Fixture to mock FOIAGeneratorMicroAgent's generate_foia_request
@pytest.fixture
def mock_foia_generate():
    with patch('modules.foia_generator.FOIAGeneratorMicroAgent.generate_foia_request') as mock_method:
        mock_method.return_value = "Mocked FOIA request letter."
        yield mock_method

# Fixture to mock AuraMicroAgent's generate_insights
@pytest.fixture
def mock_aura_generate():
    with patch('modules.aura_agent.AuraMicroAgent.generate_insights') as mock_method:
        mock_method.return_value = [{"type": "pattern_recognition", "summary": "Mocked Aura insight."}]
        yield mock_method

@pytest.mark.asyncio
async def test_analyze_scenario_basic(client, mock_gemini_generate, mock_ingest_document, 
                                     mock_entity_analyzer_methods, mock_foia_generate, mock_aura_generate):
    """
    Test a basic scenario analysis with text input.
    """
    response = await client.post('/analyze_scenario', json={
        'scenarioText': 'A suspicious transaction occurred.',
        'mode': 'analysis'
    })

    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'aiResponse' in data
    assert 'redFlagReport' in data
    assert 'auraInsights' in data
    assert 'foiaOutput' in data
    assert 'entities' in data

    assert data['aiResponse'] == "AI analysis: This is a comprehensive AI report."
    assert data['redFlagReport'] == "Mocked red flag summary: High financial risk."
    assert data['foiaOutput']['generated'] is False # Not in audit mode
    assert len(data['auraInsights']) > 0
    assert {"name": "Mock Person", "type": "PERSON"} in data['entities'] # Check dict format
    assert {"name": "Mock Org", "type": "ORG"} in data['entities']

    mock_gemini_generate.assert_called_once()
    # ingest_document won't be called if no document_url is provided
    mock_ingest_document.assert_not_called() 
    mock_entity_analyzer_methods[0].assert_called_once() # extract_entities
    mock_entity_analyzer_methods[1].assert_called_once() # analyze_entities
    mock_foia_generate.assert_not_called() # Not in audit mode
    mock_aura_generate.assert_called_once()

@pytest.mark.asyncio
async def test_analyze_scenario_with_document_url(client, mock_gemini_generate, mock_ingest_document, 
                                                 mock_entity_analyzer_methods, mock_foia_generate, mock_aura_generate):
    """
    Test scenario analysis with a document URL.
    """
    response = await client.post('/analyze_scenario', json={
        'scenarioText': 'Another scenario.',
        'documentUrl': 'http://example.com/doc.pdf',
        'mode': 'analysis'
    })

    assert response.status_code == 200
    data = json.loads(response.data)

    mock_ingest_document.assert_called_once_with(url='http://example.com/doc.pdf')
    # Both scenario text and doc content will be passed to entity analyzer
    # The call to extract_entities_from_content will receive a combined string
    # The first argument is the content string
    assert "Another scenario." in mock_entity_analyzer_methods[0].call_args[0][0]
    assert "Mocked document content." in mock_entity_analyzer_methods[0].call_args[0][0]


@pytest.mark.asyncio
async def test_analyze_scenario_audit_mode_foia_generated(client, mock_gemini_generate, mock_ingest_document, 
                                                          mock_entity_analyzer_methods, mock_foia_generate, mock_aura_generate):
    """
    Test audit mode where FOIA request should be generated.
    """
    # Configure mock_entity_analyzer_methods for high financial risk
    mock_entity_analyzer_methods[1].return_value = {
        "red_flags": {"financial_misconduct": ["bribe"]},
        "severity_scores": {"financial_misconduct": 9.0}, # High enough for FOIA
        "related_entities": {"bribe": ["Mock Person"]},
        "summary": "High financial risk detected, initiating audit."
    }

    response = await client.post('/analyze_scenario', json={
        'scenarioText': 'Audit a financial scandal.',
        'mode': 'audit'
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['foiaOutput']['generated'] is True
    assert data['foiaOutput']['letter'] == "Mocked FOIA request letter."
    mock_foia_generate.assert_called_once() # Should be called in audit mode with high risk

@pytest.mark.asyncio
async def test_analyze_scenario_audit_mode_foia_not_generated_low_risk(client, mock_gemini_generate, mock_ingest_document, 
                                                                       mock_entity_analyzer_methods, mock_foia_generate, mock_aura_generate):
    """
    Test audit mode where FOIA request should NOT be generated (low risk).
    """
    # Configure mock_entity_analyzer_methods for low financial risk
    mock_entity_analyzer_methods[1].return_value = {
        "red_flags": {"financial_misconduct": ["minor anomaly"]},
        "severity_scores": {"financial_misconduct": 3.0}, # Low enough to not trigger FOIA
        "related_entities": {"minor anomaly": ["Mock Person"]},
        "summary": "Low financial risk."
    }

    response = await client.post('/analyze_scenario', json={
        'scenarioText': 'Audit a minor issue.',
        'mode': 'audit'
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['foiaOutput']['generated'] is False
    mock_foia_generate.assert_not_called()

@pytest.mark.asyncio
async def test_analyze_scenario_psycho_warfare_mode(client, mock_gemini_generate, mock_ingest_document, 
                                                  mock_entity_analyzer_methods, mock_foia_generate, mock_aura_generate):
    """
    Test psychological warfare mode.
    """
    response = await client.post('/analyze_scenario', json={
        'scenarioText': 'Analyze a target\'s profile.',
        'mode': 'psychoWarfare'
    })

    assert response.status_code == 200
    data = json.loads(response.data)

    # Aura agent should be called with 'psychological_warfare' mode
    mock_aura_generate.assert_called_once()
    # Access the arguments passed to the mock
    call_args, call_kwargs = mock_aura_generate.call_args
    assert call_kwargs['mode'] == 'psychological_warfare'

@pytest.mark.asyncio
async def test_analyze_scenario_no_input(client):
    """Test scenario analysis with no input."""
    response = await client.post('/analyze_scenario', json={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert "Please provide scenario text or a document URL." in data['error']

@pytest.mark.asyncio
async def test_analyze_scenario_gemini_error(client, mock_gemini_generate, mock_ingest_document, mock_entity_analyzer_methods, 
                                            mock_foia_generate, mock_aura_generate):
    """Test error handling when Gemini API call fails."""
    mock_gemini_generate.side_effect = requests.exceptions.RequestException("Gemini API is down")

    response = await client.post('/analyze_scenario', json={
        'scenarioText': 'Test Gemini error.',
        'mode': 'analysis'
    })
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data
    assert "API call or document processing failed: Gemini API is down" in data['error']

@pytest.mark.asyncio
async def test_analyze_scenario_document_ingestion_error(client, mock_gemini_generate, mock_ingest_document, 
                                                         mock_entity_analyzer_methods, mock_foia_generate, mock_aura_generate):
    """Test error handling when document ingestion fails."""
    mock_ingest_document.return_value = {"content": "", "metadata": {"error": "Failed to parse PDF"}}

    response = await client.post('/analyze_scenario', json={
        'scenarioText': 'Some text.',
        'documentUrl': 'http://bad.url/doc.pdf',
        'mode': 'analysis'
    })
    
    assert response.status_code == 200 # Ingestion error doesn't halt entire process, just means doc content is empty
    data = json.loads(response.data)
    assert "Mocked red flag summary: High financial risk." in data['redFlagReport'] # Other parts still proceed
    assert "Mocked Aura insight." in data['auraInsights'][0]['summary']
    assert mock_ingest_document.called
    # Ensure that even if doc ingestion fails, the entity analyzer is still called with available text
    # The first argument to extract_entities_from_content is the content string
    assert mock_entity_analyzer_methods[0].call_args[0][0] == 'Some text.'

