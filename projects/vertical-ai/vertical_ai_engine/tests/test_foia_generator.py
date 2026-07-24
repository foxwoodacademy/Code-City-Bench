# tests/test_foia_generator.py
import pytest
from datetime import date
from modules.foia_generator import FOIAGeneratorMicroAgent

@pytest.fixture
def foia_generator_instance():
    """Provides a FOIAGeneratorMicroAgent instance."""
    return FOIAGeneratorMicroAgent()

def test_load_templates(foia_generator_instance):
    """Test that templates are loaded correctly."""
    assert "standard" in foia_generator_instance.templates
    assert "appeal" in foia_generator_instance.templates
    assert "Dear $recipient_salutation" in foia_generator_instance.templates["standard"].template
    assert "Re: FOIA Appeal" in foia_generator_instance.templates["appeal"].template

def test_initialize_agency_database(foia_generator_instance):
    """Test that the agency database is initialized."""
    assert "department_of_justice" in foia_generator_instance.agency_info
    assert foia_generator_instance.agency_info["department_of_justice"]["name"] == "Department of Justice"

def test_generate_foia_request_success(foia_generator_instance):
    """Test successful generation of a standard FOIA request."""
    data = {
        "records_description": "all emails between John Doe and Jane Smith concerning Project Phoenix",
        "requester_category": "a journalist",
        "your_name": "Test Requester",
        "your_contact_info": "123 Test St, Test City, TS 12345, test@example.com",
        "agency_key": "department_of_justice"
    }
    
    foia_letter = foia_generator_instance.generate_foia_request(data)
    
    assert f"Dear Sir or Madam:" in foia_letter
    assert "Re: Freedom of Information Act Request" in foia_letter
    assert "I request that a copy of the following documents be provided to me: all emails between John Doe and Jane Smith concerning Project Phoenix" in foia_letter
    assert "In order to help determine my status for the purpose of determining the applicability of any fees, you should know that I am a journalist." in foia_letter
    assert f"Sincerely,\n\nTest Requester" in foia_letter
    assert date.today().strftime("%B %d, %Y") in foia_letter
    assert "950 Pennsylvania Avenue, NW, Washington, DC 20530" in foia_letter

def test_generate_foia_request_unknown_agency(foia_generator_instance):
    """Test FOIA generation with an unknown agency."""
    data = {
        "records_description": "some records",
        "requester_category": "public",
        "your_name": "Unknown",
        "your_contact_info": "contact",
        "agency_key": "non_existent_agency"
    }
    foia_letter = foia_generator_instance.generate_foia_request(data)
    assert "Unknown Agency" in foia_letter
    assert "FOIA Officer" in foia_letter

def test_generate_foia_request_missing_data(foia_generator_instance):
    """Test FOIA generation with missing required data."""
    data = {
        "requester_category": "a researcher",
        "agency_key": "department_of_justice"
        # records_description, your_name, your_contact_info are missing
    }
    foia_letter = foia_generator_instance.generate_foia_request(data)
    assert "Error generating FOIA request: Missing data for" in foia_letter
    assert "$records_description" in foia_letter # Indicates placeholder wasn't filled

def test_generate_appeal_letter_success(foia_generator_instance):
    """Test successful generation of an appeal letter."""
    analysis_data = {
        "exemptions_cited": ["b(5)", "b(6)"],
        "denial_date": "2023-05-10"
    }
    request_data = {
        "original_request_date": "2023-04-01",
        "tracking_number": "DOJ-2023-12345",
        "your_name": "Appeal Requester",
        "your_contact_info": "appeal@example.com",
        "agency_key": "department_of_justice"
    }
    
    appeal_letter = foia_generator_instance.generate_appeal_letter(analysis_data, request_data)
    
    assert f"Dear Sir or Madam:" in appeal_letter
    assert "Re: FOIA Appeal - Original Request Dated 2023-04-01 - Tracking Number DOJ-2023-12345" in appeal_letter
    assert "I received your denial letter on 2023-05-10." in appeal_letter
    assert "Regarding Exemption b(5) (Deliberative Process)" in appeal_letter
    assert "Regarding Exemption b(6) (Personal Privacy)" in appeal_letter
    assert f"Sincerely,\n\nAppeal Requester" in appeal_letter
    assert date.today().strftime("%B %d, %Y") in appeal_letter

def test_generate_appeal_letter_no_exemptions(foia_generator_instance):
    """Test appeal letter when no specific exemptions are cited."""
    analysis_data = {
        "exemptions_cited": [],
        "denial_date": "2023-06-01"
    }
    request_data = {
        "original_request_date": "2023-05-01",
        "tracking_number": "EPA-2023-98765",
        "your_name": "No Exemptioner",
        "your_contact_info": "noexemption@example.com",
        "agency_key": "environmental_protection_agency"
    }
    
    appeal_letter = foia_generator_instance.generate_appeal_letter(analysis_data, request_data)
    
    assert "The agency has not provided specific reasons for the denial" in appeal_letter
    assert "Regarding Exemption b(5)" not in appeal_letter # Ensure specific exemption text is not there

