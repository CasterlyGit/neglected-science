# Initial structural corpus protocol

## The decision this corpus must support

The first corpus answers one simple question: **do different fields contain the same evidence-supported research-design structure, or only similar-looking stories?**

It does not select an experiment and does not claim that different phenomena share a mechanism.

## Fixed first intake

The initial atlas contains exactly nine case slots. The six verified records in `corpus/structural-cases.jsonl` are anchors, not a candidate shortlist. Add at most three new cases, then stop and issue a verdict.

| Slot type | Count | Purpose |
| --- | ---: | --- |
| Historical demonstration | 1 | Shows a robustness check changed or qualified a published-style interpretation. |
| Open but gated cases | 2 | Shows a testable structural question with an explicit unresolved gate. |
| Prior-art defeat | 1 | Shows a plausible overlap that is already answered. |
| Data-closure failures | 2 | Shows why availability and granularity are scientific constraints. |
| New comparison cases | 3 | Fill only documented gaps in domain or structural-pattern coverage. |

The six anchors currently fill the first six slots. The three new cases must be deliberately different in both domain and research design: one controlled laboratory system, one field or observational system, and one synthesis or engineering system. A case may not be added merely to make the domains look diverse.

## Source-and-data-first admission list

Reject a prospective case before detailed reading unless all of the following are recorded:

1. One primary paper with an explicit published inference and a precise location.
2. One official public-data record linked to that paper.
3. A file inventory or a clean retrieval result—not landing-page metadata alone. A verified inventory is distinct from row-level inspection and checksum verification.
4. A named possible structural fragility: measurement reuse, unit mismatch, calibration shift, scale translation, provenance reconciliation, or data closure.
5. A plausible independent partition, replication, or a documented reason the case is a data-closure counterexample.
6. A claim that can remain self-contained: no mechanism, causality, or specialist interpretation beyond the cited record.

If an input fails items 1–3, retain only a one-line rejection receipt. Do not spend corpus time reading it as a candidate.

## How the three new cases are chosen

1. Read the generated atlas verdict and identify missing patterns or domain roles.
2. Search only for paper–data pairs that could fill one missing cell.
3. Run the source-and-data-first list before extracting any scientific claim.
4. Add the case only if it makes a distinct comparison possible; otherwise record why it was rejected.
5. Stop after three additions even if the map feels incomplete. The final verdict must state the uncertainty rather than silently widening the corpus.

## Required verdict after nine slots

> **STRUCTURAL VERDICT: [supported pattern / no supported pattern].** The evidence does or does not show [plain-language structural observation]. It does not establish [prohibited bigger claim]. New interview-ready targets: [number]. Next permitted action: [one action].

The only acceptable next actions are: add a specifically missing case, form a lead with a domain-specific consequence, or stop. “Read more papers” is not a verdict.
