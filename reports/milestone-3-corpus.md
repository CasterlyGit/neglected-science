# Milestone 3 — Trustworthy evidence corpus

Status: complete for the bounded pilot.

## Evidence

- 56 sources, evenly distributed across four domains.
- 37 primary studies, 11 reviews or syntheses, and 8 dataset-documentation records.
- All 48 paper records have a DOI verified through Crossref with a normalized title match.
- All dataset records point to identified landing pages; six were directly reachable and two blocked automated access without being treated as invalid.
- 65 claim records resolve to a source and location. Abstract-derived evidence uses a bounded excerpt, sentence index, full-sentence hash, extraction method, review status, and uncertainty.
- Raw abstracts are stored only in the ignored local cache and can be regenerated from OpenAlex metadata.

## Review

- A 12-record source sample covering every domain and source role was accepted, with dataset records explicitly requiring variable-level audits.
- An 11-record extraction sample passed all evidence-location and hash checks.
- Two classifier-polarity errors were found, documented, corrected through explicit overrides, and excluded from unreviewed scientific decisions.
- Two additional bounded searches per domain added no new high-level mechanism or dataset family. They did refine terms that must be used during finalist-specific novelty searches.

## Coverage boundary

The corpus covers urban/land-surface heat, ecological recovery, battery degradation and relaxation, and material fatigue/hysteresis. It does not claim exhaustive literature coverage, full-text extraction, specialist validation, or proof that any question is unresolved.

## Verification artifacts

- `verification/source-review.json`
- `verification/extraction-review.json`
- `verification/extraction-overrides.json`
- `verification/saturation-audit.json`
- `verification/saturation-review.json`
- `corpus/retrieval-ledger.jsonl`
