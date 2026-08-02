# Structural Atlas program

## One-sentence purpose

Compare how different scientific studies turn observations into claims, then use verified structural overlaps or mismatches to produce better questions without claiming that the underlying phenomena share one mechanism.

## Required final output

Every atlas run must end with one short, fixed-format verdict:

> **STRUCTURAL VERDICT:** what pattern is supported, what it does *not* establish, whether a new three-target interview set exists, and the one next permitted action.

The current verdict is generated in `verification/structural-atlas-verdict.json` and rendered for review in `reports/structural-atlas.md`.

## Exact operating list

### Phase 1 — add a structural case

- [ ] Name one paper–data pair and its domain.
- [ ] Record exact source URLs and locations for every consequential statement.
- [ ] Record the public-data URL, file-level location, and one of four acquisition states: checksum verified, row-level inspected, aggregate only, or access blocked.
- [ ] Map five layers: system, unit, measurement, published inference, and validation gap.
- [ ] Classify only the evidence-backed structural pattern(s): measurement reuse, unit mismatch, calibration shift, provenance reconciliation, or data closure.
- [ ] State a one-sentence, non-jargon verdict and at least one limitation.
- [ ] Validate the record against `schemas/structural-case.schema.json`.

### Phase 2 — review the atlas

- [ ] Run `python3 scripts/build_structural_atlas.py`.
- [ ] Read the final verdict first, then inspect each linked case record.
- [ ] Treat an overlap as meaningful only when the mapped roles and assumptions align; a shared word, curve shape, or subject label is insufficient.
- [ ] Preserve mismatches, exclusions, blocked access, and prior-art defeats as results.

### Phase 3 — generate and admit questions

- [ ] Form a lead only from a named structural comparison and a domain-specific consequence.
- [ ] Challenge the lead with direct prior art and the simplest domain-specific explanation.
- [ ] Require public row-level data, an explicit published baseline, a known artifact/confounder, an independent partition or replication, self-contained interpretation, and checksum-acquirable files.
- [ ] Send only passing leads to `scripts/closed_evidence_factory.py`.
- [ ] Begin the first interview only when exactly three targets pass; require both a primary and reserve survivor before broader evidence work.

## Safe boundaries

- The atlas is a map of research-design structure, not a theory that different domains share a physical, biological, or social mechanism.
- A structurally interesting case cannot bypass data adequacy, novelty, self-contained-interpretation, execution-readiness, or preregistration gates.
- No external contact, remote action, publication, or scientific public claim is authorized by this program.
- The existing E. coli result is retained as a historical demonstration; it is not counted as a new Cycle 2 candidate.

## Owner review questions

1. Is the stated overlap a real alignment of roles and assumptions, or only an analogy?
2. Does the comparison make a falsifiable, domain-specific question possible?
3. Is the final verdict clear enough to act on without accepting scientific jargon on trust?
