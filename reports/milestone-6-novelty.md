# Milestone 6 — Adversarial novelty challenge

Status: complete for all three Milestone 5 finalists.

Outcome: all three finalists were rejected. No experiment is eligible for Milestone 7.

This is a negative scientific result, not a pipeline failure. The challenge found direct prior art for the two leading candidates and a fatal construct-and-data mismatch for the cross-domain candidate. No candidate is described as novel, selected, or experimentally validated.

## Method and boundary

The review attempted to invalidate each finalist through exact and alternative terminology, backward and forward citation tracing, adjacent-disciplinary formulations, variable-level dataset audits, simpler explanations, decisive tests, confounders, evidence against importance, and explicit specialist gaps.

The bounded review used primary studies and official dataset documentation for consequential judgments. Bibliographic metadata was used only to trace citations or document an indexing gap. Reviews and theory oriented terminology and tested whether a proposed contribution was already generic. No paper was replayed in full and no experiment, holdout, preregistration, or final selection was started.

Governed evidence:

- `verification/novelty-searches.jsonl`: 13 search and citation-tracing records.
- `verification/dataset-audits.jsonl`: 7 variable/protocol audits.
- `verification/novelty-challenges.jsonl`: 3 comparative adversarial dossiers.
- `schemas/novelty-search-record.schema.json`, `schemas/dataset-audit.schema.json`, and `schemas/novelty-challenge.schema.json`: validation contracts.

## Comparative result

| Finalist | Decisive adverse evidence | Dataset result | Disposition |
|---|---|---|---|
| Urban thermal recovery with ECOSTRESS and Landsat | Kang, Song, and Kim (2025), DOI `10.1117/12.3073343`, already uses multi-temporal ECOSTRESS and Landsat to analyze post-heatwave cooling rates and temperature deviations across multiple U.S. urban areas and urban-form classes (abstract and bibliographic record). | ECOSTRESS and Landsat provide quality-controlled surface temperature, not air temperature or exposure; irregular clear-sky observations do not directly observe a trajectory. | Rejected |
| Battery relaxation and path-dependent degradation | Zhu et al. (2022), DOI `10.1038/s41467-022-29837-w`, predicts capacity from relaxation features; the 2025 primary study DOI `10.1039/D4EE04787G` explicitly tracks path-dependent degradation with SOC-wise relaxation voltage under reordered conditions. | The actual NASA B0005/6/7/18 README defines charge, discharge, and impedance operations but no recorded rest-voltage series or controlled load-order permutations. | Rejected |
| Four-domain recovery-feature transfer | Established resilience work already defines degree of return, recovery time/rate, and curve area (DOI `10.1038/srep28426`); dynamical-systems theory shows finite-time return depends on perturbation and observed variable (DOIs `10.1016/j.jtbi.2017.10.003` and `10.1017/S0956792523000141`). | The named sources do not share a protocol: radiometric surface fields, battery operations, product-specific ecology, biomass footprints, computed static material properties, and heterogeneous repository entries are not interchangeable recovery curves. | Rejected |

## 1. Urban thermal recovery

### Terminology and citation attack

Searches expanded the proposal into *post-heatwave thermal response*, *urban heatwave recovery*, *cooling rate*, *temperature deviation*, *thermal persistence*, *nocturnal recovery*, *diurnal surface urban heat island*, and *local climate zone dynamics*.

The exact-match result is decisive. The abstract for Kang, Song, and Kim (2025) states that the authors used multi-temporal land-surface-temperature series from ECOSTRESS and Landsat to analyze cooling rates and temperature deviations during post-heatwave recovery across multiple U.S. cities. They compare Local Climate Zones with a morphology-adaptive 3D landscape classification. That substantially matches the proposed instrument pair, event phase, outcome, spatial comparison, and urban-form explanation.

Adjacent primary work also uses ECOSTRESS to measure diurnal urban-park cooling and local-climate-zone thermal dynamics. These studies do not all define post-event recovery, but they remove the proposed method and explanatory variables from plausible novelty.

OpenAlex indexed no references and no forward citations for the recent SPIE paper. Both absences are recorded as indexing/access gaps, not evidence for novelty. The ECOSTRESS retrieval lineage was traced through the official L2 user guide.

### Dataset and explanation attack

ECOSTRESS Collection 2 provides land-surface temperature, per-pixel error, emissivity, quality flags, cloud/water masks, view angle, elevation, and acquisition metadata at a delivered 70 m grid. Landsat Collection 2 provides surface temperature, pixel and radiometric quality flags, and a surface-temperature uncertainty band. These variables support a surface-temperature analysis, but neither instrument directly measures neighborhood air temperature, indoor conditions, or human exposure.

Simpler explanations include acquisition time, post-event meteorology, surface composition, cloud-related missingness, and emissivity error. A meaningful extension would need to reproduce the 2025 result, demonstrate an incremental prediction or validation claim, and validate surface recovery against independent near-surface observations. That would be a new candidate requiring reranking; it is not a surviving form of the present finalist.

### Specialist gap

Urban-climate, thermal-remote-sensing, and heat-health review remain necessary for any future event, harmonization, or exposure claim.

## 2. Battery relaxation and degradation path

### Terminology and citation attack

Searches included *voltage relaxation*, *open-circuit voltage recovery*, *SOC-wise relaxation voltage*, *degradation path indicator*, *history-dependent aging*, *order effects*, *calendar-cycle sequence*, and *voltage hysteresis*.

