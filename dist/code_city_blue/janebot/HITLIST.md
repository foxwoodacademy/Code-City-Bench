# 🎯 Swarm Orchestration HITLIST

This document tracks the unfinished tasks for the Samsung tablet orchestration hub integration within the MkdMind ecosystem.

## 📱 MotherBrain UI/UX & Tablet Setup
*Goal: Establish the Samsung Galaxy Tab A9 5G as the intuitive 'steering' device.*

- [ ] **Shell Aliases:** Implement "one-shot" shell commands and aliases in `.bashrc` for orchestration:
    - `jane boot`: Launch Python HTTP server and open UI in Chrome.
    - `jane status`: Check swarm health and node connectivity.
    - `jane stop`: Gracefully shut down the orchestration hub.
    - `jane init`: Initialize swarm environment/configurations.
- [ ] **Dynamic UI Development:** Evolve the static `index.html` into a dynamic dashboard for real-time monitoring, log streaming, and swarm steering.
- [ ] **Environmental Hardening:**
    - [ ] Execute `termux-wake-lock` for persistence.
    - [ ] Configure Static Internal IP for the tablet.
    - [ ] Disable Android Battery Optimization for Termux.

## 🌐 Distributed Swarm Fabric (Backend)
*Goal: Transform `janebot_motherbrain` into a resilient, distributed network hub.*

- [ ] **Transport Layer (`protocols/`):**
    - [ ] Implement `protocols/security.py`: Token-based authentication and payload validation schemas.
    - [ ] Implement `protocols/websocket_bus.py`: WebSocket server/client logic and JSON serialization for `Message` objects.
- [ ] **Network-Aware Core:**
    - [ ] Update `MessageBus` to broadcast via WebSockets.
    - [ ] Update `AgentRegistry` to track remote endpoints.
    - [ ] Update `TaskQueue` for distributed task distribution.
- [ ] **Agent Client:** Create a lightweight client for remote nodes (Windows, Linux, Android) to "Phone Home" to the Hub.
- [ ] **Verification & Rigor:**
    - [ ] **Testing:** Achieve 85-95% test coverage across the network fabric.
    - [ ] **Benchmarks:** Establish rigorous performance benchmarks for latency and throughput.
    - [ ] **Adversarial Testing:** Conduct "Brown Team" destructive testing to identify failure points.
    - [ ] **7-Hat Analysis:** Apply the 7-Hat framework (White, Red, Black, Yellow, Green, Blue + Brown) to all major architectural decisions.

---
*Last Updated: 2026-05-15* (Automated by Gemini CLI)
