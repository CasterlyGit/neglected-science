# Opportunity scoring

Scoring is a comparison aid, not a substitute for judgment. Each dimension is scored from 0 to 4 with a written rationale, cited evidence, uncertainty, and reviewer identity.

## Dimensions

- Societal or scientific importance
- Evidence that the question remains unresolved
- Public-data or simulation adequacy
- Computational testability
- Strength of falsification and independent verification
- Feasibility within time and compute limits
- Expected value of a negative result
- Cross-disciplinary leverage
- Potential real-world impact

## Penalties tracked separately

- Prior-work risk
- Confounding and measurement risk
- Dependence on inaccessible expertise or infrastructure
- Safety, ethics, privacy, or licensing constraints
- Susceptibility to benchmark or publication bias

## Ranking rules

1. Preserve dimension scores; do not expose only one total.
2. A candidate cannot advance with zero testability, data adequacy, or falsification strength regardless of total.
3. Run sensitivity analysis across at least three reasonable weight profiles.
4. Reviewer disagreement remains visible.
5. Ranking selects finalists for challenge, not the final experiment.
