# Neglected Science

Neglected Science is a local-first research program for discovering scientifically important, computationally testable questions that may be overlooked despite sufficient public evidence or data.

The project is not a generic paper summarizer or an autonomous scientist. It first builds a bounded, evidence-traceable metaresearch process; uses that process to select a question; executes a reproducible investigation; and only then decides what should be generalized.

## Governing direction

> Metaresearch chooses the question. Domain research tests whether the choice was intelligent.

The current candidate territory is stress, memory, recovery, and phase transitions across physical and environmental systems. It is a search boundary, not a predetermined conclusion. Phoenix thermal memory is one candidate and receives no automatic preference.

## Current status

- Maturity: experimental
- Visibility: public source repository
- Remote: https://github.com/CasterlyGit/neglected-science
- Program state: paused after Milestone 6
- Completed milestones: 1–6
- Redesign state: three-target candidate factory and first-interview gauntlet implemented; no new cycle authorized
- Milestone 7: gated; no eligible finalist
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

The pilot is paused after Milestone 6. The revised flow first upgrades raw leads into exactly three interview-ready targets using five uncompensated construction checks, then requires a primary and reserve survivor from an immediate adversarial interview. The roadmap and governed replay contracts implement this design, but no new target cycle is authorized.

The public repository documents the program and its evidence; it does not constitute a scientific publication or a claim that any result is novel.

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
- Retrospective replay: none of those finalists would qualify as a target under the revised candidate factory, so the new flow stops before broad corpus, ranking, or confirmation-grade novelty work.

See `reports/milestone-3-corpus.md`, `reports/milestone-4-discovery.md`, `reports/milestone-5-ranking.md`, `reports/milestone-6-novelty.md`, and `reports/three-target-replay.md`.
