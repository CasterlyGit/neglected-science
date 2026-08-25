# Versioning policy

Package versions follow semantic versioning. The run manifest has its own `spec_version`. A package may read more than one manifest version, but a breaking manifest change must never be hidden inside a package patch release.

Audit-rule changes that can turn an existing PASS into FAIL require a changelog entry and an adversarial fixture.