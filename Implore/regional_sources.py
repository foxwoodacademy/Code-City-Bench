import requests

class RegionalSourceAdapter:
    """Base class for regional grant sources."""
    def fetch_grants(self, region):
        raise NotImplementedError

class SearXAdapter(RegionalSourceAdapter):
    """Adapter for SearX to query diverse knowledge sources."""
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_grants(self, query):
        # Example SearX API request
        params = {'q': query, 'format': 'json', 'categories': 'general'}
        try:
            response = requests.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            print(f"❌ SearX error: {e}")
            return []
