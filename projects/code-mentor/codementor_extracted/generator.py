import json

class NarrativeGenerator:
    def __init__(self, profile, opportunity):
        self.profile = profile
        self.opportunity = opportunity

    def generate_technical_approach(self):
        """Simulate LLM generation of a technical approach section"""
        # In a production environment, this would call Claude/OpenAI
        return f"""
# Technical Approach: {self.opportunity.get('title')}

Based on the analysis of our codebase, which primarily utilizes {list(self.profile.get('languages', {}).keys())}, 
we propose the following technical approach to address the objectives of {self.opportunity.get('number')}.
...
"""

if __name__ == "__main__":
    # Mock data
    profile = {"languages": {".py": 10}, "dependencies": ["requirements.txt"]}
    opp = {"title": "Test Grant", "number": "123-ABC"}
    
    generator = NarrativeGenerator(profile, opp)
    print(generator.generate_technical_approach())
