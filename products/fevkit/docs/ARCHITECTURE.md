# Architecture

FEVKit has four deliberately separate layers:

1. **Declaration:** `run.json` records the bounded objective, ordered steps, artifacts, evidence, claims, privacy, replay, and validation evidence.
2. **Deterministic audit:** `fevkit.core` resolves references, verifies files, evaluates Function and Evidence completeness, checks claim support and boundaries, and computes the cumulative Validation stage.
3. **Controlled replay:** the runner preflights by default and executes only after an explicit flag in a temporary copy with `shell=False` and expected-artifact comparison.
4. **Interoperability and review:** JSON, text, SARIF, Process Run RO-Crate export, and the browser inspector expose the same run to different reviewers.

The browser inspector is not the canonical validator because a selected JSON file cannot prove adjacent file hashes or execute replay. The CLI is canonical. The CLI still cannot establish scientific or clinical correctness; it can only make the captured basis inspectable.