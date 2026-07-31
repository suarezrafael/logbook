# Exact gate-order optimization for projected affine residual DAGs

## Definitions

For a system of `m` two-cell affine gates and a processed gate set `S`, let `R(S)` be the set of distinct nonempty affine systems obtained by:

1. choosing one cell for every gate in `S`;
2. conjoining the selected affine equations;
3. discarding inconsistent choices; and
4. existentially projecting onto variables occurring in gates outside `S`.

Write `w(S)=|R(S)|`.

## Set-layer invariance

`R(S)` depends only on the set `S`, not on the order in which its gates were processed. Conjunction of the selected cells is order independent, and the projection target is determined by the complement of `S`.

## Ordered DAG formula

For an order `pi=(pi_0,...,pi_{m-1})`, let `S_i={pi_0,...,pi_{i-1}}`. The nonterminal states at layer `i` are exactly `R(S_i)`. Therefore

```text
G_proj(pi) = sum_{i=0}^{m-1} w(S_i).
```

## Exact optimum

Define `G*_proj=min_pi G_proj(pi)`. The optimum is the shortest path from the empty set to the full gate set in the subset lattice, with cost `w(S)` on every edge leaving `S`:

```text
DP[empty] = 0
DP[S union {g}] = min(DP[S] + w(S))  over g not in S.
```

The recurrence also reconstructs an optimal order.

## Scope

This is an exact exponential-time audit algorithm. Computing all layer widths can itself require exponentially many affine residuals, and the subset dynamic program uses `2^m` states. The theorem does not provide a polynomial good-order algorithm and does not prove an all-orders lower bound.
