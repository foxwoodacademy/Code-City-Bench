from __future__ import annotations

import json
import hashlib
import os
from base64 import b64encode
from cryptography.fernet import Fernet

class Vault:
    def __init__(self, vault_path, master_key_env_var="VAULT_MASTER_KEY"):
        self.vault_path = vault_path
        self.master_key = os.getenv(master_key_env_var)
        if not self.master_key:
            raise ValueError(f"Vault master key not found in {master_key_env_var}")
        
        # Derive key: Fernet requires 32-byte url-safe base64-encoded key
        key = hashlib.sha256(self.master_key.encode()).digest()
        self.cipher = Fernet(b64encode(key))

    def _ensure_path(self):
        os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)

    def _read_vault(self):
        if not os.path.exists(self.vault_path):
            return {}
        with open(self.vault_path, "rb") as f:
            return json.loads(self.cipher.decrypt(f.read()).decode())

    @staticmethod
    def _normalize_record(value):
        if isinstance(value, dict):
            if "encrypted_key" in value:
                record = dict(value)
                record.setdefault("meta", {})
                return record
            if "key" in value:
                return {
                    "encrypted_key": value["key"],
                    "meta": value.get("meta", {}),
                }
        return {"encrypted_key": value, "meta": {}}

    def save_key(self, service, key_data, meta=None):
        self._ensure_path()
        vault = self._read_vault()
        record = self._normalize_record(key_data)
        if meta:
            record["meta"] = {**record.get("meta", {}), **meta}
        vault[service] = record

        with open(self.vault_path, "wb") as f:
            f.write(self.cipher.encrypt(json.dumps(vault).encode()))

    def get_key(self, service):
        record = self.get_record(service)
        if record is None:
            return None
        if isinstance(record, dict):
            return record.get("encrypted_key")
        return record

    def get_record(self, service):
        vault = self._read_vault()
        value = vault.get(service)
        if value is None:
            return None
        return self._normalize_record(value)

    def list_services(self):
        return sorted(self._read_vault().keys())
