# Integration guide

FEVKit is an export boundary around systems that already exist.

At the end of a run, map native events to:

- `steps`: ordered decisions and tool calls;
- `inputs` and `artifacts`: content-addressed files;
- `evidence`: source snapshots and software/model outputs;
- `claims`: bounded statements with support relations;
- `validation`: evaluations actually performed;
- `human_checkpoints`: review decisions and authority boundaries.

Then run:

```bash
fevkit audit /path/to/bundle --profile generic
```

## CI gate

```yaml
- name: Audit scientific trajectory
  run: fevkit audit run-bundle --format sarif --output fevkit.sarif
```

The command exits with code `2` when deterministic errors are present.

## Private environments

FEVKit requires no hosted service. Keep sensitive bundles inside the lab's existing infrastructure. Publish only redacted manifests or RO-Crates that have passed local governance review.
