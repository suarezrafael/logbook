# Cumulative scientific state

**Current laboratory:** V71 candidate  
**Updated:** 2026-07-31  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP research active:** exploratory  
**Direct P-versus-NP route active:** no  
**P versus NP resolved:** no  
**External review:** requested, replies pending  
**External contact:** sent  
**Promotion status:** local verification passed; pull-request CI required

## Current scientific position

V68 gives an explicit stretch-one family with exponentially many complete branching-tree leaves while the same family has a linear projected residual DAG.

V69 defines

```text
G*_proj = min over gate orders pi of G_proj(pi)
```

and proves that it is the shortest-path cost in the subset lattice of processed gate sets. This is an exact exponential-time audit algorithm.

V70 introduces the support frontier

```text
F(S) = union(processed supports) intersect union(unprocessed supports)
```

and proves

```text
w(S) <= min(2^|S|, A(|F(S)|))
G_proj(pi) <= sum_i min(2^i, A(b_i)) <= m A(q(pi)).
```

It also proves exact component factorisation of projected residual-state sets.

## V71 standard-width correspondence

Let `H` be the support hypergraph, with one labelled hyperedge per gate, and define

```text
lambda_H(S) = |V(S) intersect V(E(H) \ S)|.
```

This is exactly the V70 frontier size. Therefore

```text
q* = min_pi max_prefix lambda_H
```

is the linear branch-width of the support hypergraph under the vertex-boundary connectivity function. For ordinary graphs this specializes to classical linear-width.

If every support has size at most `r` and `P(H)` is the primal graph, V71 proves the constructive sandwich

```text
q* <= pw(P(H)) + 1
pw(P(H)) <= q* + r - 1.
```

For ternary supports:

```text
q* <= pw(P(H)) + 1
pw(P(H)) <= q* + 2.
```

A supplied width-`p` primal path decomposition gives a polynomial-time gate order with frontier at most `p+1`, and hence

```text
G_proj <= m A(p+1).
```

## Tree-decomposition result and boundary

A nice tree decomposition of primal width `k` gives an exact affine-cell feasibility DP with at most `A(k+1)` distinct affine residuals per bag and direct join cost at most `A(k+1)^2 poly(k)`.

This DP is tree-shaped and is not the linear projected residual DAG. Treewidth alone does not control the linear order parameter because trees have treewidth one and unbounded pathwidth.

## V71 finite validation

The constructive maps and inequalities were checked on:

```text
3,472 exhaustive rank-at-most-three hypergraphs on four variables,
160 seeded rank-two/three hypergraphs on five variables,
240 additional independent bit-mask instances.
```

Both V71 LaTeX documents compile in two passes locally. These checks are regressions, not the mathematical proof and not external review.

## Publication and discovery

`v71/MANUSCRIPT.tex` is the current English consolidation and `v71/THEOREM_STATUS.md` is the single status table. `v71/ECCC_METADATA.yaml` is explicitly marked `draft_not_submitted`. No ECCC/arXiv/Zenodo submission, DOI, acceptance, peer review, or novelty confirmation is claimed.

The repository license, authorship metadata, external proof review, release tag, and archive checks remain gates before public archival.

## Consequence for the projected-DAG program

V71 turns the V70 frontier parameter into a standard width interface and gives constructible FPT upper bounds on bounded-pathwidth instances. It does not prove that unrestricted support hypergraphs have small pathwidth or that a good order can always be found with polynomial width.

The competing lower-bound target remains an explicit family whose `G*_proj` is superpolynomial under every order. No simulation to OBDD, FBDD, resolution, Res-Lin, or communication complexity has been proved.

## Lower-bound route gates

1. Resolve projected-DAG order complexity across all six non-affine classes.
2. Reach unrestricted `NC0_3-Avoid` in a lower-bound-relevant stretch regime.
3. Establish a complete reduction to a lower bound strong enough to bear on NP versus polynomial-size circuits.
4. Only then evaluate a logical P-versus-NP consequence.

## Historical corrections

**V22 reproducibility correction:** the original `full_certificate_cases.json` is absent. V22 remains a proof candidate without repository-reproduced finite evidence. V26 remains a justified missing-script skip. The incomplete `n=9` search remains falsification/regression only.

## Repository entry points

- `PUBLICATION_INDEX.md` — theorem-status and discovery index;
- `v71/MANUSCRIPT.tex` — current consolidated manuscript;
- `v71/WIDTH_CORRESPONDENCE.md` — V71 definitions and proofs;
- `v71/V71_WIDTH_CORRESPONDENCE_THEOREM.tex` — standalone formal module;
- `v71/RESULTS.json` — finite validation output;
- `v71/V72_CORE_CONTEXT.md` — next laboratory constraints;
- `v70/RESULTS.json` and `v70/WITNESSES.json` — preserved V70 records.

`LEDGER.json` remains at V70 until the V71 branch passes repository CI and is promoted.
