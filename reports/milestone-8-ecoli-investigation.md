# Milestone 8 — E. coli robustness investigation

Status: executed with open verification gaps. The final-holdout run occurred once under preregistration v2; this report preserves its result and does not rerun it.

## Question

The published experiment reported that E. coli populations beginning fitter tended to gain less fitness. The question was whether this negative relationship persists when baseline fitness and later gain are estimated from different assay blocks, avoiding the known shared-measurement structure of a change score.

## Provenance and procedure

The two official Dryad files were owner-downloaded and matched the source-published SHA-256 values in `verification/ecoli-final-result.json`. The original R Markdown (Zenodo DOI 10.5281/zenodo.6795996, lines 35–69 and 247–282) identifies the published-style grouping and variables. Exploration used blocks 1–2; block 3 validated the implementation; block 4 was evaluated once after commit `62d5899bbe79ffa633f10ae330a35af3dff6de86` froze the amended procedure.

## Results

The final published-style mean Fisher correlation across 16 strain-by-environment comparisons was −0.644. The preregistered independent-block cross-fit mean was −0.171, with bootstrap 95% interval −0.356 to 0.013. The interval includes zero, so the preregistered disposition is **attenuated or uncertain**.

The leave-one-comparison-out range was −0.222 to −0.121. Leave-one-evolutionary-replicate means were −0.300, −0.142, and −0.110. These checks preserve a negative point direction but do not override the primary interval.

## Claim boundary

The result weakens support for calling the published diminishing-returns direction robust to this specific shared-measurement stress test. It does not prove that the original pattern is false, that measurement error caused it, or that any biological mechanism or universal evolutionary law is invalid.

## Open verification gaps

The predeclared weighted errors-in-variables sensitivity was not implemented before final evaluation; any later work is exploratory. No independent statistician or microbial-evolution specialist reviewed block exchangeability or the estimand. Those gaps prevent claiming Milestone 8 fully complete, but they do not erase the preserved negative/uncertain primary result.
