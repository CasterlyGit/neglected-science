# FEVKit

**Trust the trajectory, not just the answer.**

FEVKit is a local-first, agent-neutral audit and replay gate for biomedical and scientific AI runs. It records and checks three different questions without collapsing them into a misleading trust score:

- **Function (F1–F6):** what the workflow demonstrably did.
- **Evidence (E1–E6):** what supports its actions and claims.
- **Validation (V0–V4):** what level of assurance the captured run actually earned.

A workflow can execute reproducibly and still use the wrong data, methods, parameters, or interpretation. FEVKit therefore treats reproducibility as necessary—not proof of scientific or clinical correctness.

## What ships in v0.1.0

- Deterministic manifest and semantic validation
- SHA-256 integrity checks for every declared input and artifact
- Reference and lineage resolution across steps, files, evidence, and claims
- F1–F6 and E1–E6 completeness profiles
- Cumulative V0–V4 stage computation and overclaim detection
- Claim-to-evidence relations with uncertainty and limitation checks
- Privacy attestations, contradiction checks, and bounded secret-pattern scanning
- Human checkpoint and escalation records
- Safe replay preflight and opt-in execution (`shell=False`, copied bundle, timeout)
- JSON, human-readable, and SARIF reports
- Process Run RO-Crate 0.5 export
- A small Python recorder SDK
- Passing and deliberately broken example bundles
- A browser-only inspector at `https://fevkit.vercel.app`

## Install

```bash
python -m pip install .
```

## Audit

```bash
fevkit audit examples/complete --profile differential-expression
fevkit audit examples/incomplete --format json
fevkit audit examples/incomplete --format sarif --output fevkit.sarif
```

A successful audit reports a profile, not a single score:

```text
FEVKit PASS
Validation: V3 (Scientifically evaluated computation)
Qualifiers: BHSR
Integrity: all declared files verified
```

## Replay

Replay is never implicit:

```bash
fevkit replay examples/complete
fevkit replay examples/complete --execute
```

The first command performs preflight only. The second copies the bundle into a temporary directory, deletes expected outputs, executes an argument-array command without a shell, applies a timeout, and compares regenerated hashes.

FEVKit cannot by itself enforce network isolation. Use an external sandbox or container policy when replaying untrusted code.

## Export a research object

```bash
fevkit export-rocrate examples/complete --output /tmp/fevkit-crate
```

The export conforms to RO-Crate 1.1 and the Process Run Crate 0.5 profile. FEVKit adds its Function/Evidence/Validation records without inventing a replacement provenance standard.

## Scope boundary

FEVKit does **not** determine whether a treatment is safe or effective, a biological interpretation is true, an LLM is suitable for clinical use, a workflow satisfies a regulation, or an experiment is ethically authorized. Clinical, regulatory, and domain review remain external governance responsibilities.

## Status

v0.1.0 is an open technical alpha. The schema and profile vocabulary may evolve after feedback from biomedical-agent maintainers, research-software engineers, and reproducibility specialists.

FEVKit is an independent implementation informed by the Function–Evidence–Validation framing associated with Pham and Hy. It is not affiliated with or endorsed by the framework authors.

MIT licensed.
