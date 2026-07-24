import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class NarrativeGenerator:
    """Core narrative engine for domain-agnostic grant writing."""
    def __init__(self, profile, opportunity, domain="technological"):
        self.profile = profile
        self.opportunity = opportunity
        self.domain = domain
        # Fallback to mock if API key is missing
        if os.environ.get("OPENAI_API_KEY"):
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
            self.use_llm = True
        else:
            self.use_llm = False

    def generate_technical_approach(self):
        """Generates a structured, fact-based narrative adapted for the target domain."""
        if self.use_llm:
            # Domain-Aware Prompt Engineering
            system_prompt = (f"You are a professional grant writer specializing in the {self.domain} sector. "
                             f"Focus on equitable access, clear measurable outcomes, and significant societal impact. "
                             f"Avoid jargon and strictly adhere to the project data.")
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("user", "Write a compelling technical narrative for grant: {opp_title}. "
                         "Project data: {profile_data}")
            ])
            chain = prompt | self.llm
            response = chain.invoke({"opp_title": self.opportunity.get('title'), "profile_data": str(self.profile)})
            return response.content
        else:
            # Mock fallback
            return f"Fact-based technical approach for {self.opportunity.get('title')} ({self.domain} sector) (Mocked)."

# --- Lesser utility helpers pushed to bottom ---
class MockNarrativeGenerator(NarrativeGenerator):
    """Helper for testing logic pipelines without LLM calls."""
    def generate_technical_approach(self):
        return f"Mocked approach for {self.domain}."
