# FEVKit 0.1 run specification

## Design invariant

Function, Evidence, and Validation are separate axes. A workflow may have broad capability but weak evidence, strong provenance but invalid science, or reproducible execution without prospective validation. The manifest must preserve those distinctions.

## Function classes

- `F1` planning and task decomposition
- `F2` role specialization and coordination
- `F3` tool selection and execution
- `F4` workflow-state and trace capture
- `F5` self-evaluation and repair
- `F6` verification and escalation

A Function class is present only when at least one step declares it. It is complete only when that declaration has no Function-scoped audit error. Presence is not evidence of correctness.

## Evidence classes

- `E1` scientific literature
- `E2` structured biological knowledge
- `E3` biological data
- `E4` software and statistical outputs
- `E5` scientific-model outputs
- `E6` experimental or clinical observations

Evidence records require a retrieval time, a source title, class-specific versioning fields, and resolvable artifact links when artifacts are cited.

## Claims

Every claim declares a kind, risk, typed support edges, uncertainty, limitations, rationale for inferential claims, and producing steps. Supported edge relations are `supports`, `calculated_from`, `observed_in`, `derived_from`, `contradicted_by`, and `qualified_by`.

## Validation stages

Stages are computed cumulatively from captured evidence; they are not self-attested labels.

- `V0`: demonstrated execution is absent
- `V1`: completed, resolvable steps and at least one declared output
- `V2`: V1 plus verified files, exact runtime, hashed lockfile or digest-pinned container, replay argument array, and expected artifacts
- `V3`: V2 plus evaluation, baseline/control, metrics, uncertainty, robustness/failure analysis, and approved human checkpoint
- `V4`: V3 plus prospective and independent evaluation and at least one E6 record

## File integrity

All declared paths must be relative, stay inside the bundle, exist, and carry lowercase SHA-256 digests. Hash equality proves byte identity only.

## Replay

`replay.command` is an argument array, never a shell string. The CLI defaults to preflight. Execution requires `--execute`. The current runner uses a copied bundle, `shell=False`, a reduced environment, an executable allowlist, and a timeout. It does not enforce network or kernel isolation.

## Compatibility

The manifest is intentionally JSON and adapter-friendly. Unknown fields are preserved. Future breaking changes require a new `spec_version`.