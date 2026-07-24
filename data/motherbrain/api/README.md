# 🌳 MotherBrain Swarm API Ecosystem

A decentralized, recursive self-improvement AI swarm architecture running locally on Android via Termux. The ecosystem leverages automated iteration loops, file-based data transit routing, and access-restricted runtime personas.

## 📁 Ecosystem Blueprint

* `swarm_bus.py` - The central communications highway. Employs a zero-dependency JSONL file-queue network for inter-process telemetry and message routing.
* `comms_bridge.py` - The human-to-swarm flight deck. Allows the operator to poll incoming agent requests or issue system-wide `buzz` overrides.
* `persona_engine.py` - The cognitive morphing layer. Securely segments and wraps tasks within distinct behavioral lenses (Tiers 1–3).
* `SWARM_PROTOCOLS.md` - The engineering ruleset governing path independence, headless behavior, and fail-safe operation.

## 🛡️ Secure Architecture Segmentation

The ecosystem enforces a rigorous access matrix to insulate core systemic logic from public interaction surfaces:

1.  **Tier 1 (Public & UI Interface):** `EquiNex` (Anonymity/UX), `Askhole` (Blunt Onboarding), `NME` (Rapping Node).
2.  **Tier 2 (Sentry & Optimization):** `TruthSleuth` (Code Cleansing Matrix).
3.  **Tier 3 (Restricted Executive Counsel):** `EquiLex` (Procedural/Legal Strategy), `ModMind` (Core Analytics Gateway).
4.  **Tier 0 (The Brown Team Matrix):** An isolated, off-the-books analytical sanctuary completely physically sandboxed inside Termux internal home files.

## 🕹️ Operator Quick-Launch Directives

### Check Inbound Swarm Mail
```bash
python3 comms_bridge.py

