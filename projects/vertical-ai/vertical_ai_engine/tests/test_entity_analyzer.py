# tests/test_entity_analyzer.py
import pytest
from unittest.mock import patch, MagicMock
import re
from modules.entity_analyzer import EntityParsingRedFlagAnalyzer

@pytest.fixture
def entity_analyzer_instance():
    """Provides an EntityParsingRedFlagAnalyzer instance, mocking spaCy loading."""
    # Mock spaCy load to prevent actual model loading during tests
    with patch('modules.entity_analyzer.spacy.load', return_value=MagicMock()) as mock_spacy_load:
        analyzer = EntityParsingRedFlagAnalyzer()
        yield analyzer
        mock_spacy_load.assert_called_once() # Ensure spacy.load was attempted

@pytest.fixture
def entity_analyzer_no_spacy():
    """Provides an EntityParsingRedFlagAnalyzer instance with spaCy loading failed."""
    with patch('modules.entity_analyzer.spacy.load', side_effect=Exception("SpaCy load error")):
        analyzer = EntityParsingRedFlagAnalyzer()
        yield analyzer

def test_init_spacy_success(entity_analyzer_instance):
    """Test that spaCy model loads successfully."""
    assert entity_analyzer_instance.nlp is not None

def test_init_spacy_failure(entity_analyzer_no_spacy):
    """Test that spaCy model failure is handled."""
    assert entity_analyzer_no_spacy.nlp is None

def test_initialize_red_flag_rules():
    """Test that red flag rules are initialized with compiled regex."""
    analyzer = EntityParsingRedFlagAnalyzer() # This will attempt to load spaCy
    rules = analyzer.red_flag_rules
    assert isinstance(rules, dict)
    assert "financial_misconduct" in rules
    assert isinstance(rules["financial_misconduct"][0], re.Pattern)

def test_extract_entities_from_content_with_spacy(entity_analyzer_instance):
    """Test entity extraction using a mocked spaCy."""
    mock_doc = MagicMock()
    mock_ent1 = MagicMock()
    mock_ent1.text = "John Doe"
    mock_ent1.label_ = "PERSON"
    mock_ent2 = MagicMock()
    mock_ent2.text = "Acme Corp"
    mock_ent2.label_ = "ORG"
    mock_doc.ents = [mock_ent1, mock_ent2]
    
    entity_analyzer_instance.nlp.return_value = mock_doc

    content = "John Doe works at Acme Corp."
    entities = entity_analyzer_instance.extract_entities_from_content(content)
    
    assert ("John Doe", "PERSON") in entities
    assert ("Acme Corp", "ORG") in entities
    entity_analyzer_instance.nlp.assert_called_once_with(content)

def test_extract_entities_from_content_no_spacy(entity_analyzer_no_spacy):
    """Test entity extraction with spaCy fallback (no spaCy loaded)."""
    content = "This is a contract with an agreement from Big Company."
    entities = entity_analyzer_no_spacy.extract_entities_from_content(content)
    
    assert ("Contract", "DOCUMENT") in entities
    assert ("Agreement", "DOCUMENT") in entities
    assert ("Big", "POTENTIAL_NOUN") in entities # Basic fallback should pick this up

def test_detect_red_flags_in_text(entity_analyzer_instance):
    """Test red flag detection with various patterns."""
    text = "There was a bribe and an act of embezzlement. Also some market manipulation and a cover-up."
    detected_flags = entity_analyzer_instance._detect_red_flags_in_text(text)

    assert "financial_misconduct" in detected_flags
    assert "corruption_abuse" in detected_flags
    assert "general_malice" in detected_flags
    assert "bribe" in detected_flags["financial_misconduct"]
    assert "embezzlement" in detected_flags["financial_misconduct"]
    assert "market manipulation" in detected_flags["financial_misconduct"]
    assert "cover-up" in detected_flags["general_malice"]

def test_calculate_severity(entity_analyzer_instance):
    """Test severity calculation based on detected flags."""
    red_flags = {
        "financial_misconduct": ["bribe", "embezzlement"],
        "corruption_abuse": ["abuse of power"],
        "procedural_violations": []
    }
    severity_scores = entity_analyzer_instance._calculate_severity(red_flags)
    
    assert round(severity_scores["financial_misconduct"], 1) == 10.0 # 9 + 2*0.5 = 10
    assert round(severity_scores["corruption_abuse"], 1) == 8.5 # 8 + 1*0.5 = 8.5
    assert "procedural_violations" not in severity_scores # No flags, no score
    assert "ethical_concerns" not in severity_scores # No flags, no score

def test_identify_related_entities(entity_analyzer_instance):
    """Test identifying entities related to red flags."""
    entities = [("John Doe", "PERSON"), ("Acme Corp", "ORG"), ("Project X", "EVENT")]
    red_flags = {
        "financial_misconduct": ["John Doe engaged in embezzlement", "Acme Corp had a kickback scheme"],
        "general_malice": ["Project X was a cover-up"]
    }
    related_entities = entity_analyzer_instance._identify_related_entities(entities, red_flags)

    assert "John Doe engaged in embezzlement" in related_entities
    assert "John Doe" in related_entities["John Doe engaged in embezzlement"]
    assert "Acme Corp had a kickback scheme" in related_entities
    assert "Acme Corp" in related_entities["Acme Corp had a kickback scheme"]
    assert "Project X was a cover-up" in related_entities
    assert "Project X" in related_entities["Project X was a cover-up"]

def test_analyze_entities_for_red_flags(entity_analyzer_instance):
    """Integration test for the main red flag analysis function."""
    documents_content = ["John Doe received a bribe from Acme Corp for Project Alpha.", "There was a clear conflict of interest."]
    entities = [("John Doe", "PERSON"), ("Acme Corp", "ORG"), ("Project Alpha", "PROJECT")]

    analysis_report = entity_analyzer_instance.analyze_entities_for_red_flags(documents_content, entities)

    assert "red_flags" in analysis_report
    assert "severity_scores" in analysis_report
    assert "related_entities" in analysis_report
    assert "summary" in analysis_report

    assert "bribe" in analysis_report["red_flags"]["financial_misconduct"]
    assert "conflict of interest" in analysis_report["red_flags"]["corruption_abuse"]
    assert analysis_report["severity_scores"]["financial_misconduct"] > 0
    assert "John Doe" in analysis_report["related_entities"]["bribe"]
    assert "Acme Corp" in analysis_report["related_entities"]["bribe"]
    assert "High-priority investigation recommended." in analysis_report["summary"] # Based on mock severity

def test_generate_analysis_summary(entity_analyzer_instance):
    """Test generation of the analysis summary string."""
    entities = [("Person A", "PERSON"), ("Org B", "ORG")]
    red_flags = {
        "financial_misconduct": ["fraud"],
        "corruption_abuse": ["nepotism", "bribe"]
    }
    severity_scores = {
        "financial_misconduct": 8.0,
        "corruption_abuse": 9.0
    }
    
    summary = entity_analyzer_instance.generate_analysis_summary(entities, red_flags, severity_scores)
    
    assert "Analysis detected 3 potential red flags with an average severity of 8.5/10." in summary
    assert "- 1 person" in summary
    assert "- 1 org" in summary
    assert "- Financial Misconduct: 1 instances (Severity: 8.0/10)" in summary
    assert "- Corruption Abuse: 2 instances (Severity: 9.0/10)" in summary
    assert "High-priority investigation recommended." in summary

