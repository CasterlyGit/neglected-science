# Manual priority cycle through confirmation-grade Milestone 6

Status: complete. No experiment has been selected, preregistered, or executed.

## Result

A manually curated queue of seven high-probability leads replaced automatic candidate generation for this cycle. Three diverse targets passed all five noncompensatory construction checks, all three passed the adversarial first interview, and all three received confirmation-grade dispositions:

| Target | First interview | Milestone 6 disposition | Role after confirmation |
|---|---|---|---|
| E. coli shallow-history diminishing returns under measurement-error-aware estimation | Admitted | Surviving | Provisional primary |
| Bighorn pathogen-associated fat change within individuals | Admitted | Surviving | Reserve |
| MESI source-extraction disagreement | Admitted after one rewrite | Reframed | Alternate; specialist/author overlap check required |

“Surviving” means no fatal prior-art or data defect was found after the documented bounded challenge. It is not a claim of absolute novelty, correctness, causal identification, or experimental validation.

## Candidate selection

The ranked queue is recorded in `opportunities/candidate-priority-list.jsonl`. Selection favored an exact scientific consequence, row-level public data, a known but unresolved adverse explanation, and a test that could discriminate that explanation. Four attractive leads were not selected:

- MagDrift fatigue validation was deferred because both the raw Dryad archive and small error-analysis workbook returned HTTP 403; landing-page metadata was not accepted as data adequacy.
- Vineyard biocontrol robustness was excluded because the public outcome file contains only 20 treatment-epidemic summaries and the primary paper already tested epidemic-by-treatment interaction.
- Voltage-controlled battery diagnosis was excluded because the closest paper already shows the age-shift OCV failure and names the needed extension.
- VR balance habituation was deferred because no bounded labelled event sample could be verified without the 32.4 GB archive.

This is the intended behavior: plausible themes remain leads until actual variables and nearest prior work support a proposed experiment.

## Target 1 — E. coli shallow-history predictability

### Question

Does the shallow-history diminishing-returns relationship reported by Smith et al. (2022) persist when ancestral fitness and fitness gain are estimated from independent assay blocks with measurement-error-aware models?

### Why it survived

The [primary experiment](https://doi.org/10.1098/rspb.2022.1292) reports negative ancestral-fitness versus fitness-change correlations in 15 of 16 shallow-history comparisons. Its competition assays have fourfold replication, but the stated analysis does not address the directional regression-to-the-mean bias demonstrated by [Berger and Postma (2014)](https://doi.org/10.1534/genetics.114.169870). Exact and forward searches found no dataset-specific independent-block correction.

The [Dryad dataset](https://doi.org/10.5061/dryad.4f4qrfjfs) was inspected at row level. The evolved file has 704 assay rows, four strains, four environments, four shallow-history states, 191 evolutionary units, and four assay blocks. The ancestral file adds 251 rows. Fields include strain, environment, mutation, evolution replicate, assay block, ancestral fitness and SEM, and fitness change.

### Adverse explanations and decisive test

The strongest simple explanation is mathematical coupling: error in ancestral fitness appears with the opposite sign in a change score. The decisive later experiment would cross-fit ancestral fitness and change from disjoint assay blocks and fit a hierarchical errors-in-variables model, with environment and evolution-replicate consistency checks.

The remaining gaps are specialist review of assay-block exchangeability and limited precision from four shallow-history genotypes per deep-history background.

Disposition: **surviving**, moderate confidence.

## Target 2 — Bighorn infection and energetic reserves

### Question

Does pathogen-associated seasonal fat change persist within repeatedly observed bighorn sheep after separating stable individual and herd differences?

### Why it survived

The [primary study](https://doi.org/10.1098/rspb.2024.0636) uses seasonal ordering and animal random intercepts, then interprets pathogen coefficients as energetic costs. A random intercept accounts for repeated observations but does not itself separate within-individual exposure changes from between-individual exposure propensity. Exact and forward searches found no public within-between reanalysis.

The [Dryad data](https://doi.org/10.5061/dryad.6wwpzgn44) contain 183 interval records from 63 randomized animal IDs; 45 IDs repeat, with at most eight records. Current and prior fat, pathogen status and richness, acquisition, clearance, herd, age, reproduction, season, and snow depth are present.

### Adverse explanations and decisive test

Stable host quality, herd habitat, forage availability, or contact behavior could jointly affect infection and fat. The decisive later test would decompose pathogen exposure into individual means and within-individual deviations, then compare correlated-random-effect and individual-fixed-effect sensitivities across seasons, acquisition/clearance definitions, and leave-one-herd-out analyses.

Even a persistent within-animal association would remain observational: food intake, contact networks, and immune expenditure are absent, and single-capture pathogen detection is imperfect. Wildlife-disease and longitudinal-inference review remain required.

Disposition: **surviving**, moderate confidence.

## Target 3 — MESI extraction reconciliation

### Original question and killer

The original target asked whether independent MESI constituent databases extract conflicting effects from the same global-change experiments. That question is already partly answered by the [EGU 2026 abstract](https://doi.org/10.5194/egusphere-egu26-15935), which reports a researcher effect that can exceed the original effect and a belowground-biomass discrepancy ranging from negative to positive.

### One allowed rewrite

Can an independent, predeclared source-level reconciliation of a frozen MESI version reproduce that researcher effect, identify which extraction micro-decisions cause sign changes, and stabilize selected moderator conclusions?

The [MESI paper](https://doi.org/10.1111/gcb.16585) proposed quantifying extractor bias and retained constituent-database and potential-duplicate provenance, but did not perform the rewritten source-level protocol audit. The current [Zenodo archive](https://zenodo.org/records/10423853) was inspected: `mesi_main.csv` contains 56,547 rows and 60 fields, including database, potential-duplicate ID, citation, response, experiment, treatment/control means, units, dispersion, replication, aggregation, and sampling metadata.

The main risk is overlap with unpublished or forthcoming work from the EGU authors. `duplicate_id` also marks potential overlap rather than guaranteed estimand equivalence. A global-change ecologist, meta-analyst, and preferably the MESI/EGU authors must review overlap before this alternate could be selected.

Disposition: **reframed**, moderate confidence.

## Comparative decision

The E. coli target is the provisional primary because it has the cleanest alignment between a known artifact, independent assay structure, and a falsifiable correction. The bighorn target is the reserve because its within-between test is valuable and data-supported, but residual time-varying confounding prevents causal interpretation. MESI remains an alternate because it is important and tractable, but the 2026 conference claim narrows novelty and creates an unresolved author-overlap gate.

No final ranking score chose these roles. The comparison used prior-art severity, protocol adequacy, strength of the decisive test, negative-result value, execution cost, and specialist dependency.

## Verification and next decision

Machine-readable evidence:

- `opportunities/candidate-priority-list.jsonl`
- `verification/target-reviews.jsonl`
- `verification/cycle-result.json`
- `schemas/candidate-priority.schema.json`
- `schemas/target-review.schema.json`
- `schemas/cycle-result.schema.json`

The next decision belongs to the owner: choose whether to begin Milestone 7 with the E. coli primary, choose the bighorn reserve instead, request specialist review before choosing, or stop. Milestone 7 must freeze a preregistration before any final analysis or holdout evaluation.

## Cost boundary

This continuation began at 75.0% weekly used and ended at 76.0% after the evidence batches, governed validation, tests, documentation, commit, and delivery closeout. The displayed delta was one percentage point, below the owner-authorized 85% stop. Successful retrievals were not repeated, and blocked or oversized archives were not promoted into the trio.
