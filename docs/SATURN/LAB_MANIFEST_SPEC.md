# 📄 The Lab Manifest Specification

To ensure the Saturn Engine can autonomously audit the `labs/` directory, every project must adhere to the **Lab Manifest Standard**.

## Required: `README.md`
Every lab must contain a `README.md` at its root with the following headers:
- **Project Name**: The formal name of the experiment.
- **Purpose**: A one-sentence description of the goal.
- **Status**: (`Active` | `Stalled` | `Prototype` | `Legacy`).
- **Core Dependencies**: Key libraries required to run.

## Optional: `manifest.json`
For labs intended for integration into the ModMind Stack, a `manifest.json` is required:
```json
{
  "id": "lab-id-001",
  "version": "1.0.0",
  "integration_point": "thoth_orchestrator/modules",
  "dependencies": ["openclaw", "molt_bleak"],
  "last_audit": "2026-05-18"
}
```

## The Lab Lifecycle
1. **Incubation**: Project created in `labs/`.
2. **Validation**: Project meets the Manifest Standard and is indexed in `SATURN.md`.
3. **Promotion**: Project is merged into the core ModMind Stack.
4. **Sunset**: Project is moved to `archive/`.
