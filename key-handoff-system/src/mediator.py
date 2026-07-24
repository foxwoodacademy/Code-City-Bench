from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from vault import Vault


class CredentialRetrievalError(RuntimeError):
    pass


@dataclass
class ServiceStatus:
    service: str
    available: bool
    healthy: bool
    source: str | None = None
    expires_at: str | None = None
    status: str | None = None


class Mediator:
    def __init__(self, vault_path="/data/data/com.termux/files/home/.openclaw/vault.enc", env_prefix=""):
        try:
            self.vault = Vault(vault_path)
        except Exception:
            self.vault = None
        self.env_prefix = env_prefix
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _env_candidates(self, service_name: str) -> Iterable[str]:
        normalized = service_name.upper().replace("-", "_").replace(" ", "_")
        prefix = f"{self.env_prefix}_" if self.env_prefix else ""
        yield f"{prefix}{normalized}"
        yield f"{prefix}{normalized}_KEY"
        yield f"{prefix}{normalized}_TOKEN"

    def _parse_expires_at(self, value: Optional[str]) -> Optional[datetime]:
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                return parsed.replace(tzinfo=timezone.utc)
            return parsed
        except Exception:
            return None

    def _record_to_handle(self, service_name: str, record: Any, source: str) -> Dict[str, Any]:
        if isinstance(record, dict):
            handle = record.get("encrypted_key") or record.get("key") or record.get("value")
            meta = record.get("meta", {})
        else:
            handle = record
            meta = {}
        return {
            "service": service_name,
            "handle": handle,
            "meta": meta,
            "source": source,
        }

    def _fetch_from_vault(self, service_name: str):
        if self.vault is None:
            return None
        record = self.vault.get_record(service_name)
        if not record:
            return None
        return self._record_to_handle(service_name, record, "vault")

    def _fetch_from_env(self, service_name: str):
        for candidate in self._env_candidates(service_name):
            value = os.getenv(candidate)
            if value:
                return self._record_to_handle(service_name, value, f"env:{candidate}")
        return None

    def _resolve(self, service_name: str):
        if service_name in self._cache:
            return self._cache[service_name]

        record = self._fetch_from_vault(service_name) or self._fetch_from_env(service_name)
        if not record:
            return None

        self._cache[service_name] = record
        return record

    def get_handle(self, service_name, default=None, require_healthy=False, include_meta=False):
        record = self._resolve(service_name)
        if not record:
            if default is not None:
                return default
            raise CredentialRetrievalError(f"No valid key found for service: {service_name}")

        status = self.get_service_status(service_name, record=record)
        if require_healthy and not status.healthy:
            raise CredentialRetrievalError(f"Service handle for {service_name} is not healthy")

        if include_meta:
            return record
        return record["handle"]

    def get_handles(self, service_names, include_meta=False, require_healthy=False):
        resolved = {}
        for service_name in service_names:
            resolved[service_name] = self.get_handle(
                service_name,
                include_meta=include_meta,
                require_healthy=require_healthy,
            )
        return resolved

    def get_service_status(self, service_name, record=None):
        record = record or self._resolve(service_name)
        if not record:
            return ServiceStatus(service=service_name, available=False, healthy=False)

        meta = record.get("meta") or {}
        expires_at = meta.get("expires_at")
        expiry = self._parse_expires_at(expires_at)
        expired = bool(expiry and expiry <= datetime.now(timezone.utc))
        status = meta.get("status") or ("expired" if expired else "active")
        healthy = bool(record.get("handle")) and not expired and status == "active"
        return ServiceStatus(
            service=service_name,
            available=True,
            healthy=healthy,
            source=record.get("source"),
            expires_at=expires_at,
            status=status,
        )

    def list_services(self):
        services = set(self.vault.list_services()) if self.vault is not None else set()
        for name in services:
            yield name

    def refresh(self, service_name=None):
        if service_name is None:
            self._cache.clear()
        else:
            self._cache.pop(service_name, None)


if __name__ == "__main__":
    os.environ["VAULT_MASTER_KEY"] = "super-secret-key"
    m = Mediator()
    try:
        print(m.get_service_status("NEWS_API"))
    except Exception as e:
        print(f"Caught expected error: {e}")
