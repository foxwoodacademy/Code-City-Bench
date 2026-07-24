import argparse
import json
from implore_scanner_walker import RepoWalker
from implore_scanner_profile import ProfileBuilder
from grants_gov_client import GrantsGovClient
from generator import NarrativeGenerator
from sf424_filler import SF424Filler

def run_pipeline(directory):
    print(f"🚀 Starting Implore pipeline on: {directory}")

    # 1. Scan
    print("🔍 Scanning codebase...")
    walker = RepoWalker(directory)
    builder = ProfileBuilder()
    for filepath in walker.walk():
        builder.update_with_file(filepath)
    profile = builder.get_profile()
    
    # 2. Match
    print("📡 Matching grants...")
    client = GrantsGovClient()
    # Simple keyword extraction for matching
    keywords = list(profile.get('languages', {}).keys())[:2]
    opportunities = client.search_opportunities(keywords, limit=1)
    
    if not opportunities:
        print("⚠️ No matches for specific languages, trying broad search...")
        opportunities = client.search_opportunities("technology", limit=1)
    
    if not opportunities:
        print("❌ No matching opportunities found.")
        return

    opp = opportunities[0]
    print(f"✅ Found match: {opp.get('title')}")

    # 3. Generate
    print("📝 Generating application...")
    gen = NarrativeGenerator(profile, opp)
    technical_approach = gen.generate_technical_approach()
    
    filler = SF424Filler()
    sf424 = filler.fill(profile, opp)

    # 4. Output
    output = {
        "sf424": sf424,
        "narrative": technical_approach
    }
    
    with open("implore_application.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("✅ Pipeline complete. Results in implore_application.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Implore CLI")
    parser.add_argument("directory", help="Directory to scan")
    args = parser.parse_args()
    run_pipeline(args.directory)
