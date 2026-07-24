import json
import time
import ssl
import websocket # pip install websocket-client
from pathlib import Path
from typing import Optional, Callable, List

class NostrClient:
    """
    The ModMind Transport Layer.
    Handles real-time WebSocket communication with Nostr Relays.
    """
    def __init__(self, relays=None, privkey=None, pubkey=None):
        self.relays = relays or ["wss://relay.damus.io", "wss://nos.lol"]
        self.privkey = privkey
        self.pubkey = pubkey
        self.connections = {}
        self.event_handlers = []

    def connect(self):
        """Establishes connections to all configured relays."""
        for relay in self.relays:
            try:
                ws = websocket.WebSocketApp(
                    relay,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close
                )
                # Run in a separate thread to avoid blocking
                import threading
                wst = threading.Thread(target=ws.run_forever, daemon=True)
                wst.start()
                self.connections[relay] = ws
                print(f"[Nostr] Connected to {relay}")
            except Exception as e:
                print(f"[-] Failed to connect to {relay}: {e}")

    def _on_message(self, ws, message):
        """Handles incoming events from relays."""
        try:
            data = json.loads(message)
            # Nostr events are usually wrapped in a 'event' key
            event = data.get("event") if isinstance(data, dict) else data
            if event:
                for handler in self.event_handlers:
                    handler(event)
        except Exception as e:
            print(f"[-] Error parsing Nostr message: {e}")

    def _on_error(self, ws, error):
        print(f"[-] Nostr WebSocket Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print(f"[-] Nostr Connection Closed: {close_msg}")

    def add_handler(self, handler: Callable):
        """Register a callback function to handle incoming events."""
        self.event_handlers.append(handler)

    def publish(self, content: str, kind: int = 1, tags: List[str] = None):
        """
        Publishes a signed event to all relays.
        Note: In a production environment, this would use a proper 
        Schnorr signature. For now, it uses the 'ModMind Proxy' format.
        """
        event = {
            "pubkey": self.pubkey,
            "createdAt": int(time.time()),
            "kind": kind,
            "tags": tags or [],
            "content": content,
            "sig": "SIGNATURE_PROXIED" # In production, sign with self.privkey
        }
        
        payload = json.dumps({"event": event})
        for relay, ws in self.connections.items():
            try:
                ws.send(payload)
            except Exception as e:
                print(f"[-] Failed to publish to {relay}: {e}")

# Global instance
nostr = NostrClient()
