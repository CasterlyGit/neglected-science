# Contributing

Contributions should improve inspectability without overstating what the tool proves.

Before opening a pull request:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python scripts/release_gate.py
```

Rules:

- do not convert the F/E/V profile into one trust score
- do not call a reproducible run scientifically correct solely because it replays
- do not weaken claim uncertainty, limitation, privacy, or clinical-boundary checks for convenience
- retain negative results and failed validation gates
- do not fabricate evidence, validation, expert review, or standards conformance
- adapters must translate captured facts, not infer missing provenance
- new domain profiles require a documented scientific rationale and adversarial fixture

Small deterministic rules with explicit remediation are preferred to opaque model-based grading.