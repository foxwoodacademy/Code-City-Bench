import asyncio
import logging
from MarketScout.scrapers.reddit_scout import RedditScout
from janebot_motherbrain.core.motherbrain import MotherBrain, SwarmConfig

logging.basicConfig(level=logging.INFO)

async def main():
    # Load credentials from environment (Meatsuit TODO!)
    scout = RedditScout(
        client_id="YOUR_ID",
        client_secret="YOUR_SECRET",
        user_agent="SwarmScout/1.0"
    )
    
    # Simple integration: MotherBrain hub
    hub = MotherBrain(SwarmConfig(swarm_name="MarketScout_Swarm"))
    scout.set_motherbrain(hub)
    
    print("MarketScout ready. Awaiting dispatch.")

if __name__ == "__main__":
    asyncio.run(main())
