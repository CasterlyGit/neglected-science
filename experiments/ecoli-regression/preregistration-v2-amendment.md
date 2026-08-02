# Preregistration v2 amendment — computational uncertainty and robustness

Frozen before any final-block computation on 2026-08-02. This amendment does not change the question, source, partitions, hypotheses, data exclusions, estimand, direction threshold, or claim boundary in v1.

During the pre-final implementation review, v1's requirement to report a 95% interval and leave-replicate robustness checks was found not to specify their exact deterministic calculation. The omission was identified after exploration and validation but before final-block evaluation. It is recorded rather than silently repaired.

The amended final procedure fixes: (1) a nonparametric 10,000-draw bootstrap over the 16 comparison-level Fisher-z correlations, seed `20260802`, with 2.5th and 97.5th percentile endpoints; (2) leave-one-comparison-out mean ranges; and (3) three leave-one-evolutionary-replicate-out means. The unchanged final direction interpretation uses the bootstrap 95% interval.

Validation block 3 will be rerun under this exact code before the amended procedure is committed. Any consequence of this amendment remains a declared deviation from v1, and v1 remains preserved without replacement.
