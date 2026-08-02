# Neglected Science

Neglected Science is a local-first research program for discovering scientifically important, computationally testable questions that may be overlooked despite sufficient public evidence or data.

The project is not a generic paper summarizer or an autonomous scientist. It first builds a bounded, evidence-traceable metaresearch process; uses that process to select a question; executes a reproducible investigation; and only then decides what should be generalized.

## Governing direction

> Metaresearch chooses the question. Domain research tests whether the choice was intelligent.

The current candidate territory is stress, memory, recovery, and phase transitions across physical and environmental systems. It is a search boundary, not a predetermined conclusion. Phoenix thermal memory is one candidate and receives no automatic preference.

## Current status

- Maturity: experimental
- Visibility: local-only
- Remote: none
- Completed milestones: 1–6
- Next decision: rerank or generate replacement candidates, or pause; Milestone 7 has no eligible finalist
- Scientific findings: none
- Selected investigation: none

See [VISION.md](VISION.md), [ROADMAP.md](ROADMAP.md), and [research_contract.md](research_contract.md).

## Repository map

```text
corpus/          source catalog and retrieval records
claims/          provenance-backed claim records
terminology/     cross-disciplinary concept mappings
opportunities/   candidate questions and dossiers
experiments/     preregistered computational investigations
verification/    novelty, leakage, robustness, and falsification evidence
reports/         research and method-evaluation reports
methodology/     discovery and evaluation protocols
schemas/         machine-checkable record contracts
docs/            durable project status and decisions
```

## Immediate operating rule

No broad corpus ingestion or final scientific selection begins until Milestones 1 and 2 pass their completion gates. No result is called novel without an adversarial prior-art search and appropriate expert scrutiny.

## Verification

Create the isolated development environment once, then run the repository contract checks:

```bash
python3 -m venv .venv
.venv/bin/pip install "jsonschema>=4.20"
.venv/bin/python scripts/pipeline.py validate
.venv/bin/python -m unittest discover -s tests -v
```

## Verified pilot outputs

- 56 sources: 37 primary studies, 11 reviews, and 8 dataset-documentation records.
- 65 provenance-linked claim records with bounded excerpts and source locations.
- 18 deduplicated opportunities produced by all four discovery engines.
- 18 schema-valid dossiers ranked under balanced, rigor-first, and impact-first profiles.
- Three finalists adversarially challenged: all rejected; none is eligible for experiment selection.

See `reports/milestone-3-corpus.md`, `reports/milestone-4-discovery.md`, `reports/milestone-5-ranking.md`, and `reports/milestone-6-novelty.md`.
