# Laboratory V22 — Zero-Set Polynomial Dependencies

## Main proof candidate

Let normalized Boolean outputs satisfy

```text
g_i(x)=1 iff p_i(x)=0,
```

where the `p_i` belong to a `D`-dimensional vector space over a field. If `m>D`, a nonzero linear dependency among the `p_i` gives an avoided output by requesting every polynomial in the dependency support to vanish except one.

For symmetric outputs of fixed fan-in at most `k`, coordinatewise complementation leaves an accepting Hamming-weight set of size at most

```text
d=floor((k+1)/2).
```

Over a prime field of characteristic greater than `k`, each output is a zero-set indicator of a multilinear polynomial of degree at most `d`. Therefore the proposed sufficient condition is

```text
m > sum_{j=0}^d binom(n,j).
```

For fan-in four:

```text
m > 1+n+binom(n,2).
```

## Scientific status after V61 audit

**Proof candidate; not repository-reproduced.**

The human-readable theorem and proof remain available. `RESULTS.json` records an earlier run claiming 125 accepted serialized certificates, but the required artifact

```text
full_certificate_cases.json
```

was never committed. The current `verify.py` requires a results directory containing that file. Aggregate counts in `RESULTS.json` are insufficient to reconstruct the original circuits, dependency coefficients and missing-output certificates.

Accordingly:

- the historical `125/125` claim is preserved as an unverified run record;
- the cumulative runner reports V22 as `SKIP` with an explicit reason;
- V22 is not listed as a repository-reproduced finite result;
- no replacement dataset will be presented as the original artifact.

See `REPRODUCIBILITY_STATUS.md`.

## Scope

This is a proof candidate for symmetric local output functions, not arbitrary `NC0_4`. It does not resolve P versus NP. Novelty and priority are not established.

## Files

- `THEOREM.md`: human-readable proof candidate;
- `RESEARCH_NOTE.md`: concise research note;
- `RESULTS.json`: aggregate historical summary;
- `verify.py`: verifier requiring the absent serialized dataset;
- `REPRODUCIBILITY_STATUS.md`: V61 correction record.
