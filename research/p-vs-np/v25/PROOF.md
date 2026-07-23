# Quadratic zero-set range avoidance beyond symmetric fan-in four

## Zero-set degree

For a Boolean function `f:{0,1}^4->{0,1}` and a finite field `F`, define `zdeg_F(f)` as the minimum degree of a multilinear polynomial `p` such that, after an optional output complement,

```text
f(x) xor epsilon = 1  iff  p(x) = 0.
```

Input permutations and substitutions `x_i -> 1-x_i` preserve degree, so this measure is invariant under NPN equivalence.

## Exhaustive classification

The NPN group contains `4! * 2^4 * 2 = 768` transformations. Exhaustive orbit enumeration partitions all 65,536 truth tables into 222 classes.

For a requested zero set `A`, the degree-`d` coefficient vectors that vanish on `A` form a linear kernel. A valid witness exists exactly when this kernel contains a vector outside the union of the evaluation hyperplanes indexed by the complement of `A`.

Over `GF(5)`, the exact NPN-class counts for degrees `0,1,2,3` are

```text
1, 15, 199, 7.
```

## Quadratic theorem

Let `Q5` be the set of four-input truth tables with `zdeg_GF(5) <= 2`. Consider a circuit

```text
C:{0,1}^n -> {0,1}^m
```

whose output gates belong to `Q5`, on arbitrary four-variable supports.

Choose and embed one local zero-set polynomial `p_i` for each output. Every embedded polynomial is multilinear of degree at most two, so all coefficient rows lie in a space of dimension

```text
D2(n) = 1 + n + binom(n,2).
```

If `m>D2(n)`, Gaussian elimination finds a nonzero dependency

```text
sum_i lambda_i p_i = 0.
```

Choose `j` with `lambda_j != 0`. Request normalized output one on every other coordinate in the dependency support and zero at `j`. Any realizing input would make every other support polynomial vanish. The dependency would then force `p_j=0`, contradicting the requested zero.

The same algorithm succeeds whenever the actual coefficient rank is below `m`, even when `m<=D2(n)`.

## Seven quadratic barriers

The seven hard canonical representatives are

```text
017f, 01bf, 01ef, 01fe, 07f1, 07f2, 07f8.
```

For either output orientation, the quadratic annihilator space has dimension three. Its 31 projective nonzero elements over `GF(5)` all vanish at an additional point outside the requested eight-point zero set. Therefore no quadratic zero-set polynomial exists. Cubic witnesses exist for all seven classes.

## Hard-gate-sensitive corollary

For an arbitrary four-input circuit, let `q` be the number of outputs in `Q5`, and `h` the number belonging to the seven cubic classes. With

```text
D3(n) = D2(n) + binom(n,3),
```

the two-tier dependency algorithm succeeds if

```text
q>D2(n)  or  h>D3(n).
```

The uniform pigeonhole condition `m>D2(n)+D3(n)` is included only as a completeness corollary; it is not competitive with the best general `NC0_4-Avoid` algorithms.

## Scientific limitations

The classification and certificates are computer-assisted. The proof package has not received external mathematical review. It does not resolve general `NC0_4-Avoid`, establish a new unrestricted lower bound, or resolve P versus NP.