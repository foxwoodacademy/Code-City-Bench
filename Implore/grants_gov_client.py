import requests
import json

class GrantsGovClient:
    BASE_URL = "https://api.grants.gov/v1/api/search2"

    def search_opportunities(self, keywords, limit=20):
        """Enhanced search: accepts a list of keywords to broaden scope."""
        if isinstance(keywords, list):
            keyword_query = " OR ".join(keywords)
        else:
            keyword_query = keywords
            
        data = {
            "keyword": keyword_query,
            "oppStatuses": "posted",
            "rows": limit
        }
        try:
            response = requests.post(self.BASE_URL, json=data, headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            results = response.json()
            return results.get("data", {}).get("oppHits", [])
        except Exception as e:
            print(f"❌ Grants.gov API error: {e}")
            return []

# --- Lesser classes/test utilities pushed down ---
def test_search():
    client = GrantsGovClient()
    # Test broad scope: technology, medical, societal, education
    broad_terms = ["technology", "medical", "societal", "education"]
    results = client.search_opportunities(broad_terms, limit=5)
    print(f"Broad search found {len(results)} opportunities.")

if __name__ == "__main__":
    test_search()
