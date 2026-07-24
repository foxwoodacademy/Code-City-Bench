import time
import os
import sys
import logging
from thoth_core import ThothCore
from thoth_adapters import lough

# Setup logging for the daemon
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/storage/emulated/0/RootBase/thoth_orchestrator/daemon.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("ModMindDaemon")

class ModMindDaemon:
    def __init__(self):
        logger.info("Initializing ModMind Daemon...")
        self.thoth = ThothCore()
        self.running = True
        
        # Event mapping: Event Type -> ThothCore Method
        self.event_map = {
            "payment.verified": self._handle_payment_verified,
            "scout.lead.found": self._handle_new_lead,
            "swarm.error": self._handle_swarm_error,
            "revenue.push.requested": self._handle_revenue_request
        }
        
        logger.info("Daemon operational. Listening to the Loom Mesh...")

    def _handle_payment_verified(self, payload):
        payment_id = payload.get("payment_id")
        customer_id = payload.get("customer_id")
        amount = payload.get("amount")
        if payment_id and customer_id:
            logger.info(f"Event: Payment Verified ({payment_id}). Triggering Loop...")
            self.thoth.verify_and_unlock(payment_id, customer_id, amount)
        else:
            logger.error("Payment verified event received with missing payload data.")

    def _handle_new_lead(self, payload):
        platform = payload.get("platform", "Nostr")
        logger.info(f"Event: New Lead found on {platform}. Triggering Revenue Funnel...")
        self.thoth.generate_revenue(platform=platform)

    def _handle_swarm_error(self, payload):
        error_msg = payload.get("error", "Unknown error")
        logger.error(f"Event: Swarm Error detected: {error_msg}. Initiating self-healing...")
        # Self-healing logic could go here (e.g., restarting services)
        self.thoth.swarm_audit()

    def _handle_revenue_request(self, payload):
        platform = payload.get("platform", "Nostr")
        logger.info(f"Event: Revenue push requested for {platform}.")
        self.thoth.generate_revenue(platform=platform)

    def run(self):
        """Main event loop."""
        try:
            while self.running:
                # Poll the Lough Event Spine
                events = lough.poll(limit=5)
                
                if isinstance(events, list):
                    for event in events:
                        event_type = event.get("event_type")
                        payload = event.get("payload", {})
                        
                        if event_type in self.event_map:
                            logger.info(f"Processing event: {event_type}")
                            self.event_map[event_type](payload)
                elif "error" in str(events):
                    logger.warning(f"Lough poll error: {events}")
                
                # Sleep to prevent CPU pegging
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info("Daemon shutting down via KeyboardInterrupt.")
            self.running = False
        except Exception as e:
            logger.critical(f"Daemon crashed: {e}", exc_info=True)
            self.running = False

if __name__ == "__main__":
    daemon = ModMindDaemon()
    daemon.run()
