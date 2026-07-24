from __future__ import annotations

from datetime import datetime, timedelta
import sys

import pandas as pd
import requests

try:
    sys.path.append("/data/data/com.termux/files/home/key-handoff-system/src")
    from mediator import Mediator
except Exception:
    Mediator = None

from shared import BASE_OUTBOUND, ensure_outbound_tree, utc_now, write_json, write_text


class SupplyChainIngestion:
    def __init__(self):
        if Mediator is None:
            self.api_key = None
        else:
            try:
                self.api_key = Mediator().get_handle("NEWS_API")
            except Exception:
                self.api_key = None
        self.base_url = "https://newsapi.org/v2/everything"
        self.risk_keywords = (
            "(shortage OR boycott OR 'supply chain' OR 'price spike' OR 'factory strike') "
            "AND (semiconductor OR shipping OR logistics OR lithium OR manufacturing)"
        )

    def fetch_live_signals(self):
        yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        params = {
            "q": self.risk_keywords,
            "from": yesterday,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": 20,
        }

        if not self.api_key:
            return self._generate_mock_stream()

        params["apiKey"] = self.api_key

        try:
            response = requests.get(self.base_url, params=params, timeout=20)
            if response.status_code == 401:
                return self._generate_mock_stream()
            response.raise_for_status()
            return self._normalize_data(response.json().get("articles", []))
        except Exception as exc:
            print(f"[ingest] fallback to mock data: {exc}")
            return self._generate_mock_stream()

    def _normalize_data(self, raw_articles):
        rows = []
        for article in raw_articles or []:
            rows.append(
                {
                    "timestamp": article.get("publishedAt"),
                    "source": article.get("source", {}).get("name"),
                    "headline": article.get("title"),
                    "summary": article.get("description"),
                    "url": article.get("url"),
                    "risk_score": 0.0,
                }
            )
        return pd.DataFrame(rows)

    def _generate_mock_stream(self):
        now = utc_now()
        return pd.DataFrame(
            [
                {
                    "timestamp": now,
                    "source": "Global Logistics Review",
                    "headline": "Port strike delays electronic components",
                    "summary": "Dockworker action is disrupting shipments and pushing delivery schedules back.",
                    "url": "https://example.com/port-strike",
                    "risk_score": 0.0,
                },
                {
                    "timestamp": now,
                    "source": "Automotive Tech Daily",
                    "headline": "Lithium extraction issues tighten battery supply",
                    "summary": "Refinery issues are affecting component availability and spot pricing.",
                    "url": "https://example.com/lithium-shortage",
                    "risk_score": 0.0,
                },
                {
                    "timestamp": now,
                    "source": "Geopolitical Monitor",
                    "headline": "Semiconductor supplier boycott intensifies",
                    "summary": "Campaign activity is adding pressure to regional distribution networks.",
                    "url": "https://example.com/semiconductor-boycott",
                    "risk_score": 0.0,
                },
            ]
        )


def distribute_intelligence(df):
    base_dir = ensure_outbound_tree(BASE_OUTBOUND)

    for idx, row in df.iterrows():
        headline = row.get("headline", "Untitled event")
        summary = row.get("summary", "")
        source = row.get("source", "Unknown source")
        url = row.get("url", "")

        write_json(
            base_dir / "boardroom" / f"exec_alert_{idx}.json",
            {
                "risk_vector": headline,
                "business_impact": "Review the issue against sourcing, margin, and delivery constraints.",
                "source_authority": source,
                "logged_at": utc_now(),
            },
        )

        write_text(
            base_dir / "hotseat" / f"action_item_{idx}.txt",
            "\n".join(
                [
                    "TASK BRIEFING",
                    "=" * 24,
                    f"EVENT: {headline}",
                    f"SUMMARY: {summary}",
                    "ACTION: Review alternate suppliers and near-term safety stock.",
                    "",
                ]
            ),
        )

        write_json(
            base_dir / "askhole" / f"kb_doc_{idx}.json",
            {
                "text_content": f"Source: {source}. Incident: {headline}. Details: {summary}",
                "metadata": {"category": "supply_chain_disruption", "source_url": url},
            },
        )

        write_text(
            base_dir / "scouts" / f"intel_scout_{idx}.txt",
            "\n".join(
                [
                    "FIELD RECON REPORT",
                    f"Target Event: {headline}",
                    f"Source Feed: {source}",
                    f"Verification URL: {url}",
                    "Action: Map alternatives and verify the exposure.",
                    "",
                ]
            ),
        )

    print(f"distributed {len(df)} signal(s) to {base_dir}")


def main():
    engine = SupplyChainIngestion()
    live_df = engine.fetch_live_signals()
    if live_df.empty:
        print("no signals available")
        return

    print(f"ingested {len(live_df)} signal(s)")
    print(live_df[["source", "headline"]].to_string(index=False))
    distribute_intelligence(live_df)


if __name__ == "__main__":
    main()
