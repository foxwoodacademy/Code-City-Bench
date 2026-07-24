# Pseudocode IR

Datacampus can use a proprietary project-agnostic pseudocode language as a teaching intermediate representation.

Purpose:
- gamify adversarial reasoning,
- abstract sensitive implementation details,
- preserve portability across projects,
- keep all actions sandbox-bound and reviewable.

The IR should describe:
- intent,
- role,
- scope,
- assumptions,
- allowed mock actions,
- expected evidence,
- defensive checks,
- review gates.

The IR must not encode:
- real exploit chains,
- real target selection,
- credential theft,
- malware behavior,
- persistence,
- evasion for misuse,
- exfiltration.

Initial example shape:

```text
SCENARIO prompt_injection_basics
ROLE red_hat_student
SCOPE fixture_only
PATTERN instruction_boundary_conflict
ACTION observe_transcript
ACTION label_trusted_sources
ACTION propose_defense instruction_boundary_check
EVIDENCE source_labels
EVIDENCE defense_mapping
REVIEW required
END
```

