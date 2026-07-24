# tests/test_aura_agent.py
import pytest
import re # Needed for re.Pattern assertion
from modules.aura_agent import AuraMicroAgent

@pytest.fixture
def aura_agent_instance():
    """Provides an AuraMicroAgent instance."""
    return AuraMicroAgent()

def test_init(aura_agent_instance):
    """Test that AuraMicroAgent initializes correctly."""
    assert isinstance(aura_agent_instance.insight_generators, dict)
    assert "pattern_recognition" in aura_agent_instance.insight_generators
    assert aura_agent_instance.insights == []
    assert isinstance(aura_agent_instance.pattern_database, dict)

def test_initialize_pattern_database(aura_agent_instance):
    """Test that the pattern database is initialized with expected structure."""
    pattern_db = aura_agent_instance.pattern_database
    assert "financial_irregularity" in pattern_db
    assert "keywords" in pattern_db["financial_irregularity"]
    assert "regex" in pattern_db["financial_irregularity"]
    assert pattern_db["financial_irregularity"]["keywords"] == ["unexplained wealth", "offshore transfers", "shell company", "fraudulent invoice"]
    assert isinstance(pattern_db["financial_irregularity"]["regex"][0], re.Pattern)

@pytest.mark.parametrize("mode, expected_generators", [
    ("standard", ["pattern_recognition", "entity_connections", "risk_assessment"]),
    ("deep", ["pattern_recognition", "entity_connections", "timeline_analysis", "risk_assessment", "strategic_recommendations", "psychological_profile"]),
    ("audit", ["pattern_recognition", "entity_connections", "timeline_analysis", "risk_assessment", "strategic_recommendations", "psychological_profile"]),
    ("psychological_warfare", ["psychological_profile", "strategic_recommendations", "entity_connections"]),
    ("unknown_mode", ["pattern_recognition", "entity_connections", "risk_assessment"]) # Default to standard
])
def test_get_active_generators(aura_agent_instance, mode, expected_generators):
    """Test that correct insight generators are selected based on mode."""
    active_gens = aura_agent_instance._get_active_generators(mode)
    assert sorted(active_gens) == sorted(expected_generators)

def test_generate_pattern_recognition_insights(aura_agent_instance):
    """Test pattern recognition insights generation."""
    documents = ["There was an unexplained wealth transfer to a shell company."]
    entities = [{"name": "unexplained wealth", "type": "CONCEPT"}, {"name": "shell company", "type": "ORG"}]
    red_flags = {}
    mode = "standard"
    
    insights = aura_agent_instance._generate_pattern_recognition_insights(documents, entities, red_flags, mode)
    assert insights["type"] == "pattern_recognition"
    assert "significant patterns detected" in insights["summary"]
    assert len(insights["patterns_found"]) > 0
    assert insights["patterns_found"][0]["name"] == "financial_irregularity"
    assert "unexplained wealth" in insights["patterns_found"][0]["matches"][0]
    assert "shell company" in insights["patterns_found"][0]["matches"][1]

def test_generate_entity_connection_insights(aura_agent_instance):
    """Test entity connection insights generation."""
    documents = ["John Doe and Jane Smith met. Later, John Doe and Jane Smith signed a document."]
    entities = [{"name": "John Doe", "type": "PERSON"}, {"name": "Jane Smith", "type": "PERSON"}]
    red_flags = {}
    mode = "standard"
    
    insights = aura_agent_instance._generate_entity_connection_insights(documents, entities, red_flags, mode)
    assert insights["type"] == "entity_connections"
    assert "significant entity connections identified" in insights["summary"]
    assert len(insights["connections"]) > 0
    assert {"entities": ["Jane Smith", "John Doe"], "frequency": 2} in insights["connections"]

