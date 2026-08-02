# Research-cell contract

## The unit that the atlas compares

A research cell is one **study–claim–test bundle**. It is not a paper summary, a dataset listing, or a scientific topic.

Each cell answers: *a specific study used these units and measurements to make this bounded claim; this is how the claim was validated; this is the named way it could fail; and this is the public evidence needed to check it.*

This is the smallest unit that can be meaningfully compared across domains without pretending that the underlying objects are the same.

## Required blocks

| Block | Question it answers | Why it must be separate |
| --- | --- | --- |
| Source | Which primary study and exact location support this record? | A citation alone cannot support a structural claim. |
| System | What real-world system and scope is under study? | Prevents cross-domain analogy from erasing context. |
| Design | What is a unit, exposure/comparator, outcome, and time structure? | Most false cross-domain matches fail here. |
| Measurement | How are the relevant variables observed and represented in public data? | An outcome name is not a measurement rule. |
| Inference | What exact relationship or prediction is claimed, and at what scope? | Separates observation, association, prediction, and causal language. |
| Validation | What baseline, independent partition, replication, or check supports the claim? | Shows whether two studies are comparable in evidential strength. |
| Fragility | What specific artifact, confounder, or alternative explanation could change the conclusion? | Turns a similarity into a falsifiable comparison. |
| Provenance | Can source data and files actually be acquired, identified, and checked? | Makes feasibility a scientific property. |
| Decision | Is the cell a demonstration, a gated lead, an exclusion, or a deferral? | Preserves negative evidence and prevents silent promotion. |

## How cells become comparable

The graph connects only named structural roles, not topic words:

- **design role:** repeated unit, clustered unit, aggregate summary, source record, or physical specimen;
- **claim role:** association, prediction, pooled effect, or controlled comparison;
- **validation role:** independent measurement, held-unit evaluation, reconciliation, or unavailable;
- **fragility role:** measurement reuse, unit mismatch, calibration shift, scale translation, provenance reconciliation, or data closure.

A proposed overlap must share at least two roles, including a fragility or validation role, and must list one material mismatch. A single shared label, curve, or mathematical form never creates an edge.

## Non-negotiable output

Every comparison must finish with:

> **VERDICT:** [supported structural relationship / no supported relationship]. It does not establish [prohibited scientific-mechanism claim]. Candidate action: [none / named next gate].

## What a cell may not do

- infer a mechanism from a shared structure;
- promote itself to an experiment;
- replace source locations with an AI summary;
- hide a missing file, ambiguous unit, or specialist dependency;
- turn a useful exclusion into a positive signal.
