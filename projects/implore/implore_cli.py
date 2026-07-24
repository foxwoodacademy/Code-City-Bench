import argparse
import json
from implore_scanner_walker import RepoWalker
from implore_scanner_profile import ProfileBuilder

def main():
    parser = argparse.ArgumentParser(description="Implore Scanner")
    parser.add_argument("directory", help="Directory to scan")
    args = parser.parse_args()
    
    walker = RepoWalker(args.directory)
    builder = ProfileBuilder()
    
    for filepath in walker.walk():
        builder.update_with_file(filepath)
    
    profile = builder.get_profile()
    
    with open("project_profile_new.json", "w") as f:
        json.dump(profile, f, indent=2)
    
    print("✅ Profile generated: project_profile_new.json")

if __name__ == "__main__":
    main()
