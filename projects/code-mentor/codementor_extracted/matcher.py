#!/usr/bin/env python3
"""
IMPLORE SIDECAR: Grant Matcher
"""
import json
from pathlib import Path

class GrantMatcher:
    def __init__(self, profile_file):
        with open(profile_file, 'r') as f:
            self.profile = json.load(f)
        self.grants = self._load_mock_grants()

    def _load_mock_grants(self):
        """Mock grant database for initial development"""
        return [
            {"id": "NSF-POSE-2026", "title": "Pathways to Enable Open-Source Ecosystems", "tech_keywords": ["python", "opensource", "ecosystem"]},
            {"id": "SBIR-PHASE1-2026", "title": "SBIR Phase I - Tech Innovation", "tech_keywords": ["go", "typescript", "innovation"]},
            {"id": "USDA-RURAL-2026", "title": "Rural Community Development", "tech_keywords": ["community", "development"]}
        ]

    def match(self):
        matches = []
        # Simple keyword-based matching
        tech_langs = list(self.profile.get("languages", {}).keys())
        
        for grant in self.grants:
            score = 0
            for keyword in grant["tech_keywords"]:
                if any(keyword in lang for lang in tech_langs):
                    score += 1
            
            if score > 0:
                matches.append({"grant": grant, "score": score})
        
        return sorted(matches, key=lambda x: x["score"], reverse=True)

def main():
    matcher = GrantMatcher("project_profile.json")
    matches = matcher.match()
    
    print(f"✅ Found {len(matches)} potential grant matches:")
    for m in matches:
        print(f"  [{m['score']}] {m['grant']['title']} ({m['grant']['id']})")

if __name__ == "__main__":
    main()
