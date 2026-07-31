# Support-frontier upper bound

## Definitions

Let the system have gates `1,...,m`, each supported on a subset of input variables and each offering two affine cells. For a processed set `S`, let

```text
F(S) = (union_{g in S} supp(g)) intersect (union_{g notin S} supp(g)).
```

Let `R(S)` be the set of distinct nonempty affine residuals obtained by selecting one cell for every gate in `S` and existentially projecting variables absent from all unprocessed supports. Write `w(S)=|R(S)|`.

For `b>=0`, define

```text
A(b) = sum_{d=0}^b 2^(b-d) [b choose d]_2,
```

where `[b choose d]_2` is the Gaussian binomial coefficient. This is exactly the number of nonempty affine subspaces of `GF(2)^b`.

## Theorem

For every processed set `S`,

```text
w(S) <= min(2^|S|, A(|F(S)|)).
```

Consequently, for every order `pi` with prefix sets `S_i`, frontier profile `b_i=|F(S_i)|`, and `q(pi)=max_i b_i`,

```text
G_proj(pi) = sum_i w(S_i)
           <= sum_i min(2^i, A(b_i))
           <= m A(q(pi)).
```

Therefore, if an order of support-frontier width `q` is supplied, a projected residual DAG of size at most `m A(q)` exists and is constructible by the V68 residual-state engine. In particular, the displayed counting bound is polynomial in `m` whenever `q=O(sqrt(log m))`.

## Proof

A processed gate contains only variables in the union of processed supports. After projecting every variable absent from the unprocessed supports, any surviving equation can mention only variables that occur on both sides of the cut, namely `F(S)`. Future-only variables are unconstrained by processed gates.

Thus each nonempty residual state is uniquely represented by a nonempty affine subset of `GF(2)^{F(S)}`. There are exactly `A(|F(S)|)` such subsets. Independently, there are only `2^|S|` syntactic cell selections. Both are upper bounds on `w(S)`, proving the first inequality.

V69 proves `G_proj(pi)=sum_i w(S_i)`. Summing the layer bounds proves the order-specific inequality, and monotonicity of `A` gives the final `m A(q(pi))` bound.

## Scope

The proof applies to any affine-cell system, independent of which of the six non-affine ternary NPN classes produced the cells. It does not prove that a small-frontier order always exists or can always be found in polynomial time.
