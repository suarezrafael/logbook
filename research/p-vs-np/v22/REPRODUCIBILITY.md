# V22 Reproducibility

## Current status

The commands previously documented here depended on generator and dataset files that were not committed. The present package contains `verify.py`, but the verifier requires a directory containing `full_certificate_cases.json`.

Because that artifact is absent, V22 is **not reproducible from the repository**.

See [`REPRODUCIBILITY_STATUS.md`](REPRODUCIBILITY_STATUS.md) for the V61 correction record.

## Historical expected summary

The aggregate `RESULTS.json` records:

```text
cases: 125
case failures: 0
truth tables: 1022
truth-table failures: 0
all dependency identities: true
all zero-set semantics: true
all selected outputs missing: true
matches claims: true
```

This is retained as a historical run record, not as a currently reproducible result.

## Verifier interface

With a recovered or independently regenerated dataset, the verifier would be invoked as:

```bash
python verify.py <results-directory> --output independent_verification.json
```

The `<results-directory>` must contain `full_certificate_cases.json`.

## Separation of implementations

The verifier reconstructs polynomials from serialized circuit truth tables, checks dependencies coefficientwise, verifies zero-set semantics by local Hamming weights and exhaustively enumerates each small circuit range. That design remains sound, but the input artifact is missing.
