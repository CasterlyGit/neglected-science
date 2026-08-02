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
- Completed milestones: 1 — Research constitution; 2 — Bounded discovery territory
- Active milestone: 3 — Trustworthy evidence corpus
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
.venv/bin/python -m unittest discover -s tests -v
```
