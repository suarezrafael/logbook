# Laboratory V71 — linear branch-width, pathwidth, and integrated manuscript

V71 completes the width-theoretic task frozen by V70. It identifies the support-frontier parameter with a standard linear branch-decomposition parameter and derives constructive consequences from primal path decompositions.

## Main results

Let `H` be the support hypergraph: variables are vertices and one support is a hyperedge for each gate. For `S` a set of gates, define

```text
lambda_H(S) = |V(S) intersect V(E(H) \ S)|.
```

This is exactly the V70 support frontier size. Therefore

```text
q* = min over gate orders pi of max-prefix lambda_H
```

is the **linear branch-width** of the support hypergraph for the standard vertex-boundary connectivity function. For ordinary graphs this is the classical linear-width edge-layout definition.

If every support has size at most `r` and `P(H)` is the primal graph, then

```text
q* <= pw(P(H)) + 1,
pw(P(H)) <= q* + r - 1.
```

For ternary supports:

```text
q* <= pw(P(H)) + 1,
pw(P(H)) <= q* + 2.
```

A supplied primal path decomposition of width `p` yields a polynomial-time gate order with frontier width at most `p+1`. Combining this with V70 gives

```text
G_proj <= m A(p+1),
```

where `A(b)` is the number of nonempty affine subspaces of `GF(2)^b`.

## Tree-decomposition boundary

A width-`k` tree decomposition supports an exact bottom-up affine feasibility DP with at most `A(k+1)` distinct affine residuals per bag and pairwise join cost bounded by `A(k+1)^2 poly(k)`. This is a tree-shaped dynamic program, not a proof that the linear parameter `G*_proj` is small. Treewidth alone cannot control a linear layout parameter because trees have treewidth one but unbounded pathwidth.

## Finite validation

The independent constructions were checked on:

- all `3,472` simple rank-at-most-three hypergraphs on four variables with at most five hyperedges;
- `160` seeded rank-two/three hypergraphs on five variables;
- exact optimization of both linear branch-width and primal pathwidth on every tested instance.

The tests validate the constructive maps and additive inequalities; they are not the proof.

## Files

- `WIDTH_CORRESPONDENCE.md` — definitions and proofs.
- `V71_WIDTH_CORRESPONDENCE_THEOREM.tex` — standalone theorem module.
- `MANUSCRIPT.tex` — English consolidation of V54–V71.
- `THEOREM_STATUS.md` — one status table separating theorems, experiments, retractions, conjectures, and prior art.
- `v71_width_correspondence.py` — exhaustive and seeded validation.
- `verify.py` and `verify_independent.py` — primary and independent checks.
- `ECCC_METADATA.yaml` — draft submission metadata only.
- `RELEASE_PLAN.md` — metadata, licensing, archival, and submission gates.
- `V72_CORE_CONTEXT.md` — frozen next-laboratory constraints.

No ECCC submission, acceptance, DOI, peer review, novelty confirmation, unrestricted avoidance algorithm, or P-versus-NP consequence is claimed.
