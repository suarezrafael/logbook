# V22 reproducibility repair

## Finding

`v22/verify.py` requires a positional results directory and reads:

```python
results / "full_certificate_cases.json"
```

The file is absent from the pull-request tree. `v22/RESULTS.json` contains aggregate counts but no serialized circuits or dependency certificates.

## Decision

The original 125 cases are not reconstructible from the committed aggregate file.

V61 therefore:

1. marks V22 as a proof candidate without repository-reproduced finite evidence;
2. changes the cumulative runner from an unavoidable `FAIL` to an explicit `SKIP`;
3. preserves the human theorem and historical aggregate record;
4. forbids relabeling a newly generated dataset as the original artifact.

## Why this is not a retraction of the theorem candidate

The missing artifact establishes a reproducibility failure, not a mathematical counterexample. The proof must be reviewed on its own merits. The numerical certificate claims cannot currently serve as independent support.

## Closure criteria

The issue closes only if the original artifact is recovered with provenance, or a fresh independent reproduction is created and labeled with a new version and hash.
