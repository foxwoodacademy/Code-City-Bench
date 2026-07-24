# 🌌 Lough System: The Event Spine & Intelligence Framework

The Lough System is a high-performance event-driven architecture designed to bridge raw data streams from diverse sources into a unified, relational intelligence graph. It is specifically tuned for **Behavioral Science** and **Defense Industrial Base (DIB)** analysis.

## 📁 Project Structure

### ⚙️ Core Infrastructure
- `field_bridge.py`: The "Spine". Handles all interactions with the SQLite database. 
    - **New Feature**: Relational Graph support via `field_entities` table.
- `event_registry.py`: The "Dictionary". Defines the formal namespaces for all events to ensure data consistency across domains.
- `field_server.py`: The "Gateway". A Flask API (Port 7070) that allows remote agents to emit and poll events. Includes meta-logging for system health.
- `domain_bridge.py`: Convenience helpers for emitting events by `domain` and `event_key`.
- `event_envelope.py`: Standard `_lough` metadata envelope for provenance, confidence, review status, and creator identity.
- `export_events.py`: JSON Lines export tool for backup and review.
- `domains/`: Plugin-style domain modules for predictive modeling, markets, movement, air traffic, text behavior, and safety governance.
- `ROADMAP.md`: Forward plan for hardening, adapters, analyst quality, review workflow, and governance.
- `HUMAN_REVIEW_TODO.md`: Human-owned decisions and approval tasks.
- `CLIENT_SERVICE_SETUP.md`: Low-cost client onboarding and service operation guide.
- `AUDIT_LOG.md`: File-based change ledger for backtracking when git metadata is unavailable.

### 🧠 Intelligence Layer
- `field_analyst_specialist.py`: The "Brain". A persona-driven AI agent that cycles between **Behavioral Analysis** and **Defense Procurement Analysis** using OpenRouter.
- `field_analyst.py`: A legacy, single-purpose event summarizer.

### 🖥️ Interface & Integration
- `field_watcher.py`: The "Monitor". A real-time, color-coded CLI feed for human observation.
- `patch_code_city.py`: The "Injector". Patches `code_city.html` on the SD card to display a live, integrated field event feed.

---

## 🚀 Quick Start Guide

### 1. Setup Environment
Ensure you have the required dependencies and API keys:
```bash
pip install requests flask
export OPENROUTER_API_KEY="your_key_here"
```

### 2. Launch the Stack
Run these in separate terminals (or in the background):
```bash
# Optional: require token auth for remote clients
export LOUGH_API_TOKEN="choose-a-strong-token"

# Start the API Gateway
python ~/lough_system/field_server.py &

# Start the AI Analyst
python ~/lough_system/field_analyst_specialist.py &

# Start the Live Monitor
python ~/lough_system/field_watcher.py
```

### 2a. Client Setup Endpoint
Create a client entity before importing or emitting client-scoped events:

```bash
curl -X POST http://127.0.0.1:7070/clients \
  -H "Content-Type: application/json" \
  -H "X-Lough-Token: $LOUGH_API_TOKEN" \
  -d '{"name":"Pilot Client","metadata":{"tier":"pilot"}}'
```

Then emit client-linked events:

```bash
curl -X POST http://127.0.0.1:7070/clients/1/emit \
  -H "Content-Type: application/json" \
  -H "X-Lough-Token: $LOUGH_API_TOKEN" \
  -d '{"domain":"markets","event_key":"trend_signal","payload":{"symbol":"EXAMPLE","confidence_note":"demo"}}'
```

### 3. Integrated Dashboard
To see events inside your Code City visualizer:
```bash
python ~/patch_code_city.py
# Then open /storage/ED7B-AD5A/root_2026/code_city.html in Chrome
```

---

## 🧬 Advanced Usage: The Relational Graph

The system now supports **Entities**. Instead of just logging an event, you can link it to a specific actor or contract.

### Creating an Entity
Use `field_bridge.create_entity(type, name, metadata)` to establish a tracking ID.
```python
import field_bridge
# Create a specific defense contract entity
contract_id = field_bridge.create_entity("contract", "SOW-2024-HYPER", {"prime": "Lockheed"})
```

### Emitting a Linked Event
Pass the `relation_id` to `field_bridge.emit()` to link the event to that entity.
```python
field_bridge.emit(
    event_type="dib.milestone.performance",
    location="lab_01",
    source="sensor_net",
    relation_id=contract_id, 
    payload={"status": "passed", "test": "thermal_stress"}
)
```

### Polling by Entity
Query only the events associated with a specific relation.
```python
events = field_bridge.poll(relation_id=contract_id)
```

---

## 🗺️ Domain Namespaces
Refer to `event_registry.py` and `domains/` for the full list. The API also exposes `/registry`.

| Domain | Primary Namespace | Focus |
| :--- | :--- | :--- |
| **Behavioral** | `behavior.*` | Intent, cognitive biases, and mental model shifts. |
| **Defense** | `dib.*` | Contract lifecycles, CMMC compliance, and fiscal appropriations. |
| **System** | `system.*` | Server usage, error logs, and analyst observations. |
| **Predictive** | `predictive.*` | Model training, scoring, drift, and validation. |
| **Markets** | `markets.*` | Price ticks, volatility, trend signals, and risk alerts. |
| **Movement** | `movement.*` | Authorized or aggregate path indexing and privacy review. |
| **Air Traffic** | `air_traffic.*` | Track observation, route patterns, congestion, and deconfliction. |
| **Text Behavior** | `text_behavior.*` | Language-pattern shifts with explicit uncertainty flags. |
| **Safety Governance** | `safety_governance.*` | Audit, human-rights, simulation-boundary, and misuse-risk events. |

### Emitting by Domain
Use `domain_bridge.emit_domain_event()` when an application knows the domain and event key but should not hardcode namespace strings.

```python
import domain_bridge

domain_bridge.emit_domain_event(
    domain="markets",
    event_key="trend_signal",
    location="market.feed",
    source="csv_ingest",
    payload={"symbol": "EXAMPLE", "direction": "up", "confidence": 0.72}
)
```

High-risk systems should use the `safety_governance` namespace for audit, simulation-boundary, human-rights, accountability, and misuse-risk tracking. The project should not encode operational targeting, area-denial execution, or autonomous harm orchestration.

### Event Envelope
Every emitted payload is normalized with a `_lough` metadata block:

```json
{
  "_lough": {
    "schema_version": 1,
    "created_at": 1715560000.0,
    "created_by": "source_name",
    "confidence": 0.72,
    "provenance": {"source": "authorized_feed"},
    "review_status": "unreviewed"
  }
}
```

`safety_governance.*`, `movement.*`, and `text_behavior.*` default to `review_required`.

### Exporting Events
```bash
python ~/lough_system/export_events.py --limit 500 > lough_events.jsonl
```

### Review Queue
List events that require review:

```bash
curl http://127.0.0.1:7070/review \
  -H "X-Lough-Token: $LOUGH_API_TOKEN"
```

Update a reviewed event:

```bash
curl -X POST http://127.0.0.1:7070/review/123 \
  -H "Content-Type: application/json" \
  -H "X-Lough-Token: $LOUGH_API_TOKEN" \
  -d '{"review_status":"approved_for_analysis","reviewed_by":"operator_name","review_note":"checked source and scope"}'
```

### CSV Ingest
Phase 2 starts with offline CSV ingestion:

```bash
python ~/lough_system/adapters/csv_ingest.py ./sample.csv \
  --domain markets \
  --event-key price_tick \
  --relation-id 1 \
  --dry-run
```

Remove `--dry-run` to emit events.
