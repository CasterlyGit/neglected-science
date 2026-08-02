# Milestone 8 — validation freeze before final holdout

Status: validation complete; final holdout not yet evaluated when this file was committed.

## Data readiness

The owner-downloaded official Dryad archive supplied the two preregistered input files. Their local SHA-256 values match the public version-file manifest exactly. The resulting execution-readiness certificate is `verification/execution-readiness-ecoli.json`.

## Non-final results

The published-style reconstruction uses the original R Markdown grouping (`environment`, `strain`, `mutation`, and evolutionary replicate) and its `r.anc.strain` versus `r.change` variables. On blocks 1–2, its mean Fisher correlation over 16 strain-by-environment comparisons is −0.626. The independent-block cross-fit, which estimates ancestral fitness from one block and gain from the other, is also negative but attenuated to −0.358.

On validation block 3, using block 1 and then block 2 as independent ancestral estimates, the mean cross-fitted correlation is −0.248 across all 16 comparisons. The direction remains negative and the attenuation remains material. This validation is a pipeline check, not the final estimate and not a biological or causal result.

## Frozen implementation

`scripts/ecoli_analysis.py` is the committed implementation. It parses only the two checksum-verified files; derives ancestral initial fitness as the source R Markdown specifies; reconstructs the published-style comparison; and estimates cross-fitted gain from a disjoint assay block. Its partition modes prevent an exploratory or validation invocation from using block 4.

After this commit, the exact unchanged `--partition final` path will be run once. The final report will state the estimate, uncertainty, robustness checks, deviations, and claim boundary. A negative result cannot be described as a mechanism or universal evolutionary law.
