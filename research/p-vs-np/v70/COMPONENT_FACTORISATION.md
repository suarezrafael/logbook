# Component factorisation of projected residuals

Fix a processed gate set `S`. Build the incidence graph containing every gate in `S`, every variable appearing in a processed support, and an edge between a processed gate and each variable in its support.

Let its connected components be `C_1,...,C_t`. Their variable sets are disjoint. For each component, enumerate its consistent cell choices and project onto the variables of that component that still occur in unprocessed gates. Let the resulting local residual-state set be `R_j`.

## Product lemma

```text
R(S) = R_1 x ... x R_t,
w(S) = product_j |R_j|.
```

A component with no live frontier variables contributes one state if it has a consistent branch and zero otherwise.

## Why the full processed incidence graph is necessary

Components cannot be defined using only live frontier variables. Two processed gates may share a variable that has already become dead; eliminating that shared variable can correlate their surviving constraints. Including all variables from processed supports keeps such gates in the same component.

## Computational use

The lemma supports exact component-wise width computation, memoisation by component signature, support-only certificates `product_j min(2^|C_j|, A(|F_j|))`, and component-aware ordering heuristics.

V70 checks the equality independently on every subset cut of the preserved `n=6` natural-order witness and the new `n=8`, `G*_proj=29` witness: 128 plus 512 subset cuts, with zero failures.
