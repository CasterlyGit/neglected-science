# Function–Evidence–Validation mapping

FEVKit operationalizes three orthogonal views of a scientific-agent run.

## Function

| ID | FEVKit interpretation |
|---|---|
| F1 | An inspectable plan or task decomposition exists. |
| F2 | Specialized roles and authority boundaries are recorded. |
| F3 | Tool name, version, parameters, inputs, and outputs are captured. |
| F4 | Ordered state, lineage, and intermediate artifacts are retained. |
| F5 | Self-evaluation, repair, or failure search is recorded. |
| F6 | Verification and escalation—including human checkpoints—are retained. |

## Evidence

| ID | FEVKit interpretation |
|---|---|
| E1 | Scientific literature with stable citation metadata. |
| E2 | Structured biological knowledge with database/version/query/selection. |
| E3 | Biological data with dataset identity, snapshot, and selection. |
| E4 | Software or statistical output with software/version/parameters. |
| E5 | Scientific-model output with model/version/parameters. |
| E6 | Experimental or clinical observation with protocol/site metadata. |

## Validation

| Stage | Required assurance |
|---|---|
| V0 | Illustrative output only. |
| V1 | A demonstrably executed, ordered workflow. |
| V2 | V1 plus verified files, pinned environment, and replay contract. |
| V3 | V2 plus baseline-aware evaluation, uncertainty, robustness, and supported claims. |
| V4 | V3 plus prospective, independent empirical evaluation and E6 observations. |

Stages are cumulative. A declared V4 run that only captures V1 evidence is an overclaim, not a partial V4.

FEVKit separately reports B (baseline), H (human), S (statistics), R (robustness), X (external), P (prospective), and C (closed loop). Qualifiers are descriptive—not points in a score.

FEVKit is an independent implementation informed by the FEV framing associated with Pham and Hy. It does not claim endorsement or formal conformance certification.
