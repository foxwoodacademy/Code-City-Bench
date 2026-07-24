# MotherBrain Swarm Architecture Protocols

This document establishes the binding execution constraints for all current and future modular assets running inside the /storage/emulated/0/RootBase architecture.

## 1. Absolute Path Independence
* All modules must use full absolute anchor mapping structures. 
* Never rely on local terminal relative execution context path vectors (`./`).

## 2. Headless Isolation Policy
* Visual terminal graphic updates (like clearing terminal views) must remain strictly decoupled.
* Modules must natively support a `--headless` execution matrix. When detached from a standard visual interactive terminal, text processing engines must only emit clean, structured JSON streams.

## 3. Strict Fail-Safe Degradation
* Scripts must leverage safe internal fallback patterns. If a network configuration fails or an external cloud-facing utility drops offline, the process must immediately drop down to local on-device processing capabilities (such as your offline Ollama or local storage matrix tools) instead of causing a hard execution crash.

## 4. Central Registry System
* Any asset running in the background must actively utilize the centralized communication highway (`swarm_bus.py`).
* Nodes must maintain a visible manifest profile, detailing active state, execution PID, and current workload postures.

## 5. Clean Communication Integrity
* Inter-project messaging must follow standard payload definitions:
  - Sender Origin Identity
  - Global Microsecond Timestamp
  - Unified Event Flag Category
  - Nested Context Variables Dictionary
