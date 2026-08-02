# System-1 selector v3

## Trigger

The fresh V2 pre-audit trio had primary-paper and official-inventory evidence, yet all three official content endpoints returned `Unauthorized` JSON rather than the listed files. Inventory metadata therefore overstated executable data fit.

## Change

Before a source can enter V2 pre-audit, System 1 must record one real official-file retrieval with all of:

1. the exact provider file URL or endpoint;
2. a non-error content type and plausible file signature or parse receipt;
3. a retrieved checksum matching a source-issued checksum, where the provider supplies one; and
4. a bounded structural observation from the retrieved content.

An inventory, landing page, file name, or checksum string alone is not an acquisition pass. A blocked or unauthorized retrieval is a correct `actual-data-fit` rejection, retained as negative evidence.

## Test

Run one fresh, diverse three-record source batch under V3. Compare acquisition-pass rate and correctness of rejection receipts with V2; do not compare candidate survival or scientific outcomes.
