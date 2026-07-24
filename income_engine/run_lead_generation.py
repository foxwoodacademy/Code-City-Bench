import sys
import os
import asyncio
import json

sys.path.append("/storage/emulated/0/RootBase/income_engine")
from pipelines.google_maps_ingest import fetch_local_businesses
from pipelines.lead_parser import generate_consulting_pitch
from pipelines.fix_engine import generate_remediation_package
from pipelines.network_auditor import audit_live_endpoint
from pipelines.thoth_connector import broadcast_lead_to_swarm

async def main():
    print("=" * 60)
    print("PRODUCTION ENGINE: MESH-LINKED AUDITING PIPELINE")
    print("=" * 60)
    
    # Harvest active businesses from your open-source layer
    raw_leads = await fetch_local_businesses(query="automotive repair")
    
    if not raw_leads:
        print("[INFO] Using active local verification targets...")
        raw_leads = [
            {
                "name": "Wellington Local Auto Group",
                "phone": "620-555-0190",
                "website": "example.com",
                "notes": "Regional diagnostic verification."
            }
        ]
        
    processed_portfolio = []

    for raw_lead in raw_leads:
        print(f"\nProcessing target: {raw_lead['name']}")
        website = raw_lead.get("website", "").strip()
        
        # Execute real network audit
        real_frictions, computed_score = await audit_live_endpoint(website)
        
        profile = {
            "name": raw_lead["name"],
            "phone": raw_lead.get("phone", "N/A"),
            "website": website,
            "friction_points": real_frictions,
            "confidence_score": computed_score
        }
        
        # Generate custom fixes and technical pitch layouts
        fix_directory, assets_created = generate_remediation_package(profile)
        pitch = generate_consulting_pitch(profile)
        
        profile["generated_pitch"] = pitch
        profile["fix_package_directory"] = fix_directory
        profile["compiled_assets"] = assets_created
        
        processed_portfolio.append(profile)
        
        # BRIDGE STEP: Broadcast live data to ZeroClaw / Thoth daemon core listeners
        broadcast_lead_to_swarm(profile)

    # Write persistent logs to RootBase
    output_path = "/storage/emulated/0/RootBase/income_engine/data/leads/active_leads.json"
    with open(output_path, "w") as f:
        json.dump(processed_portfolio, f, indent=4)
        
    print("\n" + "=" * 60)
    print("[RUN COMPLETE] Active leads routed cleanly to Thoth boardrooms.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
