# Key-Handoff System

## Overview
The Key-Handoff System is a high-availability infrastructure component designed to transition API credential management from static, insecure `.env` files to a dynamic, rotatable, and fault-tolerant architecture.

## Principles
1. **Transient Credentials:** Keys have limited lifespans and are treated as replaceable assets.
2. **Mediator-Only Access:** Application logic NEVER interacts with raw credentials; it requests a service handle from the Mediator.
3. **Fail-Safe Operation:** If the Mediator cannot provide a healthy key, the system MUST default to a pre-defined safe state (e.g., pause, alert, switch to secondary provider).

## Documentation
- [Architecture Design](./docs/ARCHITECTURE.md)
- [Threat Model](./docs/THREAT_MODEL.md)

## Usage
*See [ARCHITECTURE.md](./docs/ARCHITECTURE.md) for implementation details and integration instructions.*

## Installer

Run `./install.sh` from this directory to validate the Python dependency chain and create an example mediator env file.
Use `./install.sh --seed` only if `VAULT_MASTER_KEY` is already set and you want an empty encrypted vault initialized at `VAULT_PATH`.
