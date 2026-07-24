# Lough System Roadmap

This roadmap treats Lough as an event spine for decision support, simulation, audit, and analysis. It should not become an unreviewed action system.

## Current Baseline

Implemented:
- Relational event spine in `field_bridge.py`.
- HTTP gateway in `field_server.py`.
- Dynamic domain registry in `event_registry.py`.
- Plugin-style domain modules under `domains/`.
- Domain/key emission helper in `domain_bridge.py`.
- Persona cycling in `field_analyst_specialist.py`.
- File-based audit trail in `AUDIT_LOG.md`.
- Phase 1 hardening started: API access policy, event envelope, migration ledger, export tool, and unit tests.
- Phase 2 started: client onboarding endpoints and CSV ingest adapter.
- Review queue endpoints started: `GET /review` and `POST /review/<event_id>`.

Known gaps:
- API auth exists but deployment policy still needs a human-approved token and network posture.
- Event envelope exists but domain-specific validation rules are still basic.
- Migration ledger exists but does not yet support rollback migrations.
- Unit tests exist but coverage should be expanded as adapters are added.
- No reviewed policy for which non-default events require human approval.

## Phase 1 - Hardening

Goal: make the system reliable enough to trust its logs.

Tasks:
- Add an API token or local-only guard to `field_server.py`.
- Add a formal event envelope schema with `confidence`, `provenance`, `review_status`, and `created_by`.
- Add tests for `field_bridge`, `event_registry`, `domain_bridge`, and `field_server`.
- Add a migration ledger table so schema changes are recorded in SQLite.
- Add event export tooling for backup and review.

Exit criteria:
- A fresh install and an existing database both pass the same smoke tests.
- Every emitted event has provenance and review metadata.
- A human can export, inspect, and restore the event log.

## Phase 2 - Domain Adapters

Goal: connect real data sources without weakening provenance.

Candidate adapters:
- CSV ingest for markets, predictive modeling, and movement datasets. Started with `adapters/csv_ingest.py`.
- Public or authorized API ingest for air traffic and market feeds.
- Manual review forms for safety-governance events.
- Batch import for historical datasets.

Rules:
- Adapters must label source, license or authorization basis, collection time, transform time, and confidence.
- Adapters must not silently overwrite or delete events.
- High-risk domains must emit safety-governance events when boundaries, assumptions, or review requirements change.

Exit criteria:
- Each adapter has a sample input, a dry-run mode, and a rollback note.
- Each adapter emits at least one provenance-bearing test event.

Started:
- `POST /clients` creates a client entity.
- `GET /clients` lists client entities.
- `POST /clients/<id>/emit` emits client-linked events by domain/event key or raw event type.
- `adapters/csv_ingest.py` imports CSV rows as provenance-bearing events.
- `GET /review` lists review-required events.
- `POST /review/<event_id>` records review status, reviewer, and review note.

## Phase 3 - Analyst Quality

Goal: make analyst outputs useful without overstating certainty.

Tasks:
- Add analyst-specific output schemas.
- Separate observation, inference, recommendation, and required-review fields.
- Add prompt guardrails for uncertainty and non-operational boundaries.
- Add evaluator checks for unsupported claims.
- Add review queues for events that affect people, money, safety, or compliance.

Exit criteria:
- Analyst events distinguish facts from inference.
- High-impact conclusions are marked `review_required`.
- Analysts can be tested against fixed event fixtures.

## Phase 4 - Human Review Workflow

Goal: keep consequential decisions accountable.

Tasks:
- Add reviewer entities and review events.
- Add states: `unreviewed`, `needs_context`, `approved_for_analysis`, `rejected`, `archived`.
- Add a watcher or dashboard view filtered to review-required events.
- Add escalation-block events for requests outside policy.

Exit criteria:
- A human can see what needs review and why.
- Every review action is itself logged as an event.
- No high-impact workflow depends only on analyst output.

## Phase 5 - Simulation and Governance

Goal: support safety research and oversight without operationalizing harm.

Tasks:
- Keep high-risk system work in simulation, audit, compliance, and policy-review namespaces.
- Add simulation scenario entities with explicit boundaries and assumptions.
- Add misuse-risk scoring for proposed integrations.
- Add human-rights review checklists.
- Add ownership and accountability metadata to each scenario.

Exit criteria:
- Simulation events are clearly labeled and cannot be mistaken for live operations.
- Human-rights and misuse-risk checks are first-class records.
- Boundary violations emit `safety_governance.escalation.blocked`.
