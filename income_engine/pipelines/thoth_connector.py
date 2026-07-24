import sys
import logging

# Append the main Thoth orchestrator path to access adapters
sys.path.append("/storage/emulated/0/RootBase/thoth_orchestrator")

try:
    from thoth_adapters import lough
    THOTH_AVAILABLE = True
except ImportError:
    THOTH_AVAILABLE = False
    print("[WARN] Thoth Orchestrator mesh path not found. Running independent engine logging.")

logger = logging.getLogger("IncomeEngine.Connector")

def broadcast_lead_to_swarm(profile):
    """
    Pushes verified local business leads with real network friction points
    directly into the Loom Mesh / Lough Event Spine for agent processing.
    """
    if not THOTH_AVAILABLE:
        logger.warning(f"Mesh offline. Aborting broadcast for: {profile['name']}")
        return False
        
    event_payload = {
        "business_name": profile["name"],
        "phone": profile.get("phone", "N/A"),
        "website": profile.get("website", ""),
        "detected_vulnerabilities": profile.get("friction_points", []),
        "remediation_assets": profile.get("compiled_assets", []),
        "pitch_package_path": profile.get("fix_package_directory", "")
    }
    
    logger.info(f"Emitting scout.lead.found event for {profile['name']} over Lough Mesh...")
    
    # Broadcast explicitly matching the event loop types recognized by thoth_daemon.py
    response = lough.emit(
        event_type="scout.lead.found",
        payload=event_payload,
        source="income_engine_auditor"
    )
    return response
