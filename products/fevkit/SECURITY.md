# Security policy

## Scope

FEVKit audits local declarations and optionally executes a replay command. Treat every untrusted bundle as potentially malicious.

## Safe default

`fevkit audit` reads the manifest and declared files. It does not execute run code. The browser inspector reads a selected JSON file in memory and has no upload endpoint.

## Replay risk

`fevkit replay` is preflight-only unless `--execute` is supplied. Execution uses an argument array with `shell=False`, a temporary bundle copy, a small executable allowlist, a reduced environment, a timeout, and post-run hash comparison.

These controls reduce accidental execution risk but are not a sandbox. A permitted interpreter can still run arbitrary code. FEVKit does not enforce network isolation, operating-system permissions, process limits, container isolation, or secret-store separation.

For untrusted code, run FEVKit inside a disposable VM, hardened container, institutional compute sandbox, or equivalent control plane. Do not execute PHI-bearing or proprietary bundles on shared infrastructure without appropriate authorization and controls.

## Data handling

FEVKit sends no telemetry. The public inspector has no analytics, account, database, or upload endpoint. A bundle may still contain sensitive data; users remain responsible for authorization, access control, encryption, retention, redaction, and institutional policy.

The audit detects a small set of obvious secret patterns and privacy contradictions. It is not a data-loss-prevention product.

## Reporting

Report vulnerabilities through a private GitHub security advisory for `CasterlyGit/neglected-science` when available. Do not include patient data, private datasets, credentials, or exploitable third-party details in a public issue.