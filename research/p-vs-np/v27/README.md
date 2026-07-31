# P versus NP Lab V27

Affine-parity and balanced multi-zero range certificates for the seven cubic four-input predicate classes.

## Main result

Write each exact GF(2) algebraic normal form as

```text
f_i(x) = c_i + a_i · phi(x).
```

If `H` is a basis of the left nullspace of the nonconstant coefficient matrix `A`, every range output satisfies

```text
H y = H c.
```

Any target with another syndrome is outside the range. Nullity `t` confines the range to an affine subspace of codimension `t`, certifying at least a fraction `1-2^(-t)` of all outputs as absent.

## Verified results

- 1,280 hard truth tables;
- 640 complement pairs;
- 5,120 non-complement affine triples;
- smallest non-complement relation uses three gates;
- 96 complete circuit certificates independently verified;
- near-balanced missing targets in every benchmark;
- zero verification failures.

## Smallest local relation

The gates `0x7f80`, `0x078f`, and `0x780f` always have even output parity. Thus `001`, `010`, `100`, and `111` are absent.

## Scientific status

Internal level 4.4 candidate. Not peer reviewed. Novelty and priority are not established. This does not improve the worst-case cubic threshold for general `NC0_4-Avoid` and does not resolve P versus NP.
