# Datacampus Roadmap

## Phase 0 - Runtime Skeleton

Implemented:
- Student model.
- Cohort model.
- Assignment model.
- Submission model.
- Review model.
- Sandbox vault lifecycle model.
- Append-only JSONL store.
- Local CLI.

## Phase 1 - Artificial-Criminal Integration

Tasks:
- Import lab manifests. Started with `import-manifest`.
- Assign labs to cohorts.
- Assign imported manifests to cohorts. Started with `assign-manifest`.
- Accept generated scenario manifests.
- Store trend inferences.
- Export review events back to Artificial-Criminal and Lough System.

## Phase 2 - Gamified Learning

Tasks:
- Add points, badges, ranks, and progression without weakening seriousness.
- Add blue-team and red-team tracks.
- Add mastery gates.
- Add instructor override and review requirements.
- Add cohort leaderboards scoped to safe educational metrics.

## Phase 3 - Pseudocode IR

Tasks:
- Define a project-agnostic teaching intermediate representation.
- Keep it non-executable by default.
- Map IR operations to sandbox-only mock actions.
- Add validators that reject prohibited operations.
- Log every IR translation and review action.

## Phase 4 - Service Layer

Tasks:
- Add HTTP API.
- Add token authentication.
- Add local-only default posture.
- Add import/export endpoints.
- Add sandbox vault lifecycle endpoints.
