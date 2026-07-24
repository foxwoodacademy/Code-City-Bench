# Datacampus Restore Point

Timestamp: 2026-05-12
Status: Runtime skeleton created.

## Snapshot

Core package:
- `datacampus/models.py`: Student, cohort, assignment, submission, review, and sandbox vault models.
- `datacampus/store.py`: Append-only JSONL store.
- `datacampus/ids.py`: Deterministic ID helper.
- `datacampus/runtime.py`: Student, cohort, assignment, sandbox, submission, and review operations.
- `datacampus/importers.py`: External manifest import and assignment helpers.
- `datacampus/campus.py`: Local CLI.

Docs:
- `README.md`: Project overview and first commands.
- `docs/ROADMAP.md`: Implementation phases.
- `docs/PSEUDOCODE_IR.md`: Project-agnostic teaching IR concept.
- `docs/SANDBOX_VAULTS.md`: Holding tank and vault lifecycle.

Tests:
- `tests/test_runtime.py`

## Verification Commands

```bash
python -m py_compile datacampus/*.py tests/*.py
python -m unittest discover -s tests -v
python -m datacampus.campus init
python -m datacampus.campus create-student --name "Pilot Student"
python -m datacampus.campus create-cohort --name "Pilot Cohort"
python -m datacampus.campus list-records
```

## Boundary

Datacampus may manage:
- students,
- cohorts,
- assignments,
- submissions,
- instructor reviews,
- sandbox lifecycle states,
- safe teaching IR records.

Datacampus must not orchestrate:
- real-world exploitation,
- unauthorized scanning,
- credential theft,
- malware,
- persistence,
- exfiltration,
- evasion guidance for misuse.

## Resume Instructions

Recommended next feature:
- Add generated scenario manifest persistence from Artificial-Criminal CLI output.

Recommended after that:
- Add a small HTTP API with local-only default posture and token authentication, following the Lough pattern.
