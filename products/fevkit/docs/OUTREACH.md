# FEVKit outreach drafts

These are review requests, not launch announcements. Send individually after final approval.

## Framework-author review

**Subject:** A concrete implementation of Function–Evidence–Validation for biomedical agent runs

Hello [Name],

I built a small open-source implementation that turns one biomedical-agent run into separate Function, Evidence, and Validation profiles rather than a single trust score. It verifies the declared trajectory, files, claim-to-evidence edges, replay prerequisites, and the highest validation stage supported by the captured record.

Live inspector: https://fevkit.vercel.app

Source and fixtures: https://github.com/CasterlyGit/neglected-science/tree/main/products/fevkit

I am not asking for endorsement. I would value a falsification review: does the implementation materially misread your framework anywhere, especially in the cumulative V0–V4 staging or the separation between execution, evidence, and scientific correctness? One concrete objection would be more useful than general feedback.

Thank you,
Tarun S P

## Agent-platform adapter review

**Subject:** Could one sanitized [Biomni/ToolUniverse] trajectory falsify this audit layer?

Hello [Name],

I built FEVKit, a local-first audit and replay gate for scientific-agent runs. It does not replace an agent framework. It consumes a run record and checks tool versions and parameters, artifact hashes, evidence sources, claim support, uncertainty, limitations, human checkpoints, and the validation stage the run actually earned.

Live inspector: https://fevkit.vercel.app

Source: https://github.com/CasterlyGit/neglected-science/tree/main/products/fevkit

The useful next test is not another demo. It is one sanitized native [Biomni/ToolUniverse] trajectory. I would build the narrow adapter and ask you to identify where the mapping loses essential information or duplicates guarantees you already have. No patient or proprietary data is needed.

Would that be a reasonable technical review target?

Thank you,
Tarun S P

## Standards review

**Subject:** Review request: Process Run RO-Crate boundary for scientific-agent assurance

Hello [Name],

I built FEVKit, an open-source local audit layer for scientific-agent trajectories. Rather than introduce a new provenance package, it exports an RO-Crate with a Process Run profile declaration and keeps Function, Evidence, claims, and assurance metadata as an additive extension.

Source and generated fixture: https://github.com/CasterlyGit/neglected-science/tree/main/products/fevkit

I am specifically looking for a rejection-quality review of the crate boundary. Does the exporter misuse the Process Run profile, duplicate an existing representation, or overstate compatibility? I will change or remove the conformance wording rather than create another incompatible format.

Thank you,
Tarun S P
