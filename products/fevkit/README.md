# FEVKit

**Local-first trajectory assurance for biomedical and scientific agent runs.**

FEVKit asks three separate questions:

1. **Function (F1–F6):** What did the workflow demonstrably do?
2. **Evidence (E1–E6):** What supports its actions and claims?
3. **Validation (V0–V4):** What level of assurance did this particular run actually earn?

It does not produce a universal trust score. It audits an inspectable run bundle, verifies declared artifacts, checks claim-to-evidence links, computes the highest supported assurance stage, and reports what blocks the next stage.

**Live inspector:** https://fevkit.vercel.app

## What ships in v0.1.0

- dependency-free Python CLI and SDK
- deterministic structural and semantic audit rules
- SHA-256 verification for declared inputs, outputs, and lockfiles
- path-traversal and unresolved-reference checks
- Function and Evidence profile computation
- claim support, uncertainty, limitation, and inference-rationale checks
- explicit privacy attestation and contradiction checks
- cumulative V0–V4 stage computation with overclaim detection
- JSON, human-readable text, and SARIF output
- replay preflight and opt-in execution in a temporary copy with `shell=False`
- RO-Crate export with Process Run profile declarations
- passing synthetic and deliberately broken clinical-style fixtures
- local-only browser inspector with no account, analytics, database, or upload endpoint
- fourteen automated tests and a reproducible release gate

## Install

```bash
python -m pip install \
  "git+https://github.com/CasterlyGit/neglected-science.git#subdirectory=products/fevkit"
```

Development:

```bash
git clone https://github.com/CasterlyGit/neglected-science.git
cd neglected-science/products/fevkit
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

## Quick start

```bash
fevkit audit examples/complete --strict
fevkit audit examples/incomplete                 # exits 2
fevkit audit examples/incomplete --format sarif --output fevkit.sarif
fevkit replay examples/complete                   # preflight only
fevkit replay examples/complete --execute
fevkit export-rocrate examples/complete --output ro-crate-metadata.json
```

## Assurance is cumulative

| Stage | Meaning | Minimum signal |
|---|---|---|
| V0 | Illustrative output | A declaration exists, but execution is not demonstrated |
| V1 | Demonstrated execution | Completed steps and outputs form a resolvable trajectory |
| V2 | Replayable computation | Declared files verify, environment is pinned, and replay outputs are specified |
| V3 | Scientifically evaluated computation | Baseline, metrics, uncertainty, robustness, and human review are captured |
| V4 | Prospective empirical evaluation | Independent prospective evaluation and E6 observations are captured |

A run claiming a higher stage than captured evidence supports receives `VALIDATION.OVERCLAIM`.

Qualifiers are orthogonal to stages: `B` baseline, `H` human review, `S` statistics/uncertainty, `R` robustness, `X` independent evaluation, `P` prospective testing, and `C` closed-loop refinement.

## Integration contract

FEVKit is not another agent framework. Existing systems emit a bundle by writing `run.json`, using `fevkit.RunRecorder`, or translating an existing trace with an adapter. An adapter must never invent missing tools, versions, evidence, uncertainty, review, or validation.

## Security and privacy

Browser inspection never transmits the selected JSON file. CLI audit is local. Replay is separate and requires `--execute`.

Replay is **not a security sandbox**. FEVKit uses a temporary copy, `shell=False`, an executable allowlist, a reduced environment, and a timeout. Enforceable network, filesystem, process, and hardware isolation require an external sandbox or institutional execution environment.

## Scientific boundary

A passing audit means that the declared trajectory is inspectable and satisfies the selected FEVKit rules. It does **not** establish biological truth, clinical validity or safety, causal correctness, regulatory compliance, or absence of undisclosed work.

FEVKit should make review possible, not automate scientific approval.

## Standards strategy

FEVKit does not introduce a replacement provenance package. It exports existing research-object concepts and a Process Run RO-Crate declaration, while adding Function, Evidence, claim, and assurance metadata as an explicit extension layer. The exporter is an interoperability scaffold, not a certification claim.

## Status

- Release: `0.1.0`
- Maturity: alpha research infrastructure
- License: MIT
- Clinical use: prohibited as a stand-alone decision or validation system
- Telemetry: none

The next adoption gate is independent review and one real adapter accepted or used by a scientific-agent team.