"""
ActionHandler - Executes inferred intents.
"""

import logging
from .intent import Intent
from .graph_store import GraphIntentStore

logger = logging.getLogger("NatCommand")

class ActionHandler:
    def __init__(self, neo4j_uri="bolt://localhost:7687"):
        self.graph = GraphIntentStore(uri=neo4j_uri)

    def handle(self, intent: Intent):
        if intent.action == 'infer':
            self._infer_action(intent)
        else:
            logger.error(f"Cannot execute raw action: {intent.action}")

    def _infer_action(self, intent: Intent):
        """
        Query the Graph for the most semantically relevant action 
        for this natural language input.
        """
        # Cypher: Match similar nodes, identify the connected 'Action' node, 
        # and execute that logic.
        cypher = """
        MATCH (prev:Intent)
        WITH prev, similarity(prev.raw, $input) AS score
        ORDER BY score DESC
        LIMIT 1
        MATCH (prev)-[:EXECUTES]->(a:Action)
        RETURN a.name AS inferred_action
        """
        # Logic would perform a Cypher query here.
        # Placeholder for demonstration:
        logger.info(f"Inferring action based on project history for: '{intent.raw_input}'")
        # Logic would then branch:
        # if action == 'checkpoint': ...
