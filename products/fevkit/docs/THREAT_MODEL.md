# Threat model

## Assets

- unpublished research inputs;
- patient or participant data;
- credentials and service tokens;
- proprietary code and models;
- scientific conclusions and review decisions.

## Trust boundaries

1. The manifest may be wrong or malicious.
2. Declared files may be missing, altered, or symlinked outside the bundle.
3. Replay code may be hostile.
4. A reproducible result may still be scientifically invalid.
5. A polished final claim may exceed captured evidence.
6. A local browser inspection cannot prove adjacent file integrity.

## Implemented controls

- path containment and SHA-256 verification;
- explicit privacy attestation and contradiction checks;
- bounded secret-pattern scan;
- no shell strings for replay;
- explicit `--execute`;
- copied temporary working directory;
- reduced environment and timeout;
- expected-output hash comparison;
- separate clinical and regulatory boundary warnings.

## Residual risks

FEVKit is not a sandbox, DLP system, medical device, statistical reviewer, or regulatory validator. Strong isolation requires a container or microVM with network, filesystem, identity, and resource policies.
