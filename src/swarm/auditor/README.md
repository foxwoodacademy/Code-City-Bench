# ModMind Swarm Integrity Auditor

The silent killer of complex agentic systems isn't a crash; it's **State Divergence**. When agents operate on inconsistent versions of "truth," the system begins to hallucinate decisions that compound over time.

## 🛡️ The Auditor's Role
This service runs as a background "sidecar," continuously auditing all agent states against the global `state_truth.json`.

## ⚙️ Operational Logic
1. **Divergence Detection:** If an agent's reported state deviates from ground truth, the Auditor immediately logs an `INTEGRITY_VIOLATION`.
2. **Auto-Recovery:** The Auditor triggers the `ConciergeStateManager` to force the agent back to the correct stage/phase.
3. **Resilience:** This prevents the swarm from making decisions based on stale or conflicting data, ensuring the system remains high-fidelity over years of autonomous operation.

---
*Status: Integrated as core Swarm protection.*
