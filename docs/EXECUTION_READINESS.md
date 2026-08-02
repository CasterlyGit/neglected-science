# Execution-readiness protocol and failure catalogue

## Why this gate exists

A scientifically strong, data-shaped question can still fail as an investigation if its public inputs cannot be acquired, verified, partitioned, or operated reproducibly when execution begins. A prior row-level inspection is evidence of possible analytical fit; it is not evidence of current execution readiness. This protocol makes that distinction a noncompensatory gate.

## Milestone 6.5 — execution-readiness certification

Milestone 6.5 sits after confirmation-grade novelty review and before Milestone 7 selection. Both the proposed primary and reserve must independently pass every check below. A score, prior success, cached copy, landing page, or plausible substitute cannot compensate for a failed check.

| Check | Required evidence | Failure consequence |
|---|---|---|
| Official acquisition | Fresh clean-environment retrieval from the cited public source, or a separately documented authorized public mirror | Target is not selectable. |
| Integrity and version | Published checksum verified, or a source-issued version/hash plus an immutable local receipt | Target is not selectable. |
| Rights and scope | License permits the declared computation; all required files and any access conditions are recorded | Target is not selectable. |
| Structural fit | Machine-readable headers, identifiers, unit counts, required variables, and partition field are checked against the proposed estimand | Target is not selectable. |
| Partition safety | A deterministic reader can expose only schema and declared non-final partitions; final outcomes are inaccessible to exploration code | Target is not selectable. |
| Baseline viability | The original code, or an independently specified reconstruction, identifies the exact inputs, grouping, transformation, and expected diagnostic | Target is not selectable. |
| Operational rehearsal | A clean environment creates a provenance receipt and runs a no-outcome structural check with pinned dependencies | Target is not selectable. |

The certification record must name the source URL, retrieval time, version, digest, license, file list, exact structural checks, environment lock, partition design, failure logs, and reviewer. It is a feasibility certificate, not a scientific result and not permission to inspect final-holdout outcomes.

## Current E. coli status

The E. coli target was selected and preregistered before this new gate existed. Its historic selection remains an auditable record, but it has **not passed Milestone 6.5 retrospectively**: Dryad's live page exposes the files, while unattended retrieval encounters an anti-automation validation page. The downloaded responses had HTML content and did not match the published SHA-256 values; they were discarded. No scientific data were accepted. Milestone 8 remains blocked until the official files are acquired and verified.

## Failure catalogue through Milestone 9

| Milestone / failure mode | Preventive control | Required evidence before advancing |
|---|---|---|
| 6.5: source disappears, changes version, blocks automation, or has an incompatible license | Fresh retrieval, checksum/version receipt, rights review, and a separately certified reserve | Passing certificates for both selectable targets; retain failed receipts. |
| 7: selecting a compelling but operationally weak primary | Selection may consider only 6.5-certified targets; reserve stays executable until final analysis starts | Comparative selection memo tied to two certificates, not ranking score alone. |
| 7: preregistration leaves outcome-dependent choices open | Freeze data version, identities, partitions, exclusions, baseline, estimand, tests, robustness set, and falsifiers in version control | Machine-valid preregistration committed before final-outcome access. |
| 8: provenance drift or parser silently maps the wrong units | Immutable raw receipt, explicit input schema, row/unit reconciliation, and synthetic parser tests | Checksums, data dictionary mapping, count reconciliation, and passing tests. |
| 8: published baseline cannot be reproduced | Reconstruct the original analysis from source code/methods on non-final partitions first; never tune novel analysis to force agreement | Baseline report stating match, partial match, or failure with exact source-location evidence. |
| 8: exploratory choices leak into final evaluation | Separate exploration, validation, and final code paths; commit the validation-frozen implementation before final evaluation | Commit hash, partition access log, and one final-evaluation receipt. |
| 8: result is driven by one block, unit, model, or undocumented dependency | Predeclare robustness checks, use leave-unit/block checks, pin environment, and retain null/contrary outcomes | Reproducible report, environment lock, robustness table, deviations, and negative results. |
| 8: computational association is inflated into mechanism or causation | Claim linting against the preregistered claim boundary; record specialist gaps | Claim-to-evidence table and explicit prohibited inferences. |
| 9: one successful run is generalized into a discovery platform | Evaluate question quality separately from result direction; compare selected and reserve, failed leads, cost, automation contribution, and expert dependencies | Method-evaluation report with misses, counterfactuals, unsafe automations, and limits. |
| 9: method evaluation hides selection bias or unavailable expertise | Preserve all triage exclusions, failed access checks, revisions, deviations, and unresolved specialist objections | Auditable negative ledger and a bounded next-architecture decision. |

## Immediate-workaround policy

For an already preregistered target, a public source may be retrieved manually through its visible official interface when unattended access is blocked. The raw files must be placed in `data/raw/`, checksum-verified against the official manifest, and recorded as a deviation-free acquisition receipt. A browser challenge page, screenshot, metadata listing, figure reconstruction, or unverified copy is never a substitute. If manual official retrieval fails, use the independently certified reserve; do not weaken the protocol or invent a mirror.
