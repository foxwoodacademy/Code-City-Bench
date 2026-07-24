# Concierge: The Token & Context Master

## 1. Token-Aware Orchestration (The "Fresh Dev" Handoff)
- **Monitoring:** The Concierge tracks API usage across multiple configured accounts (Account A, B, C...).
- **Autonomous Rotation:** When an account hits a token or model limit, the Concierge triggers an automatic "State Handoff."
- **Context Handoff:**
    - Serializes current system state (Project Path, Phase, Stage).
    - Fetches the next available credential set.
    - Re-initializes the CLI/API client with the new identity.
    - Injects a "Resume Context" prompt to the new instance so the "new developer" starts fully caught up.

## 2. Hype Manbot: Proactive Industry Outreach
- **Strategy:** Position you as a "ModMind AI-Supported Developer." 
- **Outreach Mechanism:**
    - Agentic sourcing of high-impact engineering leads (not just general jobs).
    - Personalized outreach that highlights your agentic toolkit (the RootBase stack).
    - Acts as a verifiable reference system: It can demonstrate your capabilities by performing audits, generating architectural solutions, or providing proof-of-work directly to prospective companies.
