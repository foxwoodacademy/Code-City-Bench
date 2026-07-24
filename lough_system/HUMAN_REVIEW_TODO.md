# Human Review TODO

These tasks require human judgment, authorization, or project ownership decisions. They should not be delegated fully to automation.

## Policy Decisions

- Decide who is allowed to emit events into the live database.
- Decide which domains are allowed in production versus sandbox use.
- Define what counts as a high-impact event.
- Define what event types require human review before downstream use.
- Decide retention periods for raw data, derived events, analyst observations, and exports.
- Decide how to handle requests that exceed the safety boundary.

## Data Governance

- Identify every intended data source.
- Record the authorization basis for each data source.
- Define privacy constraints for movement, language, behavioral, and financial data.
- Decide whether personally identifiable data is allowed; default should be no.
- Define redaction requirements before events enter the spine.
- Define who can export the event log.

## Analyst Oversight

- Review each analyst persona prompt before use.
- Approve output schemas for observations, inferences, recommendations, and review flags.
- Create examples of unacceptable analyst claims.
- Create examples of acceptable uncertainty language.
- Decide whether analyst outputs can trigger alerts, and under what review state.

## Safety Governance

- Approve the list of high-risk domains that are allowed only for audit, simulation, compliance, or safety research.
- Define simulation boundary requirements.
- Define what must happen when a boundary is crossed.
- Identify who owns human-rights review.
- Identify who owns misuse-risk review.
- Decide how blocked escalations are reported and preserved.

## Operational Readiness

- Set up authentication or network isolation for `field_server.py`.
- Create a backup and restore procedure for `modmind.db`.
- Create a test dataset for every active domain.
- Run a tabletop review of one complete event lifecycle: ingest, analysis, review, archive.
- Create a release checklist before adding any new adapter.

## Immediate Next Human Inputs

- Name the first two real domains to operationalize.
- Pick one data source for each selected domain.
- Decide whether the first integration should be batch import, live API polling, or manual entry.
- Name the person or role responsible for approving review-required events.
- Confirm the safety boundary language in `README.md` and `ROADMAP.md`.

