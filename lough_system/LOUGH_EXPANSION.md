# Lough System Expansion: Multi-Domain Intelligence

The Lough System is evolving from a generic event spine into a multi-layered intelligence framework. It now supports a core event spine, a relational graph, plugin-style domains, domain personas, and safety-governance events.

---

## 1. The Cognitive Layer (Behavioral Science)

**Objective:** Transition from observing *actions* to inferring *intent and cognitive states*.

This layer treats events not just as data points, but as indicators of underlying psychological or behavioral models.

### Event Taxonomy
| Event Type | Description | Example Payload |
| :--- | :--- | :--- |
| `intent.observed` | An inferred goal based on event sequences. | `{"goal": "resource_accumulation", "confidence": 0.85}` |
| `pattern.cognitive_bias` | Detection of biased decision-making. | `{"bias": "loss_aversion", "trigger": "budget_cut"}` |
| `state.mental_model` | The current understanding of the world held by an agent. | `{"model_version": "2.1", "assumptions": ["market_stability"]}` |
| `behavior.deviation` | An action that contradicts established patterns. | `{"expected": "routine_maintenance", "actual": "rapid_expansion"}` |

### Analysis Logic
The `field_analyst.py` will be specialized via prompt engineering to act as a **Behavioral Profiler**, looking for "Cognitive Signatures" in the event stream.

---

## 2. The Industrial Layer (Defense & Subcontracting)

**Objective:** Model the lifecycle, risk, and opportunity of a **Non-Prime Entity** operating within the Defense Industrial Base (DIB).

This layer focuses on the "Subcontractor's Reality": navigating the complex, high-friction, and highly regulated lifecycle of defense spending.

### Event Taxonomy
| Event Type | Description | Example Payload |
| :--- | :--- | :--- |
| `contract.lifecycle` | Movements through the procurement phases. | `{"phase": "RFP", "vehicle": "OTA", "prime": "Lockheed"}` |
| `compliance.requirement` | Triggers related to regulatory adherence (CMMC, ITAR). | `{"standard": "CMMC-L2", "status": "audit_pending"}` |
| `fiscal.appropriation` | Shifts in available budget/funding levels. | `{"program": "hypersonics", "change": "+5%", "source": "congress"}`
| `milestone.performance` | Execution of contract-specific obligations. | `{"milestone": "PDR", "status": "complete"}` |

### Strategic Intelligence
The system will monitor the "friction" between Primes and Subs, identifying:
* **Dependency Risks:** Heavy reliance on a single Prime's contract vehicle.
* **Regulatory Bottlenecks:** Patterns of compliance failures delaying milestones.
* **Budgetary Drift:** Aligning macro-level defense spending trends with micro-level subcontractor performance.

---

## Implementation Roadmap

Completed:
1. **Registry:** `event_registry.py` defines core namespaces and dynamically loads plugin domains.
2. **Analyst Specialization:** `field_analyst_specialist.py` cycles through core and plugin-provided personas.
3. **Relational Graph:** `field_bridge.py` links events to entities through `relation_id`.
4. **Domain Plugins:** `domains/` contains predictive, market, movement, air-traffic, text-behavior, and safety-governance modules.

Next:
- See `ROADMAP.md` for the forward implementation plan.
- See `HUMAN_REVIEW_TODO.md` for decisions that require human ownership.
- See `AUDIT_LOG.md` for backtracking notes and verification history.
