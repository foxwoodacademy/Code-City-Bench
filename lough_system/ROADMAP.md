# Lough System Roadmap

## Current Version: v0.1 (Event Spine)
- [x] HTTP API for emitting and polling events.
- [x] Review queue for human/agent audit.
- [x] Client entity management.

## Phase 2: The Truth Engine (v0.2)
- [ ] **Automated Verification:** Use "Verifier Agents" to automatically check evidence against the task requirements.
- [ ] **Event Correlation:** Automatically link 'Invoice Paid' $
ightarrow$ 'Task Started' $
ightarrow$ 'Result Submitted' into a single 'Lifecycle Trace'.
- [ ] **Advanced Analytics:** Generate 'Swarm Health' reports based on event frequency and error rates.

## Phase 3: The ModMind Ledger (v0.3)
- [ ] **Zk-Proofs:** Implement zero-knowledge proofs so customers can verify their work was done without seeing the worker's private methods.
- [ ] **Public Mirror:** Mirror a sanitized version of the event spine to a public Nostr relay for transparency.
- [ ] **Immutable Archiving:** Export long-term logs to decentralized storage (IPFS/Arweave).
