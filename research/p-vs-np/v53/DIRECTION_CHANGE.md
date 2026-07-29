# V53 direction change — from NC⁰₄ to NC⁰₃, with V54 correction

The strategic move from `NC⁰₄` to stretch-one `NC⁰₃-Avoid` remains justified:

- `NC⁰₂-Avoid` has a polynomial-time algorithm;
- stretch-one `NC⁰₃-Avoid` remains open;
- important explicit-construction problems already reduce to `NC⁰₄-Avoid`;
- cryptographic work gives evidence against overly general deterministic Avoid algorithms, without directly ruling out stretch-one `NC⁰₃-Avoid`.

## Preserved V53 theorem

For a pure `AND₃` circuit, output monomials indexed by edge subfamilies map to input monomials indexed by their vertex unions. Therefore bounded-size union-distinctness implies injectivity of the substitution and excludes low-degree vanishing identities.

## Retracted V53 claim

The original V53 package incorrectly claimed:

```text
incidence girth > 4t
        => t-union-free
        => syndrome degree > t.
```

The first implication is false for nested collisions. After removing common edges from equal-union families, one residual family may be empty.

An edge may be covered by the union of other edges even when the incidence graph is acyclic. Consequently, the claimed stretch-one family with syndrome degree `Ω(log n)` is retracted.

## Correct replacement from V54

Every positive-excess `k`-uniform support hypergraph has a nonempty 2-core. A core edge is covered by at most one witness edge through each of its vertices, producing:

```text
(1-Y_e) product_f Y_f = 0
```

with degree at most `k+1`.

For pure `AND₃`, an explicit missing target always has separating degree at most four.

## Methodological lesson

The target `NC⁰₃-Avoid` remains correct, but the lesson changed:

```text
high girth
    does not prevent
nested cover relations.
```

Future work must move beyond singleton-fiber gates and must run both cycle and cover/union-collision regressions before promoting asymptotic claims.
