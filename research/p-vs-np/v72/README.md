# Laboratory V72 — exact linear width and branch residual composition

V72 studies the computational and algorithmic consequences of the V71 identification of support-frontier width with a standard hypergraph layout parameter.

## Main results

### 1. Complexity at rank three

The decision problem

```text
Input: a support hypergraph H and integer k.
Question: is its vertex-boundary linear branch-width at most k?
```

is NP-complete even for simple three-uniform hypergraphs.

Membership in NP is witnessed by a labelled hyperedge order. For hardness, start with a graph `G` and replace each graph edge `uv` by the triple

```text
{u,v,z_uv},
```

where `z_uv` is private to that edge. Private vertices never cross a cut, so every cut has exactly the same boundary as the corresponding edge cut of `G`. The reduction therefore preserves linearwidth exactly.

### 2. Exact subset dynamic program

For a processed edge set `S`, write `lambda(S)` for its vertex boundary. V72 implements

```text
dp[S] = min over e in S of max(dp[S - {e}], lambda(S)).
```

This computes the optimum and an order in

```text
O(m 2^m poly(n))
```

time and `O(2^m)` stored states.

The implementation is checked against permutation enumeration on 1,470 rank-at-most-three hypergraphs.

### 3. Branch residual dynamic program

Given a rooted binary decomposition of the gate set, every node stores the distinct affine residuals on the variables shared with the complementary gates.

If the maximum boundary size is `b`, each node stores at most `A(b)` residuals, and each internal node considers at most `A(b)^2` child pairs. The result is an exact tree-shaped affine feasibility algorithm with bound

```text
O(m A(b)^2 poly(n)).
```

This is not the linear `G_proj` model and is not asserted to be an OBDD, FBDD, resolution, or Res-Lin simulation.

### 4. Bounded treewidth does not control linear width

Private-vertex padding of a tree replaces every tree edge by one triangle. The resulting primal graph has treewidth at most two, while the support-hypergraph linear width equals the graph linearwidth of the original tree. Perfect binary trees therefore give a rank-three family of bounded primal treewidth and unbounded linear support width.

This separates tree-shaped feasibility from linear-order complexity. It does not prove that `G*_proj` is superpolynomial.

## Preserved-record benchmark

Exact primal-pathwidth orders were reconstructed for six V69–V70 records. Their projected-DAG sizes were between `1.38` and `2.06` times the exact preserved `G*_proj` values. These are six finite records, not an approximation theorem.

## Entry points

- `COMPLEXITY_AND_BRANCH_DP.md` — definitions and proofs;
- `PATHWIDTH_BENCHMARK.md` — six preserved-record comparisons;
- `PRIOR_ART.md` — scoped literature audit;
- `v72_branch_residual.py` — exact width and residual-DP implementation;
- `verify.py` and `verify_independent.py` — primary and independent checks;
- `V72_BRANCH_RESIDUAL_THEOREM.tex` — standalone theorem module;
- `RESULTS.json` — deterministic result snapshot;
- `V73_CORE_CONTEXT.md` — frozen next-laboratory constraints.

## Scientific boundary

V72 does not prove a polynomial good-order theorem for unrestricted instances, an all-orders superpolynomial lower bound for `G*_proj`, a standard proof-system simulation, unrestricted `NC0_3-Avoid`, or a P-versus-NP consequence. Novelty and peer review remain unconfirmed.
