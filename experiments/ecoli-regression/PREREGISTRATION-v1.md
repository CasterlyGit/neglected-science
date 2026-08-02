# Preregistration v1 — E. coli shallow-history regression artifact stress test

Frozen 2026-08-02 before downloading the source files or accessing results from final assay block 4.

## Selection

The selected target is `target-ecoli-regression`, the confirmation-grade primary survivor. The reserve remains `target-bighorn-within-between`. The selection follows the recorded comparison: E. coli has the most direct alignment between a documented shared-error artifact, four assay blocks, and a decisive public-data stress test. This is not a novelty, causal, or biological-mechanism claim.

## Question and hypotheses

Does the shallow-history diminishing-returns relationship reported by Smith et al. (2022; DOI 10.1098/rspb.2022.1292) persist when ancestral fitness and fitness gain are estimated from independent assay blocks with measurement-error-aware models?

The artifact hypothesis predicts material attenuation because error in ancestral fitness is shared with the change score, as described by Berger and Postma (2014; DOI 10.1534/genetics.114.169870, abstract and equations 3–4). The persistence hypothesis predicts a negative relationship under independent-block estimation.

## Data and partitions

The only permitted source is Dryad DOI 10.5061/dryad.4f4qrfjfs, using `data_set-full.anc.txt` and `data_set-full.ev.change.txt`. Assay blocks 1–2 are exploration, block 3 is validation, and block 4 is the final holdout. Raw files and their checksums will be recorded on acquisition. Block 4 must not be read, summarized, or used to choose definitions, code, transformations, exclusions, or models until the validation freeze is committed.

Rows with missing identity, assay block, ancestral-fitness, or fitness-change fields will be excluded and counted. The published identifiers and documented strain, mutation/shallow-history, evolution environment, and evolutionary-replicate definitions control grouping. No outlier removal is permitted except a documented source-file parsing failure, recorded as a deviation.

## Analyses

First reproduce the published-style per-comparison Pearson correlation from exploration blocks only, recording any definition mismatch. Next estimate ancestral fitness on one block and fitness gain on a disjoint block, reverse the assignment, Fisher-z transform both correlations, and average them. The primary estimand is the mean cross-fitted Fisher-z correlation across the 16 comparisons. A weighted errors-in-variables sensitivity and leave-one-replicate/comparison-out checks are declared robustness analyses.

After the implementation and block-3 validation are committed, run the unchanged procedure exactly once on block 4. The pattern is robust only when the final point estimate is negative and its 95% interval excludes zero; it is attenuated/uncertain if the interval includes zero, and directionally contrary when non-negative. All outcomes, including a failed baseline or null result, remain in the report.

## Claim boundary and deviations

The analysis is associational and computational. It does not identify a causal biological mechanism or validate assay-block exchangeability; that specialist-review gap remains explicit. `preregistration-v1.json` is the machine-readable source of record. Any post-freeze alteration is a timestamped deviation and must not replace this version.
