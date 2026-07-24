import json
import os

class StateManager:
    """
    Lightweight, file-based state manager to handle pipeline persistence.
    """
    def __init__(self, state_file="pipeline_state.json"):
        self.state_file = state_file
        if not os.path.exists(self.state_file):
            self.save_state({})

    def save_state(self, state):
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)

    def load_state(self):
        with open(self.state_file, "r") as f:
            return json.load(f)

    def update_key(self, key, value):
        state = self.load_state()
        state[key] = value
        self.save_state(state)

    def get_key(self, key):
        return self.load_state().get(key)
