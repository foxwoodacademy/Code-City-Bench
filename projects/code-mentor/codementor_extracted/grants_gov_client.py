import requests
import json

class GrantsGovClient:
    BASE_URL = "https://api.grants.gov/v1/api/search2"

    def search_opportunities(self, keywords, limit=5):
        """Search Grants.gov opportunities (no auth required)"""
        # Testing a payload matching the structure seen in the debugging output
        data = {
            "keyword": keywords,
            "oppStatuses": "posted",
            "rows": limit
        }
        try:
            print(f"DEBUG: Requesting {self.BASE_URL} with payload {data}")
            response = requests.post(self.BASE_URL, json=data, headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            results = response.json()
            # It seems the data is under result.get("data").get("oppHits")
            return results.get("data", {}).get("oppHits", [])
        except Exception as e:
            print(f"❌ Grants.gov API error: {e}")
            return []

if __name__ == "__main__":
    client = GrantsGovClient()
    # Broad search
    results = client.search_opportunities("technology", limit=5)
    print(f"Results found: {len(results)}")
    if results:
        print(json.dumps(results[0], indent=2))
