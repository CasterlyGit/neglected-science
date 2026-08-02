# Three-target gauntlet

Status: implemented as the operating design for the next cycle. The scientific program remains paused before new target generation.

## Decision

Neglected Science will not begin by selecting a broad domain, building a corpus, generating many candidates, and discovering fatal defects near the end.

Every search cycle will begin with exactly three interview-ready target experiments. Raw ideas do not count toward three. All three will face an immediate adversarial first interview. No broad corpus, discovery engine, ranking exercise, or preregistration may begin unless the trio produces both:

1. one primary survivor; and
2. one reserve survivor.

If fewer than two targets survive, the trio fails. It is closed with its rejection evidence and replaced by a new trio. The project does not “continue anyway” with the least-bad target.

## Why this replaces the previous approach

The pilot paid for 56 sources, 65 claims, 18 candidates, and three ranked finalists before discovering that:

- one finalist was substantially answered by exact prior work;
- another combined an answered idea with a dataset that did not record the required variables; and
- the cross-domain finalist had shared vocabulary but no common measurement contract.

Those were not late-stage scientific subtleties. They were first-interview failures. The system had the right adversarial questions, but asked them at Milestone 6 instead of at entry.

The redesign moves the kill test to the front. Later novelty review remains necessary, but it confirms and deepens a challenge already passed; it is no longer the first serious attempt to invalidate the work.

## What a target is

A target is not a field, theme, dataset, or vague question. It is a compact proposed experiment containing:

- a named system and stable unit of analysis;
- a specific contrast or intervention;
- a measured outcome;
- a named public dataset or simulation source;
- a baseline or closest prior experiment;
- a falsifying result; and
- a reason either a positive or negative result matters.

If these cannot be stated before searching, the idea is not ready to occupy one of the three slots.

## Candidate factory: improve before interviewing

The generator may inspect many cheap raw leads, but it emits exactly three targets only after each lead passes five construction checks:

1. **Prior-art distance:** name the closest primary experiment and state a consequential residual difference. “Not done on this dataset/location/model” does not pass.
2. **Actual data fit:** inspect official variable/protocol documentation and a real sample; verify the unit, contrast, outcome, controls, identifiers, and independent check.
3. **Nontrivial consequence:** state what changes under positive, null, and contrary outcomes. A new plot, benchmark increment, or untested pairing does not pass.
4. **Decisive test:** show that the proposed data can distinguish the target claim from the strongest simple explanation.
5. **Bounded expertise:** identify the domain judgments and show that they are narrow enough to audit without an unbounded multi-specialty dependency.

A single failed check excludes the lead before it occupies a trio slot. The factory keeps forging replacements until exactly three pass or the cycle budget expires. This is not a promise that admitted targets will survive: it prevents known, cheap-to-detect defects from masquerading as candidates.

The three emitted targets must also satisfy the diversity rule below. Candidate quality is therefore a hard contract, not another score that a high total can compensate for.

## The trio must be intentionally diverse

The three slots should not be minor variations of one idea. That creates correlated failure and disguises a single bet as a portfolio.

Each trio should normally contain:

### Target A — Data-first

A concrete, unusually rich public dataset with protocol variation that appears scientifically underused.

The target must be based on inspected variables and protocol, not a repository landing page.

### Target B — Contradiction-first

Two primary results, models, or measurement regimes that make meaningfully different predictions under an identifiable shared condition.

The disagreement must survive basic definition and boundary-condition checks.

### Target C — Boundary-or-replication-first

An established result whose claimed scope can be tested on a consequential boundary, independent dataset, neglected population, scale, regime, or negative case.

Geographic repetition or another model architecture is insufficient unless the boundary changes the scientific claim.

Alternative trio compositions are allowed only with a written reason and comparable failure diversity.

## The first interview

The interview is a compact version of the strongest Milestone 6 attacks. It is conducted before broad ingestion. Search stops for a target as soon as one fatal answer is verified.

### Question 1 — What exact work already kills this?

Search the exact question, dataset plus outcome, instrument plus analysis, alternative terminology, and adjacent-discipline formulation. Trace the nearest paper backward to foundations and forward to later resolution.

Fatal answer: a substantively equivalent experiment already answers the proposed question, or the remaining difference is only location, model family, visualization, or benchmark score.

### Question 2 — Does the actual data record the experiment?

Inspect the variable dictionary, protocol, real sample, identifiers, units, missingness, intervention or exposure, outcome, controls, and validation route.

Fatal answer: the required variable, ordering, intervention, repeated unit, or independent outcome is absent or inseparable from protocol confounding.

### Question 3 — Is the claim merely renamed, trivial, or structurally guaranteed?