The conceptual bridge is already present in primary work. Zhu et al. (2022) use relaxation-curve features across 130 cells for capacity estimation and report held-out errors of roughly 1.1–1.7% (abstract and results). Raj et al. (2020), DOI `10.1002/batt.202000160`, experimentally vary the order of matched calendar and cyclic aging. Most decisively, the 2025 Energy & Environmental Science study DOI `10.1039/D4EE04787G` uses SOC-wise relaxation voltage as a degradation-path tracker under dynamic operating sequences where condition counts are balanced and order varies.

Earlier alternative terminology includes direction-dependent voltage hysteresis and open-circuit equilibration before resistance measurement (DOI `10.1016/j.jpowsour.2007.08.025`). Forward tracing from Zhu et al. leads to the explicit 2025 degradation-path study. Citation counts were retained only as metadata and not treated as evidence of scientific importance.

### Dataset and explanation attack

The official NASA archive was inspected beyond its landing page. In nested archive `1. BatteryAgingARC-FY08Q4.zip`, `README.txt` defines four cells undergoing CC-CV charge, constant-current discharge, and EIS. Stored operation types are charge, discharge, and impedance. Fields include voltage, current, temperature, time, discharge capacity, impedance, `Re`, and `Rct`; there is no rest operation or voltage time series during inter-operation gaps. The four cells also use different discharge cutoffs.

The dataset therefore cannot test whether standardized relaxation features identify an order effect beyond matched cumulative exposure. Unmeasured time gaps cannot be converted into relaxation curves. The larger randomized-use archive was not downloaded after the named archive failed the variable gate and direct prior art had already invalidated the question.

Simpler explanations are current capacity, state of charge, temperature, recent charge conditions, cell identity, and protocol schedule. A decisive test needs randomized load-order permutations, matched cumulative exposure, standardized open-circuit sampling, independent diagnostics, and held-out cells. That experiment already has close prior art and would require a distinct unresolved claim before reranking.

### Specialist gap

Electrochemistry, battery-aging experimentation, and prognostics review remain necessary for mechanism, intervention, and leakage judgments.

## 3. Cross-domain transferability

### Terminology and citation attack

The search expanded into *return time*, *recovery rate*, *asymptotic resilience*, *finite-time resilience*, *resilience/rebound curve*, *relaxation time*, *hysteresis loop*, *degree of return*, *area under the recovery curve*, and *critical slowing down*.

No exact study spanning the four chosen domains was found. This failed search is weak evidence because the conjunction is arbitrary and the component mathematics are established. Soil-resilience work already defines return degree, recovery time, recovery rate, and cumulative curve magnitude using a spring-damper analogy. OpenAlex indexes 92 later works citing that formulation across several applied fields. Ecosystem and dynamical-systems theory distinguish finite-time from asymptotic return and show dependence on perturbation direction, observed variable, scale, and baseline. A 2025 methodological critique, DOI `10.1093/pnasnexus/pgaf052`, argues that generic rebound curves are non-explanatory and can hide adaptation and changing baselines.

### Dataset and explanation attack

The proposed data sources fail a common protocol:

- ECOSTRESS is an irregular radiometric surface field.
- NASA B0005/6/7/18 contains battery operations without rest-voltage trajectories.
- NEON vegetation products have plot-, product-, growth-form-, and site-specific cadence; disturbance reports are not standardized interventions.
- GEDI L4A provides sampled footprint biomass estimates, not a guaranteed repeated panel through an event.
- Materials Project provides computed equilibrium structures and properties, not cyclic experimental trajectories.
- NIST's repository explicitly describes heterogeneous provider-defined entries that may not be critically reviewed; no suitable cyclic record was identified.

Any bounded trajectory can be rescaled to look similar. A common exponential may reflect local linearization rather than shared mechanism. Incomplete return may reflect ongoing forcing, a moving baseline, irreversible damage, measurement drift, or a short observation window. Hysteresis specifically requires an interpretable loading-unloading path and cannot be inferred from every recovery series.

The proposal therefore lacks a falsifiable scientific consequence beyond generic normalization. A future pairwise candidate would need a domain-specific prediction, compatible controlled variables, within-domain nulls, and specialist agreement on construct meaning. It must re-enter opportunity ranking rather than inherit finalist status.

### Specialist gap

Dynamical-systems, ecology, electrochemistry, fatigue-materials, and urban-climate review would all be required. The breadth of this dependency is evidence against tractability, not a reason to presume a hidden survivor.

## Evidence for and against the program's ranking

The ranking did identify computationally approachable and superficially coherent questions with accessible source families. Two finalists also pointed toward genuinely active, important research areas. However, Milestone 6 exposed three ranking weaknesses:

1. One urban support source (`10.1016/j.enbuild.2021.111312`) concerned resilient building cooling rather than satellite neighborhood recovery.
2. Dataset landing-page availability inflated apparent adequacy before protocol inspection.
3. Cross-domain vocabulary and generic curve structure received too much leverage relative to construct equivalence and incremental scientific consequence.

These are method-evaluation observations, not a Milestone 9 evaluation and not authorization to generalize the system.

## Completion gate and next decision

Every finalist has an evidence-backed disposition, terminology expansion, backward/forward tracing record, dataset-variable/protocol audit where relevant, evidence for and against novelty and importance, decisive tests, simpler explanations, confounders, and explicit specialist gaps. Schema validation and repository tests pass.

Because all finalists were rejected, the project must not start Milestone 7. The owner's next decision is whether to authorize a bounded return to Milestone 5 to rerank or generate replacement candidates using the new prior-art and data-adequacy evidence, or to pause the pilot. A final experiment cannot be selected from the current finalist set.

## Cost

The fresh weekly meter was 70.0% used at task start, 71.0% after all three bounded finalist batches and governed-record validation, and 72.0% after final closeout: a 2.0 percentage-point increase, within the 3-point target and below the 75% absolute stop.
