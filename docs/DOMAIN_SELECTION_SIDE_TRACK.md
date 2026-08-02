# Domain-selection side track

Status: provisional decision framework. The main nine-milestone program remains paused after Milestone 6.

## The problem exposed by the pilot

The pilot selected a broad thematic territory—stress, memory, recovery, and phase transitions—then paid for corpus construction, candidate generation, and ranking before testing the strongest prior-art and dataset-protocol risks.

Milestone 6 showed why that order is expensive:

1. an exact urban study already used the proposed instruments, event phase, outcome, and urban-form comparison;
2. the battery concept had direct prior art, while the named NASA archive lacked the required rest-voltage and load-order protocol; and
3. the cross-domain proposal shared vocabulary and generic curve shapes, but not a common measurement or perturbation contract.

The corrective principle is:

> Do not select a domain and hope it contains a neglected question. Admit a narrow research wedge only after showing that it contains an observable contrast, usable data, and plausible novelty headroom.

## What counts as a research wedge

A wedge is narrower than a discipline and more concrete than a theme. It combines:

- a system and population or unit of analysis;
- an observed or imposed contrast;
- a measured response;
- a public dataset and actual protocol;
- a falsifiable unresolved relationship; and
- a credible independent check.

For example, “ecological resilience” is a domain label. “Recovery of a named vegetation measure at repeatedly sampled plots before and after documented disturbances, compared with matched unexposed plots” is a research wedge. The example describes structure only; it is not an endorsed candidate.

## Hard admission gates

A wedge is rejected before broad corpus work if any hard gate fails.

### 1. Observable-contrast gate

The proposal must identify a real comparison already present in public evidence or data: intervention versus control, before versus after, reordered but cumulatively matched exposure, conflicting predictions, repeated units, threshold crossing, or another explicit contrast.

A general association, visually interesting pattern, or shared metaphor is not enough.

### 2. Protocol-first data gate

Inspect the actual files, variable dictionary, sampling protocol, identifiers, missingness, units, and licensing before treating a dataset as available.

The minimum evidence is:

- one downloaded or queryable sample;
- confirmed variables for exposure, outcome, time or order, and major controls;
- stable units of analysis and join keys;
- a documented sampling or experimental protocol;
- enough independent units for a falsifiable comparison; and
- a plausible validation or holdout route.

A portal, catalog, paper claim, or landing page alone fails this gate.

### 3. Cheap novelty-kill gate

Before building a corpus, run a bounded adversarial search using:

- the exact proposed question;
- outcome plus instrument or dataset;
- alternative terminology from adjacent disciplines;
- the dataset name plus the proposed nonstandard use;
- backward citations from the closest foundational work; and
- forward citations that may already resolve the question.

If an exact or substantively equivalent experiment exists, reject or sharply reframe the wedge immediately. Geographic repetition, another model family, or another benchmark score does not by itself create scientific novelty.

### 4. Consequence gate

State what belief or decision changes under each plausible result, including a null result.

The wedge fails if its only contribution is “this has not been plotted,” “these domains have not been compared,” or “prediction improves slightly.” A useful result should discriminate explanations, validate or invalidate a measurement, expose a boundary condition, or change the adequacy of an accepted model or practice.

### 5. Independent-verification gate

Identify the check before admission: a second dataset, held-out units, another time period, a reproduced baseline, orthogonal measurement, negative control, or specialist-adjudicated protocol.

If the same data both generate and confirm the claim, the wedge requires a written justification and receives a severe penalty.

### 6. Expertise and execution gate

List the specialist judgments required and determine whether the evidence record can safely bound them. Reject wedges whose central interpretation depends on unavailable laboratory access, tacit protocol knowledge, restricted data, or several unrelated specialties.

Also verify that acquisition, cleaning, baseline reproduction, and the decisive test fit the declared compute, time, and token budget.

## Cross-domain admission rule

Cross-domain work is not an automatic virtue and should not be a domain-selection requirement.

Two wedges may be paired only when they independently pass all admission gates and share an experimental grammar:

