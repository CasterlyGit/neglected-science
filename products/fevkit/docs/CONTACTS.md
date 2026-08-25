# FEVKit outreach research

Generated from public project repositories, project documentation, institutional pages, and paper metadata on 2026-08-24. An email is listed only when it appeared in a public source retrieved during this pass. Otherwise the public project channel is retained instead of guessing an address.

## Decision

Do not begin with a broad launch or a generic “would this be useful?” campaign. The first wave is a falsification panel. Each recipient is asked to inspect one narrow boundary they are uniquely qualified to reject.

## Priority groups

1. **Function–Evidence–Validation framework authors** — review whether FEVKit preserves the semantics of separate Function, Evidence, and cumulative Validation axes.
2. **Biomni / Phylo maintainers** — provide one sanitized native run trace and pressure-test a narrow adapter.
3. **ToolUniverse / Zitnik Lab maintainers** — test whether tool versions, parameters, evidence, and claims survive as an inspectable run.
4. **Workflow Run / Process Run RO-Crate maintainers** — reject incompatible fields or overstated conformance language.
5. **BioMedArena maintainers** — test whether trajectory assurance catches failures hidden by final-answer scoring.
6. **HealthAgentBench maintainers** — review whether FEVKit can attach to benchmark runs without changing benchmark semantics.
7. **RO-Crate community maintainers** — review the broader packaging and extension boundary.

## Concrete asks

| Priority | Target | Concrete ask |
|---:|---|---|
| 1 | FEV framework authors | Name the one semantic error that would make the mapping unsafe or misleading. |
| 2 | Biomni / Phylo | Supply one sanitized native trajectory and review a Biomni-to-FEVKit adapter. |
| 3 | ToolUniverse / Zitnik Lab | Identify the smallest real trajectory that should become a conformance fixture. |
| 4 | Workflow Run RO-Crate | Review one generated crate and reject any field or wording that overstates compatibility. |
| 5 | BioMedArena | Run FEVKit on one benchmark trajectory and identify whether it exposes a hidden failure. |
| 6 | HealthAgentBench | Review attachment of FEVKit JSON/SARIF to benchmark runs. |
| 7 | RO-Crate community | Review only the crate and extension boundary, not the biomedical assurance model. |

## Send threshold

Send only after the public source path resolves, the production inspector returns HTTP 200, the release gate passes, and the complete and broken fixtures produce opposite outcomes. Do not describe FEVKit as validated, adopted, standards-conformant, clinically safe, or endorsed.

## Evidence that would kill or redirect the product

- The framework authors identify a non-repairable semantic mismatch.
- A Workflow Run RO-Crate maintainer shows that the export conflicts with an existing supported representation.
- Biomni and ToolUniverse both show that native traces already provide these guarantees in an interoperable form.
- Benchmark maintainers find that trajectory output adds no actionable information beyond existing traces and scores.
- A real adapter requires hidden proprietary fields that defeat the local, agent-neutral contract.

## Evidence that crosses the adoption threshold

- One upstream team supplies a sanitized real trace.
- One standards maintainer accepts or substantially approves the export boundary.
- One benchmark or agent team identifies a failure FEVKit catches that its current result artifact hides.
- One adapter is used in CI or a reproducible research run outside this repository.

The detailed working research, public-source URLs, extracted public contact channels, and email candidates are retained in the release evidence bundle rather than guessed into this file.