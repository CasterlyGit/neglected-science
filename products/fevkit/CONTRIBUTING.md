# Contributing

1. Describe the scientific workflow and failure mode.
2. Add a deterministic fixture.
3. Add a test that fails before the change.
4. Preserve distinctions between execution, reproducibility, scientific evaluation, and prospective validation.
5. Do not add a global trust score.
6. Do not add patient data, proprietary datasets, secrets, or unverifiable scientific claims.

```bash
python -m unittest discover -s tests -v
python -m fevkit audit examples/complete --profile differential-expression
python -m fevkit replay examples/complete --execute
```
