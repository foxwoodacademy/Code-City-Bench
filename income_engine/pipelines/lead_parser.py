import re
import json
import logging

logger = logging.getLogger("IncomeEngine.Parser")

def clean_and_score_lead(raw_data):
    """
    Parses raw agent output, extracts critical business points, 
    and determines outreach viability.
    """
    logger.info("Processing raw payload through parsing filter...")
    
    # Standardize data shape
    lead_profile = {
        "name": raw_data.get("name", "Unknown Business"),
        "email": raw_data.get("email", None),
        "phone": raw_data.get("phone", None),
        "website": raw_data.get("website", None),
        "friction_points": [],
        "confidence_score": 0
    }
    
    # Simple heuristic check for optimization gaps (e.g., slow load times, missing SEO meta)
    notes = str(raw_data.get("notes", "")).lower()
    if "slow" in notes or "performance" in notes:
        lead_profile["friction_points"].append("Page performance / Load speed bottlenecks")
        lead_profile["confidence_score"] += 35
        
    if "missing" in notes or "no schema" in notes or "seo" in notes:
        lead_profile["friction_points"].append("Unoptimized search engine presence")
        lead_profile["confidence_score"] += 35

    if lead_profile["email"] or lead_profile["phone"]:
        lead_profile["confidence_score"] += 30
        
    return lead_profile

def generate_consulting_pitch(profile):
    """
    Programmatically structures a personalized, technical pitch outline 
    based on identified business friction points.
    """
    if not profile["friction_points"]:
        profile["friction_points"].append("General conversion flow optimization")
        
    frictions_str = " and ".join(profile["friction_points"])
    
    pitch = (
        f"Subject: Performance Audit & Optimization for {profile['name']}\n\n"
        f"Hi Team,\n\n"
        f"I recently analyzed your public digital infrastructure and noticed a few critical "
        f"bottlenecks—specifically regarding {frictions_str}.\n\n"
        f"Fixing these performance blocks directly correlates to a lift in localized customer acquisition. "
        f"I've built automated tools to resolve these exact issues cleanly.\n\n"
        f"Let me know if you have 5 minutes to look over the raw diagnostic data.\n\n"
        f"Best,\nConsulting Engine"
    )
    return pitch
