# Architecture: Key-Handoff System

## Core Components

### 1. The Vault (Encrypted Manifests)
Stores key data: `{"service": "...", "key": "ENC_DATA", "meta": {"expires_at": "...", "rate_limit_bucket": "..."}}`.
The Vault uses local AES-256 encryption. Master keys are derived from machine-specific hardware IDs.

### 2. The Rotator (Nanny Agent)
An independent background process that:
1. Audits keys in the Vault.
2. Performs proactive health checks (e.g., `/v1/models` check for LLM APIs).
3. Executes rotation via browser/API when nearing expiry or detecting failure.

### 3. The Mediator (Middleware)
The interface for SaaS packages.
```javascript
const handle = await Mediator.getHandle('service-name');
// ... use handle
```

The mediator now also supports:
- `getHandles([...])` for batch resolution
- `getServiceStatus(name)` for availability/expiry checks
- `refresh(name)` to clear cached records
- environment-backed fallback when no vault is available

## Failure Scenarios (Fail-Safe)
- **Mediator Error:** If the Mediator fails, SaaS services must throw a `CredentialRetrievalError`, which triggers a circuit breaker at the application level.
- **Rotation Failure:** If a key rotation fails, the Nanny Agent attempts back-off and alerts the system operator via the `Pipeline Observability Bridge`.
