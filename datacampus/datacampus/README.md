# Datacampus

Datacampus is the educational runtime for agentic security training. It owns students, cohorts, assignments, submissions, reviews, and sandbox lifecycle records. It is designed to integrate with Artificial-Criminal as a lab and scenario provider.

Datacampus is local-first, auditable, and sandbox-oriented. It should not run uncontrolled offensive actions or real-world target operations.

## Responsibilities

- Manage student and instructor identities.
- Manage cohorts and lab assignments.
- Receive lab manifests from Artificial-Criminal.
- Record submissions and reviews.
- Track sandbox holding tanks and vault lifecycle states.
- Export auditable JSONL records.

## First Commands

```bash
python -m py_compile datacampus/*.py tests/*.py
python -m unittest discover -s tests -v
python -m datacampus.campus init
python -m datacampus.campus create-student --name "Pilot Student"
python -m datacampus.campus create-cohort --name "Pilot Cohort"
python -m datacampus.campus import-manifest ../Artificial-Criminal/labs/prompt_injection_basics.json
python -m datacampus.campus list-records
```

## Boundary

Datacampus may orchestrate:
- sandbox assignments,
- mock lab lifecycle,
- evidence collection,
- review gates,
- educational scoring,
- audit logs.

Datacampus must not orchestrate:
- real-world exploitation,
- unauthorized scanning,
- credential theft,
- malware,
- persistence,
- exfiltration,
- evasion guidance for misuse.
