"""
GraphIntentStore - Persistence layer for NatCommand using Neo4j/Cypher graph structures.
This allows us to map the 'nuance' (nodes) and 'action' (relationships) semantically.
"""

from neo4j import GraphDatabase
import logging

logger = logging.getLogger("NatCommand.Graph")

class GraphIntentStore:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._ensure_constraints()

    def _ensure_constraints(self):
        """Create initial schema constraints."""
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT FOR (i:Intent) REQUIRE i.id IS UNIQUE IF NOT EXISTS")

    def save_intent(self, intent_obj):
        """
        Maps intent to a graph:
        (Nuance:Vibe) -[:TRIGGERS]-> (Action:SystemCommand)
        """
        cypher = """
        MERGE (n:Nuance {label: $nuance_label})
        MERGE (a:Action {name: $action_name})
        CREATE (i:Intent {id: $intent_id, raw: $raw, ts: $ts})
        CREATE (i)-[:HAS_NUANCE]->(n)
        CREATE (i)-[:EXECUTES]->(a)
        """
        with self.driver.session() as session:
            session.run(cypher, 
                        nuance_label=str(intent_obj.nuance),
                        action_name=intent_obj.action,
                        intent_id=str(intent_obj.timestamp),
                        raw=intent_obj.raw_input,
                        ts=intent_obj.timestamp)
        logger.info(f"Graph node created: {intent_obj.action} (Nuance: {intent_obj.nuance})")

    def close(self):
        self.driver.close()
