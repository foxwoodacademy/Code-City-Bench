import asyncio
import json
import logging
import os
import websockets
import aiohttp

# Setup structured logging targeting a dedicated log file
LOG_FILE = os.path.expanduser("/storage/emulated/0/RootBase/income_engine/logs/orchestrator.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("IncomeEngine")

GATEWAY_URL = "http://127.0.0.1:42617"
WS_URL = "ws://127.0.0.1:42617/ws/chat"
LEADS_PATH = os.path.expanduser("/storage/emulated/0/RootBase/income_engine/data/leads/active_leads.json")

class IncomeOrchestrator:
    def __init__(self):
        self.is_running = True

    async def connect_to_gateway(self):
        """Maintains a persistent connection to the ZeroClaw event stream."""
        while self.is_running:
            try:
                logger.info("Connecting to ZeroClaw Gateway...")
                async with websockets.connect(WS_URL) as ws:
                    logger.info("Successfully wired into ZeroClaw gateway stream.")
                    while self.is_running:
                        message = await ws.recv()
                        await self.handle_gateway_event(json.loads(message))
            except Exception as e:
                logger.error(f"Connection dropped: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

    async def handle_gateway_event(self, event):
        """Monitors stream for target data extractions."""
        if event.get("type") == "agent_completion":
            payload = event.get("payload", {})
            logger.info(f"Target Agent Finished: {payload.get('task_id')}")
            await self.pipeline_data(payload.get("result"))

    async def pipeline_data(self, raw_data):
        """Saves incoming leads to a dedicated file and executes outreach logic."""
        logger.info("Running incoming data through lead filters...")
        
        # Append lead to structured file storage
        leads = []
        if os.path.exists(LEADS_PATH):
            try:
                with open(LEADS_PATH, "r") as f:
                    leads = json.load(f)
            except Exception:
                leads = []
                
        leads.append(raw_data)
        
        with open(LEADS_PATH, "w") as f:
            json.dump(leads, f, indent=4)
        
        # Trigger automated client messaging pipeline
        await self.trigger_outreach(raw_data)

    async def trigger_outreach(self, lead):
        """Dispatches specialized prompt payload back to gateway."""
        logger.info(f"Automating outreach for lead: {lead.get('name', 'Unknown Target')}")
        endpoint = f"{GATEWAY_URL}/api/agent/task"
        
        outreach_payload = {
            "agent": "OutreachWriter",
            "prompt": f"Draft a high-specificity B2B consulting pitch for {lead.get('name')}. Identify friction points based on their listing data.",
            "stream": False
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(endpoint, json=outreach_payload) as resp:
                    if resp.status == 200:
                        logger.info(f"Outreach generation queued for {lead.get('name')}")
            except Exception as e:
                logger.error(f"Failed to execute outreach automation: {e}")

    async def start(self):
        await self.connect_to_gateway()

if __name__ == "__main__":
    orchestrator = IncomeOrchestrator()
    try:
        asyncio.run(orchestrator.start())
    except KeyboardInterrupt:
        logger.info("Engine stopped safely.")
