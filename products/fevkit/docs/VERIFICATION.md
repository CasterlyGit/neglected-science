# Verification contract

Run from `products/fevkit`:

```bash
PYTHONPATH=src python scripts/release_gate.py
```

The gate requires:

1. Python compilation
2. fourteen unit tests
3. a clean strict audit of the complete fixture
4. deterministic rejection of the broken fixture
5. SARIF generation
6. replay preflight
7. opt-in replay with matching expected artifact hash
8. RO-Crate export

The gate writes `VERIFICATION.json` and build artifacts locally and in CI. Passing the gate establishes only the declared software and fixture properties. It is not evidence of biological truth, clinical safety, standards endorsement, or external adoption.