Construct the simplest explanation and ask whether the proposed result follows from normalization, local linearization, leakage, static group differences, shared definitions, or another generic artifact.

Fatal answer: the main result can occur without the proposed scientific mechanism and the data cannot discriminate the alternatives.

### Question 4 — What would a specialist call obvious or invalid?

Identify the domain judgments on which the experiment depends. Use available primary methods, official protocols, and specialist literature to anticipate the strongest objection. Record unavailable expert review explicitly.

Fatal answer: the central interpretation requires missing tacit knowledge, incompatible measurement conventions, inaccessible infrastructure, or several unrelated specialties that cannot be bounded.

### Question 5 — What changes if the answer is positive, null, or contrary?

State the scientific consequence of all three outcomes and the independent check that would make them credible.

Fatal answer: the contribution is only that a comparison has not been made, a plot has not been drawn, or predictive performance might increase slightly.

## Interview verdicts

Each target receives exactly one verdict.

### Killed

A fatal prior-art, data, construct, consequence, verification, or expertise defect is found. The evidence is retained. The target cannot be revived in the same form.

### Rewrite once

The interview exposes one precise repair that changes the scientific question rather than cosmetically narrowing it. The rewritten target is interviewed immediately in the same slot.

Only one rewrite is allowed. If the rewritten target fails, it is killed. This prevents endless reframing from consuming a full cycle.

### Admitted

No fatal defect is found in the bounded interview. “Admitted” means worthy of deeper work, not novel, correct, or selected.

The interview record must preserve the strongest unresolved risk and the exact evidence that would kill the target later.

There is no indefinite “gated” verdict at this stage. A target that requires unavailable information to pass is killed for the current cycle and may be reconsidered only when the external state changes.

## Trio pass rule

The trio passes only when at least two targets are admitted.

- The stronger survivor becomes the primary.
- The other becomes the reserve.
- If all three survive, the third remains an alternate.
- If zero or one survives, close the trio and generate three new targets.

The reserve is mandatory. It prevents a later, genuinely subtle failure from sending the project back to an empty pipeline after another expensive evidence cycle.

Primary and reserve are not chosen by a total score alone. The decision must compare:

- severity of unresolved novelty risk;
- protocol and variable adequacy;
- strength of the decisive test;
- independent verification;
- consequence of null and contrary results;
- execution cost; and
- specialist dependency.

## Hard bounds for one trio

The first interview is deliberately shallow but adversarial.

Per target, it may inspect:

- the closest primary paper and its immediate citation neighborhood;
- official dataset documentation and one real data sample;
- a small number of primary sources needed for alternative terminology or the strongest objection; and
- no more evidence once a fatal defect is verified.

It may not:

- build a broad corpus;
- extract a general claim graph;
- run discovery engines;
- train or compare predictive models;
- download large archives after a smaller protocol record has already invalidated the target;
- perform exhaustive novelty review; or
- treat missing evidence as survival.

The output is three interview records and one trio verdict, not a literature review.

## Cross-domain rule

Cross-domain work may emerge from the trio but cannot bypass it.

A cross-domain target occupies one slot only if each participating domain independently has:

- a valid measured contrast;
- adequate variables and protocol;
- a meaningful within-domain question;
- an independent check; and
- compatible experimental grammar.

Shared words or curve shapes are not enough. The cross-domain claim must predict something that could fail after transfer.

The preferred path is to admit two strong within-domain targets first. A transfer target may then be formed from them only if the comparison adds a falsifiable consequence. Cross-domain leverage never rescues a weak domain target.

## How this changes the program

The roadmap is still paused and has not yet been rewritten. When it is amended, the intended order is:

1. generate one diverse trio;
2. conduct the first interviews;
3. require a primary and reserve survivor;
4. build a bounded evidence corpus around those survivors and their strongest killers;
5. deepen candidate generation and ranking without losing the reserve;
6. conduct a later confirmation-grade novelty challenge;
7. select and preregister only after at least one target survives that confirmation.

The old Milestones 2–6 should not simply receive another preliminary checklist. Their order and gates must be changed so that target generation and adversarial admission precede territory-scale corpus work.

## Implemented controls and next action

The roadmap now places candidate construction and the first interview before broad evidence work. `schemas/candidate-admission.schema.json` and `schemas/gauntlet-replay.schema.json` govern the construction gate and replay decision. Repository tests enforce that all five construction checks must pass, exactly three ready targets are required to form a trio, and a failed batch cannot authorize later work.

The next action is to forge three new interview-ready targets under a separately authorized, bounded cycle. The historical finalist set cannot be reused.
