import json
import os
from typing import Any, Dict

class HivemindManager:
    """
    Manages the persistent, shared state (the 'Hivemind') across different kernels and execution cycles.
    Ensures that agentic context and memory are preserved.
    """

    def __init__(self, state_file: str = "hivemind_state.json"):
        """
        Initialize the HivemindManager.

        :param state_file: The path to the JSON file where the state is stored.
        """
        self.state_file = state_file
        self._state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """
        Loads the state from the file. Creates an empty state if the file doesn't exist.
        """
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                # In a production environment, we might want to log this or handle it more gracefully
                print(f"Warning: Failed to load Hivemind state ({e}). Starting with empty state.")
                return {}
        return {}

    def save(self) -> None:
        """
        Saves the current state to the file.
        """
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self._state, f, indent=2)
        except IOError as e:
            print(f"Error: Failed to save Hivemind state ({e}).")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a value from the state.
        """
        return self._state.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Sets a value in the state.
        """
        self._state[key] = value

    def update(self, updates: Dict[str, Any]) -> None:
        """
        Updates multiple values in the state at once.
        """
        self._state.update(updates)

    def delete(self, key: str) -> None:
        """
        Removes a key from the state.
        """
        if key in self._state:
            del self._state[key]

    def clear(self) -> None:
        """
        Clears the entire state.
        """
        self._state = {}

    @property
    def current_state(self) -> Dict[str, Any]:
        """
        Returns a copy of the current state.
        """
        return self._state.copy()
