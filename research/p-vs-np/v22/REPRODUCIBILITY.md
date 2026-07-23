# V22 Reproducibility

## Local commands

```bash
python p_vs_np_lab_v22.py --output p_vs_np_lab_v22_results
python verify_v22_certificate.py p_vs_np_lab_v22_results \
  --output p_vs_np_lab_v22_results/independent_verification.json
```

## Expected verifier summary

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

## Separation of implementations

The primary solver constructs multilinear coefficient vectors, finds dependencies by finite-field elimination, and produces a one-violation target. The standalone verifier reconstructs the polynomials from serialized circuit truth tables, checks the dependency coefficientwise, checks zero-set semantics by local Hamming weights, and exhaustively enumerates each small circuit range.

Finite tests support implementation correctness; the asymptotic theorem rests on the human-readable proof.
