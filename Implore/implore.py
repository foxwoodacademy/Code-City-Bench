import argparse
import json
from implore_scanner_walker import RepoWalker
from implore_scanner_profile import ProfileBuilder
from grants_gov_client import GrantsGovClient
from generator import NarrativeGenerator
from sf424_filler import SF424Filler
from matcher import SimpleSemanticMatcher
from regional_sources import SearXAdapter
from auditor import VerificationAuditor
from i18n import InternationalizationEngine
from ingestor import Ingestor
from ecosystem_bridge import bridge

def run_pipeline(directory=None, url=None, file_path=None, target_region=None, target_lang='en', domain="societal"):
    print(f"🚀 Starting Implore pipeline (Region: {target_region}, Domain: {domain})")
    
    # Ingestion phase
    ingestor = Ingestor()
    content = ""
    profile_data = {}
    if directory:
        walker = RepoWalker(directory)
        builder = ProfileBuilder()
        for filepath in walker.walk():
            builder.update_with_file(filepath)
        profile_data = builder.get_profile()
        content = str(profile_data)
        bridge.broadcast_insight("new_project_profile", profile_data)
    elif url:
        content = ingestor.fetch_url(url)
    elif file_path:
        content = ingestor.read_file(file_path)
    
    # 2. Match - Enhanced Search
    print(f"📡 Matching {domain} grants...")
    client = GrantsGovClient()
    matcher = SimpleSemanticMatcher()
    
    # Broadened Search scope based on domain
    opportunities = client.search_opportunities([domain, "equitable", "community"], limit=20)
    for opp in opportunities:
        matcher.add_grant(opp.get('id'), opp.get('title'), region='federal')
    
    best_match_id = matcher.find_best_match(content[:500], target_region=target_region)
    if not best_match_id:
        print("❌ No matching opportunities found.")
        return

    opp = next((o for o in opportunities if o.get('id') == best_match_id), None)
    print(f"✅ Found match: {opp.get('title')}")
    bridge.broadcast_insight("new_grant_match", opp)

    # 3. Generate - Domain Aware
    print("📝 Generating application...")
    profile = {"content": content}
    gen = NarrativeGenerator(profile, opp, domain=domain)
    technical_approach = gen.generate_technical_approach()
    
    # 4. Audit & Output
    auditor = VerificationAuditor()
    if not auditor.audit_draft(technical_approach):
        print("❌ Audit failed.")
        return

    filler = SF424Filler()
    sf424 = filler.fill(profile, opp)

    with open("implore_application.json", "w") as f:
        json.dump({"sf424": sf424, "narrative": technical_approach}, f, indent=2)
    
    print("✅ Pipeline complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Implore CLI")
    parser.add_argument("--directory", help="Directory to scan")
    parser.add_argument("--file", help="File to ingest (e.g., KS report)")
    parser.add_argument("--domain", default="societal", help="Grant domain (medical, societal, etc.)")
    args = parser.parse_args()
    run_pipeline(directory=args.directory, file_path=args.file, domain=args.domain)
