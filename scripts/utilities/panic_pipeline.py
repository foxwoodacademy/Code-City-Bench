from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import pandas as pd
import requests

from shared import BASE_OUTBOUND, ensure_outbound_tree, utc_now, write_json, write_text

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DashboardGenerator:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.summary_path = base_dir / "boardroom" / "telemetry_summary.json"

    def update_summary(self, alerts: list[dict[str, Any]]):
        write_json(self.summary_path, {"generated_at": utc_now(), "alerts": alerts})
        logging.info(f"Updated dashboard summary at {self.summary_path}")

class DistressIntelEngine:
    def __init__(self):
        logging.info("Loading distress signals")
        self.base_dir = ensure_outbound_tree(BASE_OUTBOUND)
        self.dashboard = DashboardGenerator(self.base_dir)

    def fetch_panic_signals(self):
        return pd.DataFrame(
            [
                {
                    "vector_type": "REAL_ESTATE_FIRE_SALE",
                    "target_region": "Metro Atlanta, GA",
                    "signal": "Spike in pre-foreclosure listings and inventory pressure.",
                    "fear_index": "CRITICAL",
                    "playbook": "Review acquisition and reserve plans.",
                },
                {
                    "vector_type": "EQUITY_CAPITULATION",
                    "target_region": "Commercial REIT sector",
                    "signal": "Heavy outflows and elevated put volume.",
                    "fear_index": "HIGH",
                    "playbook": "Review exposure and hedges.",
                },
                {
                    "vector_type": "MORTGAGE_LIQUIDITY_RUN",
                    "target_region": "Regional bank sector (Southwest)",
                    "signal": "Default rates and liquidity concerns are increasing.",
                    "fear_index": "CRITICAL",
                    "playbook": "Review liquidity reserves and counterparty limits.",
                },
            ]
        )

def route_panic_intel(engine: DistressIntelEngine, df: pd.DataFrame):
    alerts_for_dashboard = []

    for idx, row in df.iterrows():
        alert_info = {
            "type": row["vector_type"],
            "region": row["target_region"],
            "fear": row["fear_index"],
        }
        alerts_for_dashboard.append(alert_info)

        if row["vector_type"] == "EQUITY_CAPITULATION":
            write_json(
                engine.base_dir / "boardroom" / f"shareholder_panic_{idx}.json",
                {
                    "alert": f"Exposure review: {row['target_region']}",
                    "panic_trigger": row["signal"],
                    "action_mandate": "Review risk and hedge assumptions immediately.",
                },
            )

        if row["fear_index"] == "CRITICAL":
            write_text(
                engine.base_dir / "hotseat" / f"fire_sale_action_{idx}.txt",
                "\n".join(
                    [
                        "LIQUIDITY ALERT",
                        "=" * 20,
                        f"SECTOR/REGION: {row['target_region']}",
                        f"SIGNAL: {row['signal']}",
                        f"PLAYBOOK: {row['playbook']}",
                        "",
                    ]
                ),
            )

        if row["vector_type"] == "REAL_ESTATE_FIRE_SALE":
            write_text(
                engine.base_dir / "scouts" / "distressed_property_leads.txt",
                "\n".join(
                    [
                        f"[{utc_now()}] REGION: {row['target_region']}",
                        f"INTEL: {row['signal']}",
                        "FIELD ORDER: Review local acquisition capacity and constraints.",
                        "",
                    ]
                ),
                append=True,
            )

    engine.dashboard.update_summary(alerts_for_dashboard)
    logging.info("Routed panic telemetry to boardroom, hotseat, and scouts")

def dispatch_shareholder_telemetry(df: pd.DataFrame):
    endpoint = "https://httpbin.org/post"

    for _, row in df.iterrows():
        if row["vector_type"] != "EQUITY_CAPITULATION":
            continue

        payload = {
            "source_node": "MoltEngine_Capitulation_v5",
            "timestamp_utc": utc_now(),
            "asset_class": "Equities/REIT",
            "risk_profile": {
                "entity": row["target_region"],
                "trigger_event": row["signal"],
                "threat_level": row["fear_index"],
            },
            "recommended_action": "Review exposure and exit criteria.",
        }

        # Simple retry mechanism
        success = False
        for attempt in range(3):
            try:
                response = requests.post(endpoint, json=payload, timeout=20)
                response.raise_for_status()
                logging.info(f"Dispatched equity telemetry for {row['target_region']}")
                success = True
                break
            except Exception as exc:
                logging.warning(f"Attempt {attempt + 1} failed: {exc}")
        
        if not success:
            logging.error(f"Failed to dispatch equity telemetry for {row['target_region']} after 3 attempts.")

def export_wholesaler_txt_feed(base_dir: Any, df: pd.DataFrame):
    output_path = base_dir / "scouts" / "crm_ready_leads.txt"
    lines = [
        "=" * 50,
        "RAW DISTRESS LEAD TELEMETRY FEED - CRM READY",
        f"GENERATED: {utc_now()}",
        "=" * 50,
        "",
    ]

    for _, row in df.iterrows():
        if row["vector_type"] != "REAL_ESTATE_FIRE_SALE":
            continue
        lines.extend(
            [
                f"REGION TARGET: {row['target_region']}",
                f"RISK FACTOR   : {row['signal']}",
                f"LOCAL PLAYBOOK: {row['playbook']}",
                "STATUS        : REVIEW",
                "-" * 50,
            ]
        )

    write_text(output_path, "\n".join(lines) + "\n")
    logging.info(f"Updated {output_path}")

def main():
    engine = DistressIntelEngine()
    df = engine.fetch_panic_signals()
    route_panic_intel(engine, df)
    dispatch_shareholder_telemetry(df)
    export_wholesaler_txt_feed(engine.base_dir, df)

if __name__ == "__main__":
    main()
