from __future__ import annotations

import time

from vault import Vault
from mediator import Mediator
import os

class NannyAgent:
    def __init__(self, vault_path, services_to_monitor):
        self.vault = Vault(vault_path)
        self.mediator = Mediator(vault_path)
        self.services = services_to_monitor

    def run(self):
        print("[Nanny] Starting health check loop...")
        while True:
            for service in self.services:
                self.check_service(service)
            time.sleep(60) # Poll every minute

    def check_service(self, service):
        print(f"[Nanny] Checking {service}...")
        status = self.mediator.get_service_status(service)
        if not status.available:
            print(f"[Nanny] ⚠️ No key for {service}")
            return

        if not status.healthy:
            print(f"[Nanny] ⚠️ {service} needs rotation or review")
            return

        print(f"[Nanny] ✅ {service} appears healthy.")

if __name__ == "__main__":
    os.environ["VAULT_MASTER_KEY"] = "user-provided-secret" # Ensure this matches initialization
    nanny = NannyAgent("/data/data/com.termux/files/home/.openclaw/vault.enc", ["NEWS_API"])
    print("Nanny agent initialized. Starting monitor loop...")
    nanny.run() 
