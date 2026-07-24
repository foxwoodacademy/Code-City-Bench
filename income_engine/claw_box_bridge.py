import os
import sys
import json
import logging
import http.client
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger("ModMind.ClawBox")

class SwarmIntegrationBox:
    def __init__(self):
        # Write directly to the www folder to avoid Android symlink blocks
        self.boardroom_log_path = Path("/storage/emulated/0/RootBase/income_engine/www/boardroom_events.json")
        self.openclaw_token = os.getenv("OPENCLAW_GATEWAY_TOKEN", "HighFives26!")
        self.boardroom_log_path.parent.mkdir(parents=True, exist_ok=True)

    def dispatch_to_openclaw_gateway(self, payload: dict) -> bool:
        logger.info("Forwarding lead optimization payload matrix to OpenClaw gateway service...")
        try:
            conn = http.client.HTTPConnection("127.0.0.1", 5001, timeout=3)
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openclaw_token}"
            }
            conn.request("POST", "/v1/gateway/inject", json.dumps(payload), headers)
            res = conn.getresponse()
            if res.status in [200, 201]:
                logger.info("[SUCCESS] OpenClaw system frame acknowledged state integration.")
                return True
        except Exception as e:
            logger.warning(f"[FALLBACK] OpenClaw direct daemon offline. Stashing block locally. Reason: {e}")
        return False

    def inject_to_boardroom_canvas(self, business_name: str, frictions: list, score: int):
        logger.info(f"Injecting event notification context vector to 3D Boardroom stream: {business_name}")
        
        event_frame = {
            "event_type": "LEAD_DISCOVERY_SWARM",
            "agent_node": "ZeroClaw_Auditor",
            "payload": {
                "business_name": business_name,
                "friction_points": frictions,
                "optimization_score": score,
                "action_required": "Deploy Mrs. Higgins SEO Optimization Pack via Lightning Rail"
            }
        }

        try:
            events = []
            if self.boardroom_log_path.exists() and self.boardroom_log_path.stat().st_size > 0:
                with open(self.boardroom_log_path, "r") as f:
                    try:
                        events = json.load(f)
                        if not isinstance(events, list): events = []
                    except json.JSONDecodeError:
                        events = []
            
            events.append(event_frame)
            events = events[-20:] # Maintain ring-buffer size
            
            with open(self.boardroom_log_path, "w") as f:
                json.dump(events, f, indent=4)
            logger.info("[SUCCESS] Boardroom layout vector re-indexed successfully.")
        except Exception as e:
            logger.error(f"Failed to bind visual context element to Boardroom path: {e}")

def process_pipeline_wire(business_name: str, frictions: list, score: int):
    box = SwarmIntegrationBox()
    claw_payload = {
        "source": "ModMind_Deck_v3",
        "target_node": business_name,
        "metrics": {"score": score, "frictions_found": len(frictions)},
        "context": frictions
    }
    box.dispatch_to_openclaw_gateway(claw_payload)
    box.inject_to_boardroom_canvas(business_name, frictions, score)

if __name__ == "__main__":
    process_pipeline_wire("Test Auto Network Node", ["Missing SEO tags attribute"], 45)
