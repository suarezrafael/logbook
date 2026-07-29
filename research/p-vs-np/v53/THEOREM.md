# V53 theorem status — corrected by V54

## Preserved theorem

Let `H=(V,E)` be a 3-uniform hypergraph and define

```text
C_H(x)_e = product_{v in e} x_v.
```

If any two distinct edge subfamilies of size at most `t` have distinct vertex unions, then the substitution

```text
Y_e -> product_{v in e} X_v
```

is injective on multilinear output polynomials of degree at most `t`. Consequently, over every field,

```text
sd_F(Range(C_H)) > t.
```

This is the valid central theorem of V53.

## Retracted statements

The following statements from the original V53 package are false and retracted:

1. `incidence_girth(H) > 4t` implies full `t`-union-freeness;
2. the derived stretch-one `AND3` family with syndrome degree `Omega(log n)`.

The proof failed for nested equal-union collisions. For example, an edge can be contained in the union of three other edges even when the incidence graph is a tree.

## Correct replacement from V54

Every `k`-uniform hypergraph with more edges than vertices has a nonempty 2-core. A core edge is contained in the union of at most `k` other core edges, yielding

```text
(1-Y_e) product_f Y_f = 0
```

on the image. Thus pure `AND_k` has an explicit separator of degree at most `k+1`; in particular, positive-stretch pure `AND3` has degree at most four.

The finite V53 examples remain correct:

```text
UF2: exact syndrome/separating degree 3,
UF3: exact syndrome/separating degree 4.
```

Use Laboratory V54 for the proofs, validation, and current scientific status.
