# Security policy

Do not open a public issue containing patient data, credentials, proprietary datasets, or real secrets.

`fevkit replay --execute` runs code declared by a bundle. FEVKit requires explicit opt-in, rejects shell strings, copies the bundle, reduces the environment, enforces a timeout, and verifies declared outputs. It is **not** a security sandbox and cannot enforce network, filesystem, kernel, or hardware isolation.

Use a disposable container or microVM with network and resource policies for untrusted bundles.
