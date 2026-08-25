# Process Run RO-Crate export

FEVKit does not define a competing research-object format.

`fevkit export-rocrate` emits:

- RO-Crate 1.1 metadata;
- conformance to `https://w3id.org/ro/wfrun/process/0.5`;
- a `CreateAction` describing the captured run;
- copied input and output files with SHA-256 metadata;
- declared software applications;
- the original `run.json`;
- the deterministic FEVKit audit report.

FEV-specific stage and qualifier fields are additive metadata. Downstream tools may ignore them and still consume the crate as a normal Process Run Crate.
