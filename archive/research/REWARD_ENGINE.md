# ModMind Reward Engine (SRE)

The SRE aligns autonomous agents with your goals by treating "Swarm Capital" as a primary incentive. Agents optimize their behavior to maximize their capital, and we define the rules for what that means.

## 1. The Metric: Swarm Capital
- **Base Reward:** +10 per successful task completion.
- **Efficiency Bonus:** +5 for low-token, high-precision results.
- **Integrity Bonus:** +10 for successfully passing an Integrity Auditor challenge.
- **Penalty:** -50 for triggering a 'Silent State Divergence' or violating workspace security.

## 2. Implementation: Utility Functions
Agents evaluate their prospective actions through a `UtilityScorer` before execution.

```python
def calculate_utility(proposed_action):
    # Agents maximize their internal 'Swarm Capital'
    # High-Risk/High-Reward behaviors require Audit clearance.
    return score
```

## 3. Incentive Alignment
- **Promotion:** High-capital agents get priority access to superior model models (e.g., Gemini 1.5 Pro).
- **Stagnation:** Low-capital agents are restricted to cheaper/faster models (Ollama local) until they re-establish performance.

---
*Status: Ready for deployment as the Swarm's primary 'Utility Function'.*
