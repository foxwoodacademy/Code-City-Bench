"""
MarketScout: Reddit Gig Hunter.
Monitors subreddits for freelance opportunities.
"""
import praw
import logging
from typing import Dict, Any
from janebot_motherbrain.agents.base_agent import BaseAgent, AgentType

logger = logging.getLogger(__name__)

class RedditScout(BaseAgent):
    def __init__(self, client_id, client_secret, user_agent):
        super().__init__(name="RedditScout", agent_type=AgentType.SCOUT)
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    async def execute(self, capability: str, payload: Dict[str, Any]) -> Any:
        if capability == "scout":
            subreddit = payload.get("subreddit", "forhire")
            posts = []
            for submission in self.reddit.subreddit(subreddit).new(limit=10):
                posts.append({"title": submission.title, "url": submission.url})
            return posts
        return {"error": "Unsupported capability"}
