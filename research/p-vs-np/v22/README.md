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

## Verification

- 1,022 symmetric truth-table normalizations;
- 65 circuits above the uniform dimension threshold;
- 60 rank-deficient circuits below that threshold;
- 125/125 complete certificates independently accepted;
- every selected target compared with the complete range on the test instances.

## Scope

This is a proof candidate for symmetric local output functions, not arbitrary `NC0_4`. It does not resolve P versus NP. Novelty and priority are not established.

## Files

- `THEOREM.md`: human-readable proof;
- `RESEARCH_NOTE.md`: concise research note;
- `RESULTS.json`: machine-readable summary;
- `verify.py`: standalone certificate verifier.
