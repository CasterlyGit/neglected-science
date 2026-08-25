# Threat model

FEVKit assumes manifests may be incomplete, misleading, malformed, or malicious.

The audit addresses unresolved references, unsafe paths, missing files, digest mismatches, absent tool versions and parameters, unsupported claims, privacy contradictions, overclaimed validation, and a limited set of secret patterns.

It does not prove that the manifest contains every hidden step, that external sources were honest, that a dataset was legally obtained, or that code is safe to execute. Replay must be isolated externally for untrusted bundles.