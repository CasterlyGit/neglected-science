# Milestone 7 — selection and preregistration

Status: complete locally on 2026-08-02.

## Decision

`target-ecoli-regression` is selected for the program's first computational investigation. The selection is evidence-backed but cautious: it was the confirmation-grade primary survivor, and it most directly joins a known shared-error artifact to a four-assay-block public design and a predeclared falsification test. `target-bighorn-within-between` remains the reserve; it was not discarded. `target-mesi-reconciliation` remains excluded from selection pending its author-overlap and specialist-review gate.

## Frozen record

`experiments/ecoli-regression/preregistration-v1.json` and `PREREGISTRATION-v1.md` were committed in local commit `7b1232a` before source-file retrieval or final-holdout inspection. They freeze the source (Dryad DOI 10.5061/dryad.4f4qrfjfs), block partitions (1–2 exploration, 3 validation, 4 final holdout), baseline reconstruction, cross-fitted primary estimand, errors-in-variables sensitivity, falsifiers, and claim boundary.

The preregistration does not promise a positive result. It prohibits causal, biological-mechanism, universal-predictability, physical-validation, absolute-novelty, and expert-review claims.

In plain language, the published experiment found that E. coli populations beginning fitter appeared to gain less fitness. That may reflect a real diminishing-returns pattern, or partly a mathematical artifact because the same noisy baseline enters the change score. Separate public assay blocks allow a preregistered robustness test that estimates baseline and later gain from different blocks. Persistence, attenuation/null, and reversal are all informative; none alone proves a biological mechanism or universal evolutionary law.

## Next gate

Milestone 8 may begin only when the public raw files can be acquired and their listed Dryad SHA-256 digests verified. The final-holdout block must remain unused until a validated implementation is frozen in a later local commit.
