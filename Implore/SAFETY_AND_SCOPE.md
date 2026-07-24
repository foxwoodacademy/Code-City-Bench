# IMPLORE: SAFETY & SCOPE ARCHITECTURE

## 1. Safety Guardrails (Safety-by-Design)
- **Constraint Layer:** All generated content must pass a safety validation node *before* audit.
- **Harmful Content Filtering:** Deny generation if inputs relate to:
    - Weaponization/Illegal activities
    - Fraud/Deception
    - Violations of federal grant compliance rules
- **Attribution Enforcement:** Strictly link every paragraph of the narrative to an identified project feature. If a claim cannot be linked, reject generation.

## 2. Scope Expansion: "Grant Intelligence" Platform
Implore is now generalized for any high-stakes, structured business proposal:
- **Federal/State Grants**: Existing SF-424 pipeline.
- **Academic Research**: Specialized NSF/NIH/Horizon Europe narrative templates.
- **Small Business/Startup**: SBIR/STTR phase tracking; investment pitch generation.
- **Non-Profit**: Donor-fit matching and narrative alignment for 990-driven solicitations.

## 3. Implementation of Safety Node
- A dedicated LangGraph `SafetyNode` is added *before* the Generation Node.
- It validates the `opportunity` and the `profile_data` against a blacklist of forbidden use cases.