- equivalent perturbation classes, such as a pulse, step, cycle, or reordered exposure;
- equivalent response geometry, such as repeated measurements on stable units;
- a comparable estimand, not merely a similarly named feature;
- compatible uncertainty and sampling treatment;
- a falsifiable transfer claim; and
- a reason the comparison changes scientific belief.

Shared terms such as *memory*, *resilience*, *recovery*, *hysteresis*, or *phase transition* are retrieval clues only. Shared curve shape after normalization is not sufficient.

The safest sequence is domain-first, transfer-second: establish one valid wedge in each domain, then ask whether a specific representation or prediction transfers. Do not begin with a universal cross-domain claim.

## A lower-cost funnel

### Stage A — Landscape scan

Create 10–20 short wedge cards from diverse sources. Each card contains only the contrast, outcome, named dataset, closest known work, potential consequence, and obvious fatal risk.

No broad ingestion and no ranking model are needed. The goal is rejection speed.

### Stage B — Admission screen

Run the six hard gates on each card using bounded searches and dataset metadata. Reject aggressively. A card that lacks an actual variable dictionary or sample does not advance.

### Stage C — Micro-audit

For at most three survivors:

1. inspect a real data sample;
2. reconstruct the closest published baseline at the design level;
3. trace the nearest citation neighborhood;
4. write the strongest simpler explanation;
5. identify one decisive analysis and one independent check; and
6. estimate the full investigation cost.

This is still domain admission, not discovery-corpus construction.

### Stage D — Territory decision

Admit one bounded territory only if at least one wedge survives the micro-audit and at least one neighboring wedge provides enough breadth for a discovery program. If none survives, stop without building a corpus.

Only after this gate should the project decide how Milestones 2–6 need to change.

## Provisional scorecard

Hard gates are pass/fail. Scores compare only wedges that pass every hard gate.

| Dimension | Question | Weight |
|---|---|---:|
| Contrast strength | Is there a real comparison capable of discriminating explanations? | 5 |
| Protocol adequacy | Do actual variables and sampling support the estimand? | 5 |
| Novelty headroom | Did the cheap kill search leave a specific unresolved boundary? | 5 |
| Consequence | Would positive, null, and contrary results change belief or practice? | 4 |
| Independent verification | Is there a credible holdout or orthogonal check? | 4 |
| Execution fit | Can the baseline and decisive test be completed within budget? | 4 |
| Expertise fit | Can specialist dependencies be bounded and reviewed? | 3 |
| Cross-domain option | Does another independently viable wedge share the same experimental grammar? | 1 |

The low cross-domain weight is deliberate. Transfer potential is a bonus after scientific viability, not a substitute for it.

## Promising source archetypes

The next scan should favor data regimes rather than fashionable disciplines:

- controlled multi-condition experiments with repeated units and unused protocol variation;
- long-term monitoring with documented shocks and stable identifiers;
- natural experiments with explicit policy, instrument, or environmental discontinuities;
- multi-site or multi-lab datasets with standardized measurements and known heterogeneity;
- public replication packages where an unresolved boundary condition remains testable;
- datasets containing negative, failed, or censored outcomes that conventional analyses omit; and
- instrument archives with rich quality variables and an independently measurable target.

Avoid admitting:

- broad portals without an identified product and protocol;
- static property catalogs for dynamic questions;
- heavily reused benchmarks unless the proposed estimand is genuinely different;
- questions whose novelty depends on a particular phrase not appearing;
- cross-domain analogies without compatible units and interventions; and
- projects whose only validation is model performance on random splits.

## What to do next

Do not resume Milestone 5 or start Milestone 7.

The next owner decision is whether this framework captures the right selection philosophy. If accepted, the smallest useful action is a capped domain-admission sprint: produce a diverse set of wedge cards, apply the hard gates, and return only the rejection ledger plus at most three micro-audit candidates. That sprint should have an explicit cost cap and stop if no wedge passes.

Only after seeing that result should the project amend the roadmap. Likely changes would place protocol inspection and cheap novelty killing before corpus construction, but this document does not make that amendment.
