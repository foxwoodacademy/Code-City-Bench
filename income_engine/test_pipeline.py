import sys
import os
import json

# Ensure parent and pipeline paths are accessible
sys.path.append(os.path.expanduser("/storage/emulated/0/RootBase/income_engine"))
from pipelines.lead_parser import clean_and_score_lead, generate_consulting_pitch

def run_diagnostic():
    print("Executing standalone pipeline validation...")
    
    # Mock data mimicking a raw agent run from a business search
    mock_agent_result = {
        "name": "Wellington Moto Repairs",
        "email": "contact@wellingtonmoto.com",
        "phone": "620-555-0199",
        "website": "www.wellingtonmoto.com",
        "notes": "The site lacks mobile-responsive layouts, has slow image load times, and missing SEO metadata tags."
    }
    
    # 1. Test the parser filtering
    profile = clean_and_score_lead(mock_agent_result)
    print(f"\n[PARSER SUCCESS] Lead Scored: {profile['confidence_score']}/100")
    print(f"Identified Friction Points: {profile['friction_points']}")
    
    # 2. Test the pitch generation layout
    pitch_draft = generate_consulting_pitch(profile)
    print("\n[GENERATION SUCCESS] Draft Produced:")
    print("-" * 50)
    print(pitch_draft)
    print("-" * 50)
    
    # 3. Simulate file output safety
    output_dir = os.path.expanduser("/storage/emulated/0/RootBase/income_engine/data/leads")
    test_out = os.path.join(output_dir, "test_evaluated_leads.json")
    
    with open(test_out, "w") as f:
        json.dump(profile, f, indent=4)
    print(f"\n[STORAGE SUCCESS] Verified write capabilities to: {test_out}\n")

if __name__ == "__main__":
    run_diagnostic()
