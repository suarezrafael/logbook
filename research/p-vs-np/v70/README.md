# Laboratory V70 — support frontiers, components, and gate-order heuristics

V70 studies how the order-robust projected residual DAG parameter from V69 can be upper-bounded and approximated from the support hypergraph.

## Main theorem

For a processed gate set `S`, define the support frontier

```text
F(S) = (union of supports in S) intersect (union of supports outside S).
```

Let `A(b)` be the number of nonempty affine subspaces of `GF(2)^b`. The residual layer width satisfies

```text
w(S) <= min(2^|S|, A(|F(S)|)).
```

Hence every order `pi` satisfies

```text
G_proj(pi) <= sum_i min(2^i, A(b_i)) <= m A(q(pi)),
```

where `b_i` is the frontier size at prefix `i` and `q(pi)=max_i b_i`.

This proves an FPT-size upper bound parameterized by support-frontier width. It is not a general polynomial good-order theorem.

## Component factorisation

Connected components of the processed support-incidence graph use disjoint variable sets. After dead-variable projection, the global residual-state set is the Cartesian product of the component residual-state sets. V70 exhaustively verifies this identity on 640 subset cuts from two representative systems.

## Experiments

A fixed-depth support-only lookahead substantially improves the preserved natural-order records:

| n | natural `G_proj` | lookahead-2 | exact `G*_proj` |
|---:|---:|---:|---:|
| 6 | 48 | 26 | 15 |
| 8 | 99 | 25 | 15 |
| 10 | 263 | 33 | 17 |
| 12 | 580 | 52 | 29 |
| 14 | 583 | 41 | not computed |

The exact-objective search also improves the finite robustness records to:

```text
n=8:  G*_proj=29
n=10: G*_proj=30
```

These are search-budget records, not global maxima or asymptotic lower bounds.

## Entry points

- `SUPPORT_FRONTIER_THEOREM.md` — theorem and proof.
- `COMPONENT_FACTORISATION.md` — exact product lemma.
- `HEURISTIC_BENCHMARK.md` — reproducible benchmark.
- `v70_frontier_ordering.py` — implementation and search.
- `SEARCH_SPEC.json` and `WITNESSES.json` — preserved records and provenance.
- `V70_SUPPORT_FRONTIER_THEOREM.tex` — standalone formal module.
- `PUBLICATION_READINESS.md` — conservative discovery and release plan.
- `V71_CORE_CONTEXT.md` — frozen next-lab constraints.

The direct P-versus-NP route remains inactive.
