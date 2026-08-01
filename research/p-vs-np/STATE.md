# Cumulative scientific state

**Current laboratory:** V72  
**Updated:** 2026-07-31  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP research active:** exploratory  
**Direct P-versus-NP route active:** no  
**P versus NP resolved:** no  
**External review:** requested, replies pending  
**Publication status:** no DOI, submission, acceptance, peer review, or novelty confirmation  
**Promotion policy:** quick, full, and LaTeX GitHub Actions must pass before merge

## Structural chain

V68 gives an explicit stretch-one affine-cell family with exponentially many complete branching-tree leaves and a linear projected residual DAG.

V69 defines

```text
G*_proj = min over gate orders pi of G_proj(pi)
```

and computes it exactly by a subset-lattice shortest path.

V70 proves, for support frontier `F(S)`,

```text
w(S) <= min(2^|S|, A(|F(S)|)),
G_proj(pi) <= m A(q(pi)),
```

and proves exact component factorisation of projected residual sets.

V71 identifies `q*` with vertex-boundary linear branch-width of the support hypergraph and proves, for rank `r`,

```text
q* <= pw(P(H)) + 1,
pw(P(H)) <= q* + r - 1.
```

A supplied primal path decomposition therefore constructs an order with a parameterized projected-DAG upper bound. A separate tree-decomposition DP decides affine feasibility but does not control the linear objective.

## V72 complexity result

For a graph edge `uv`, introduce a fresh private vertex `z_uv` and the three-uniform support

```text
{u,v,z_uv}.
```

Private vertices never cross an edge-set cut, so every support-hypergraph boundary equals the original graph linearwidth boundary. Consequently, deciding `q*<=k` is NP-complete even for simple three-uniform hypergraphs.

The claim concerns ordering-width computation. It is not NP-hardness of Range Avoidance and does not imply a circuit lower bound.

## V72 exact width algorithm

For every processed edge set `S`, V72 implements

```text
D[empty] = 0,
D[S] = min_{e in S} max(D[S-{e}], lambda(S)).
```

The algorithm computes `q*` and an optimal labelled-edge order in

```text
O(m 2^m poly(n)) time
```

with `O(2^m)` stored values. It is an exact exponential audit, not a polynomial unrestricted algorithm.

## V72 branch residual algorithm

Given a binary tree over the gates, a node stores the distinct affine residuals on variables shared with the complementary gates. Child residuals are conjoined, inconsistent pairs are removed, and surviving systems are projected to the parent boundary.

For maximum boundary size `b`:

```text
states per node <= A(b),
pairs per join <= A(b)^2,
total time <= O(m A(b)^2 poly(n)).
```

This is an exact tree-shaped affine feasibility DP. No OBDD, FBDD, resolution, Res-Lin, communication, or proof-system equivalence is asserted.

## Bounded treewidth versus linear width

Private-vertex padding of a tree replaces every edge with a triangle. The primal graph has treewidth at most two, while every support cut preserves the graph edge boundary. Perfect binary trees therefore yield a simple three-uniform family with bounded primal treewidth and unbounded linear support width.

This proves that bounded treewidth does not imply bounded `q*`. It does not prove that `G*_proj` is unbounded or superpolynomial on this family.

## Preserved-record benchmark

Exact pathwidth-derived orders were evaluated on six frozen V69–V70 instances:

```text
record                   path G_proj   exact G*_proj   ratio
V69 natural n=6               21            15        1.400
V69 natural n=8               28            15        1.867
V69 natural n=10              35            17        2.059
V69 natural n=12              57            29        1.966
V70 robust n=8                40            29        1.379
V70 robust n=10               50            30        1.667
```

These six values are finite evidence only. Width minimization and residual-state minimization are distinct objectives.

## V72 validation surface

The primary implementation checks:

```text
1,470 exhaustive rank-at-most-three width instances,
96 seeded affine systems and 852 branch-tree nodes,
six preserved-record pathwidth benchmarks,
three finite padded-binary-tree instances.
```

The independent verifier uses separate bit-mask boundaries and Boolean assignment semantics. LaTeX compilation is a separate CI job.

## Publication and discovery

`v71/MANUSCRIPT.tex` remains the current consolidated article through V71. V72 is packaged as a standalone theorem module and a scoped prior-art appendix pending external review and a future manuscript revision.

No ECCC/arXiv/Zenodo submission, DOI, acceptance, peer review, or novelty confirmation is claimed.

## Lower-bound route gates

1. Optimize residual cost under a width budget rather than width alone.
2. Determine whether branch residual composition can construct an avoidance witness efficiently.
3. Establish a provable `G*_proj` recurrence or lower bound on an explicit bounded-treewidth family.
4. Prove a size-preserving translation before importing lower bounds from a standard model.
5. Reach unrestricted `NC0_3-Avoid` in a lower-bound-relevant stretch regime.
6. Establish a complete reduction to NP circuit lower bounds before evaluating any P-versus-NP consequence.

## Historical corrections

The V53 girth-based claims remain retracted. The original V22 certificate dataset is absent, so V22 remains a proof candidate without repository-reproduced finite evidence. V26 remains a justified missing-script skip. Incomplete `n=9` searches remain falsification/regression only.

## Repository entry points

- `PUBLICATION_INDEX.md` — theorem-status and discovery index;
- `v72/COMPLEXITY_AND_BRANCH_DP.md` — V72 proofs;
- `v72/PATHWIDTH_BENCHMARK.md` — six preserved-record comparisons;
- `v72/V72_BRANCH_RESIDUAL_THEOREM.tex` — standalone formal module;
- `v72/v72_branch_residual.py` — exact and branch algorithms;
- `v72/RESULTS.json` — deterministic snapshot;
- `v72/V73_CORE_CONTEXT.md` — next-laboratory constraints;
- `v71/MANUSCRIPT.tex` — current consolidated manuscript;
- `v70/RESULTS.json` and `v70/WITNESSES.json` — preserved prior records.

`LEDGER.json` remains a conservative historical ledger at V70 and must be advanced in a dedicated machine-readable consolidation without rewriting prior claims.
