import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load internal environment vars
load_dotenv()

class SupplyChainIngestion:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY") or "YOUR_MOCK_OR_REAL_KEY"
        self.base_url = "https://newsapi.org/v2/everything"
        
        # Core supply chain risk indicators to track
        self.risk_keywords = (
            "(shortage OR boycott OR 'supply chain' OR 'price spike' OR 'factory strike') "
            "AND (semiconductor OR shipping OR logistics OR lithium OR manufacturing)"
        )

    def fetch_live_signals(self):
        """Polls global networks for real-time risk events from the past 24 hours."""
        yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        params = {
            'q': self.risk_keywords,
            'from': yesterday,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 20,
            'apiKey': self.api_key
        }
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Ingesting live global telemetry streams...")
        
        try:
            response = requests.get(self.base_url, params=params)
            
            # If API key is missing/unauthorized, fallback to mock simulation data for local development
            if response.status_code == 401 or self.api_key == "YOUR_MOCK_OR_REAL_KEY":
                print("⚠️ Using generated real-time mock telemetry (No valid API Key detected)...")
                return self._generate_mock_stream()
                
            response.raise_for_status()
            articles = response.json().get('articles', [])
            return self._normalize_data(articles)
            
        except Exception as e:
            print(f"❌ Ingestion pipeline structural failure: {e}")
            return pd.DataFrame()

    def _normalize_data(self, raw_articles):
        """Flattens JSON data payloads into structured Pandas vectors."""
        if not raw_articles:
            return pd.DataFrame()
            
        structured_data = []
        for art in raw_articles:
            structured_data.append({
                'timestamp': art.get('publishedAt'),
                'source': art.get('source', {}).get('name'),
                'headline': art.get('title'),
                'summary': art.get('description'),
                'url': art.get('url'),
                'risk_score': 0.0  # Placeholder for our predictive model
            })
            
        return pd.DataFrame(structured_data)

    def _generate_mock_stream(self):
        """Fallback simulation engine ensuring the SaaS remains testable offline."""
        mock_events = [
            {
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'Global Logistics Review',
                'headline': 'Port of LA faces sudden dockworker strike, delaying electronic components',
                'summary': 'Negotiations stalled midnight leading to immediate picketing. Massive shipping bottlenecks predicted.',
                'url': 'https://example.com/port-strike',
                'risk_score': 0.0
            },
            {
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'Automotive Tech Daily',
                'headline': 'Lithium refinery extraction issues trigger minor market shortages',
                'summary': 'Refinery issues in Australia cause supply drops, forcing battery cell components up 12% in spot price.',
                'url': 'https://example.com/lithium-shortage',
                'risk_score': 0.0
            },
            {
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'Geopolitical Monitor',
                'headline': 'Consumer boycott campaigns targeting major semiconductor supplier intensify',
                'summary': 'Social media campaigns spark boycotts across EU regions affecting regional distribution networks.',
                'url': 'https://example.com/semiconductor-boycott',
                'risk_score': 0.0
            }
        ]
        return pd.DataFrame(mock_events)

if __name__ == "__main__":
    # Test script standalone execution
    engine = SupplyChainIngestion()
    df = engine.fetch_live_signals()
    
    print(f"\n✅ Successfully Ingested {len(df)} Active Supply Chain Vectors:")
    print(df[['source', 'headline']].to_string(index=False))

import json

def distribute_intelligence(df):
    """Routes tailored intelligence payloads to specialized operational nodes."""
    import os
    
    # Base paths inside your SaaS structure
    base_dir = "/storage/emulated/0/RootBase/New-SaaS/data_outbound"
    nodes = ['boardroom', 'hotseat', 'askhole', 'scouts']
    for node in nodes:
        os.makedirs(f"{base_dir}/{node}", exist_ok=True)
        
    for idx, row in df.iterrows():
        headline = row['headline']
        summary = row['summary']
        source = row['source']
        url = row['url']
        
        # 🏢 NODE 1: BOARDROOM (Executive Decision Format)
        boardroom_payload = {
            "risk_vector": headline,
            "business_impact": "Requires financial assessment on margin variance and contract penalty clauses.",
            "source_authority": source,
            "logged_at": datetime.utcnow().isoformat()
        }
        with open(f"{base_dir}/boardroom/exec_alert_{idx}.json", "w") as f:
            json.dump(boardroom_payload, f, indent=4)

        # 🔥 NODE 2: HOTSEAT (Immediate Threat Containment Text)
        with open(f"{base_dir}/hotseat/action_item_{idx}.txt", "w") as f:
            f.write(f"URGENT TASK FORCE BRIEFING\n{'='*30}\n")
            f.write(f"THREAT: {headline}\n")
            f.write(f"SUMMARY: {summary}\n")
            f.write(f"MITIGATION MANDATE: Source backup suppliers and review safety stock limits within 4 hours.\n")

        # 🕳️ NODE 3: ASKHOLE (LLM Chatbot Ingestion Vector JSON)
        askhole_payload = {
            "text_content": f"Source: {source}. Incident: {headline}. Details: {summary}",
            "metadata": {"category": "supply_chain_disruption", "source_url": url}
        }
        with open(f"{base_dir}/askhole/kb_doc_{idx}.json", "w") as f:
            json.dump(askhole_payload, f, indent=4)

        # 🧭 NODE 4: SCOUTS (Field Logistics Target Text)
        with open(f"{base_dir}/scouts/intel_scout_{idx}.txt", "w") as f:
            f.write(f"SCOUT FIELD RECON REPORT\n")
            f.write(f"Target Event: {headline}\n")
            f.write(f"Source Feed: {source}\n")
            f.write(f"Verification URL: {url}\n")
            f.write(f"Action: Map alternative geographic channels bypassing this friction point.\n")

    print(f"\n🚀 Intel successfully distributed to Boardroom, Hotseat, Askhole, and Scouts at {base_dir}/")

# Modify execution entry point to run distribution
if __name__ == "__main__":
    engine = SupplyChainIngestion()
    live_df = engine.fetch_live_signals()
    if not live_df.empty:
        distribute_intelligence(live_df)
