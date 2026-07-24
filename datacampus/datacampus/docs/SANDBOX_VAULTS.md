# Sandbox Vaults

Sandbox vaults are lifecycle records for holding tanks used in training.

States:
- `created`
- `assigned`
- `active`
- `frozen`
- `reviewed`
- `archived`
- `destroyed`

Rules:
- Every sandbox must be tied to an assignment.
- Every sandbox has allowed and prohibited actions.
- Every transition must include a reason.
- Destroying a sandbox means recording the destruction state and removing or invalidating runtime access.
- Evidence and audit records should survive sandbox destruction.

