# Integration guide

## Adapter boundary

An adapter should translate a system's native execution record into a FEVKit bundle without rewriting scientific history. It may normalize identifiers and copy or reference artifacts, but it must not invent missing tools, parameters, versions, evidence, uncertainty, human review, or validation.

## Minimum adapter output

1. system name and exact version
2. bounded run objective
3. ordered steps mapped to F1–F6
4. tool name, version, and parameters for every F3 step
5. declared inputs and artifacts with hashes
6. evidence records with source versions and selections
7. claims with typed support edges, uncertainty, and limitations
8. environment and replay declaration
9. privacy attestation
10. validation evidence and human checkpoints

## Python SDK

```python
from fevkit import RunRecorder

recorder = RunRecorder(
    "my-run",
    run_id="run-2026-001",
    title="Bounded analysis",
    objective="Test one predeclared computational question.",
    domain="biomedical-research/example",
    system_name="my-agent",
    system_version="1.2.3",
)
```

Run `fevkit audit my-run` after recording. The SDK records declarations; the audit verifies them.

The first external adapter should be selected with an upstream maintainer who is willing to review a real sanitized mapping. A speculative adapter is lower priority than a narrow co-designed adapter.