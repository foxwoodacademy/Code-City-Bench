import json
import os
from jsonschema import validate
from path_resolver import resolver

class EcosystemBridge:
    def __init__(self, broadcast_dir=None):
        if broadcast_dir is None:
            broadcast_dir = resolver.resolve("ecosystem_bridge")
        self.broadcast_dir = broadcast_dir
        if not os.path.exists(self.broadcast_dir):
            os.makedirs(self.broadcast_dir)

    def broadcast_insight(self, topic, data):
        """Broadcasts validated data to the ecosystem."""
        # Simple schema: enforce that data is a dict
        schema = {"type": "object"}
        try:
            validate(instance=data, schema=schema)
        except Exception as e:
            raise ValueError(f"Invalid data structure: {e}")

        file_path = os.path.join(self.broadcast_dir, f"{topic}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"📡 Broadcasted insight on '{topic}' to ecosystem.")

# Singleton instance for the pipeline to use
bridge = EcosystemBridge()