def test_generate_timeline_analysis_insights(aura_agent_instance):
    """Test timeline analysis insights generation (mocked events)."""
    documents = ["On Feb 10, 2024, an event occurred. On Jan 5, 2023, something else happened."]
    entities = []
    red_flags = {"red_flags": {"procedural_violations": ["audit findings on Jan 15, 2024"]}}
    mode = "deep"
    
    insights = aura_agent_instance._generate_timeline_analysis_insights(documents, entities, red_flags, mode)
    assert insights["type"] == "timeline_analysis"
    assert "key events on the timeline" in insights["summary"]
    assert len(insights["events"]) >= 3 # Includes mocked + extracted
    assert insights["events"][0]["date"] == "2023-01-05" # Earliest extracted
    assert insights["events"][1]["date"] == "2024-01-15" # Red flag extracted
    assert insights["events"][2]["date"] == "2024-02-10" # Latest extracted

def test_generate_risk_assessment_insights(aura_agent_instance):
    """Test risk assessment insights generation."""
    documents = []
    entities = []
    red_flags = {
        "severity_scores": {
            "financial_misconduct": 9.0,
            "corruption_abuse": 8.5
        }
    }
    mode = "audit" # Should increase risk
    
    insights = aura_agent_instance._generate_risk_assessment_insights(documents, entities, red_flags, mode)
    assert insights["type"] == "risk_assessment"
    assert "risk level: Critical" in insights["summary"] # 8.75 * 10 * 1.2 = 105, capped at 100
    assert insights["risk_score"] == 100.0
    assert "Financial Misconduct" in insights["risk_categories"][0]["category"]

def test_generate_strategic_recommendations_insights(aura_agent_instance):
    """Test strategic recommendations insights generation."""
    documents = []
    entities = []
    red_flags = {
        "severity_scores": {
            "financial_misconduct": 9.0,
            "corruption_abuse": 8.5
        }
    }
    mode = "audit"
    
    insights = aura_agent_instance._generate_strategic_recommendations_insights(documents, entities, red_flags, mode)
    assert insights["type"] == "strategic_recommendations"
    assert "Generated" in insights["summary"]
    assert len(insights["recommendations"]) >= 2
    assert any("Initiate immediate legal review" in rec["action"] for rec in insights["recommendations"])
    assert any("Prepare detailed audit report" in rec["action"] for rec in insights["recommendations"])

def test_generate_psychological_profile_insights(aura_agent_instance):
    """Test psychological profile insights generation."""
    documents = ["John Doe's emails revealed signs of greed and fear of exposure.", "Jane Smith was implicated in a cover-up."]
    entities = [{"name": "John Doe", "type": "PERSON"}, {"name": "Jane Smith", "type": "PERSON"}]
    red_flags = {}
    mode = "psychological_warfare"
    
    insights = aura_agent_instance._generate_psychological_profile_insights(documents, entities, red_flags, mode)
    assert insights["type"] == "psychological_profile"
    assert "psychological profiles for 2 individuals" in insights["summary"]
    assert len(insights["profiles"]) == 2
    
    john_profile = next((p for p in insights["profiles"] if p["name"] == "John Doe"), None)
    assert "Risk-taker (financial)" in john_profile["traits"]
    assert "Greed/Financial incentive" in john_profile["vulnerabilities"]

    jane_profile = next((p for p in insights["profiles"] if p["name"] == "Jane Smith"), None)
    assert "Control-oriented" in jane_profile["traits"]
    assert "Fear of exposure" in jane_profile["vulnerabilities"]

def test_generate_insights_overall_summary(aura_agent_instance):
    """Test the main generate_insights function and overall summary."""
    documents = ["Financial irregularity detected.", "John Doe and Jane Smith connected."]
    entities = [{"name": "John Doe", "type": "PERSON"}, {"name": "Jane Smith", "type": "PERSON"}]
    red_flags = {
        "red_flags": {"financial_misconduct": ["irregularity"]},
        "severity_scores": {"financial_misconduct": 8.0}
    }
    mode = "standard"
    
    all_insights = aura_agent_instance.generate_insights(documents, entities, red_flags, mode)
    
    assert len(all_insights) >= 4 # Standard insights + overall summary
    overall_summary_insight = next(i for i in all_insights if i["type"] == "overall_aura_summary")
    assert "Identified 1 key behavioral patterns." in overall_summary_insight["summary"]
    assert "Detected 1 significant entity connections." in overall_summary_insight["summary"]
    assert "Assessed overall risk as moderate (Score: 80.0/100)." in overall_summary_insight["summary"]

