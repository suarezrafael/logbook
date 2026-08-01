# Cumulative scientific state

**Current laboratory:** V74 candidate  
**Updated:** 2026-08-01  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP research active:** exploratory  
**Direct P-versus-NP route active:** no  
**P versus NP resolved:** no  
**External review:** requested, replies pending  
**External contact:** sent  
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

A supplied primal path decomposition constructs an order with a parameterized projected-DAG upper bound. A separate tree-decomposition DP decides affine feasibility but does not control the linear objective.

## V72 complexity and branch-decomposition results

For a graph edge `uv`, introduce a fresh private vertex `z_uv` and the three-uniform support `{u,v,z_uv}`. Private vertices never cross an edge-set cut, so every support-hypergraph boundary equals the original graph linearwidth boundary. Consequently, deciding `q*<=k` is NP-complete even for simple three-uniform hypergraphs.

V72 implements

```text
D[empty] = 0,
D[S] = min_{e in S} max(D[S-{e}], lambda(S))
```

in `O(m 2^m poly(n))` time. A supplied binary gate decomposition of maximum boundary size `b` supports exact affine residual composition with at most `A(b)` states per node and `A(b)^2` child pairs per join.

Private-vertex padding of perfect binary trees gives primal treewidth at most two but unbounded support linear width. V72 did not establish a lower bound on `G*_proj` for that family.

## V73 exact bicriteria objective

V73 minimizes residual cost subject to a frontier-width budget. Under the repository convention

```text
G_proj(pi) = sum_{i=0}^{m-1} w(P_i),
```

where `P_0=empty`, the exact recurrence is

```text
C_B(empty) = 0,
C_B(S) = min_{e in S} [C_B(S-{e}) + w(S-{e})].
```

On the six frozen V69–V70 records, the maximum finite price of minimum width is `52/29 = 1.793103...`, and one to three units of width slack attain `G*_proj`. This is finite evidence, not an approximation theorem.

## V73 counted branch residuals and normalized barrier

At each branch-decomposition node and projected affine residual `A`, V73 stores a multiplicity `mu_t(A)` equal to the number of consistent complete cell selections represented by that residual. For an exact affine decomposition of a supplied target's gate fibers,

```text
root multiplicity = 0  iff  the supplied target is outside the image.
```

The normalized V66–V73 compiler does not encode both output fibers. Cell zero of every normalized gate contains the all-zero local assignment, so the global all-zero input gives

```text
root multiplicity >= 1.
```

Internal cell branches are not output bits.

For the private-vertex partition-zero binary-tree family, rooted postorder leaves exactly one residual per nonterminal layer, proving

```text
G*_proj=m.
```

A tree-aligned decomposition has at most two states at gate leaves and exactly one at every internal node. Thus support-width hardness does not lower-bound `G*_proj` on this family.

## V74 exact two-fiber gate model

V74 represents each fan-in-at-most-three Boolean gate by:

```text
support,
truth_mask,
output_flip.
```

The output flip records polarity explicitly. For each output bit, the exact gate fiber is partitioned into pairwise-disjoint affine cells. The target bit selects a fiber; a branch bit selects a cell inside that fiber.

Every subset of `GF(2)^3` is a disjoint union of at most three affine subspaces. Seven-point fibers require three. The exhaustive minimum-cell histogram over all 256 ternary subsets is:

```text
0 cells:   1
1 cell:   51
2 cells: 196
3 cells:   8.
```

## V74 weighted preimage-count DP

For a branch-decomposition node `t`, V74 stores a weight `mu_t(A)` for each projected residual `A` on the node boundary. The weight is the number of internal assignments represented per boundary assignment.

At a leaf, projection from a cell `C` to residual `A` contributes

```text
2^(dim(C)-dim(A)).
```

At a join, compatible residuals `A` and `B` intersect to `C`; projection to the parent residual `P(C)` contributes

```text
mu_u(A) * mu_v(B) * 2^(dim(C)-dim(P(C))).
```

Disjoint fiber cells prevent double counting. The root weight is the exact number of circuit inputs mapping to the selected output word, including an explicit factor for unused inputs.

For boundary width `b`, each node has at most `A(b)` residual keys and a join tests at most `A(b)^2` pairs.

## V74 constructive bounded-width avoidance

For an output prefix `p`, let `N(p)` be the exact number of inputs whose output begins with `p`. Unfixed output gates use the tautological full cube. Exact fibers give

```text
N(p0)+N(p1)=N(p).
```

Since `m>n`, initially `N(empty)=2^n<2^m`. At every output position, choose a child prefix whose count is smaller than its number of possible completions. After `m` choices, the selected full output has count below one and therefore zero.

Given a supplied width-`b` branch decomposition, this constructs an avoided output in

```text
O(m^2 A(b)^2 poly(n,m))
```

time. The result is constructive for bounded support branch width. It does not find the decomposition and does not solve unrestricted `NC0_3-Avoid`.

## V74 bicriteria bound

For a prefix-feasible residual system and frontier budget `B`, every nonterminal layer has at least one residual and at most `A(B)` residuals. Hence

```text
m <= G*_proj <= C_B <= m A(B),
C_B/G*_proj <= A(B).
```

This is width-dependent and does not give a rank-only constant.

## V74 treewidth-one exact family

Let gate `i` be binary OR on path variables `(x_i,x_{i+1})`, and select output one. The positive fiber is the disjoint union of the affine XOR line `{01,10}` and the singleton `{11}`. The primal graph is a path, so its treewidth is one.

Endpoint order has residual profile

```text
1,2,3,3,...,3.
```

Every one-edge proper subset has two residuals. Every larger proper subset either contains a processed component of length at least two, which yields unconstrained, fixed-zero, and fixed-one residuals, or contains two isolated components, whose residual alternatives factor. Therefore every order costs at least the endpoint order, proving

```text
G*_proj = 3m-3 for m>=2.
```

This is an exact linear all-orders lower bound at treewidth one. It is not superpolynomial and is not a lower bound in a standard branching-program or proof-system model.

## V74 validation surface

The primary implementation checks:

```text
256 exact ternary fiber partitions,
4,096 exhaustive binary circuits,
32,768 exact full-target counts,
4,096 constructed avoided outputs,
2,048 output-polarity points,
96 seeded ternary circuits and 1,536 targets,
OR-path exact subset tables through m=9.
```

The independent verifier checks both fibers under both polarities, compares weighted counts to direct Boolean images on varied ternary supports, and optimizes every OR-path gate order through `m=7`. LaTeX compilation remains a separate CI job.

## Publication and discovery

`v71/MANUSCRIPT.tex` remains the current consolidated article through V71. V72, V73, and V74 are standalone theorem modules pending external review and a future manuscript revision.

No ECCC/arXiv/Zenodo submission, DOI, acceptance, peer review, or novelty confirmation is claimed.

## Next constructive and lower-bound gates

1. Reuse computations across output-prefix queries instead of rerunning the full tree DP.
2. Find or approximate a useful branch decomposition with a proved parameter guarantee.
3. Tighten the width-dependent bicriteria price bound.
4. Search for bounded-treewidth families with superlinear `G*_proj` using arbitrary exact fibers.
5. Prove a size-preserving translation before comparing weighted residuals with a standard model.
6. Reach unrestricted `NC0_3-Avoid` before evaluating any P-versus-NP consequence.

## Historical corrections

**V22 reproducibility correction:** the original V22 certificate dataset is absent, so V22 remains a proof candidate without repository-reproduced finite evidence. V26 remains a justified missing-script skip. The V53 girth-based claims remain retracted. Incomplete `n=9` searches remain falsification/regression only.

## Repository entry points

- `PUBLICATION_INDEX.md` — theorem-status and discovery index;
- `v74/TWO_FIBER_AVOIDANCE.md` — V74 definitions and proofs;
- `v74/V74_TWO_FIBER_AVOIDANCE_THEOREM.tex` — formal V74 module;
- `v74/two_fiber_model.py` — exact fibers, weighted counting, and target search;
- `v74/or_path_family.py` — exact treewidth-one family;
- `v74/RESULTS.json` — deterministic V74 snapshot;
- `v74/V75_CORE_CONTEXT.md` — frozen next-laboratory constraints;
- `v73/BICRITERIA_AND_MULTIPLICITY.md` — V73 proofs;
- `v72/COMPLEXITY_AND_BRANCH_DP.md` — V72 proofs;
- `v71/MANUSCRIPT.tex` — current consolidated manuscript.

`LEDGER.json` remains a conservative historical ledger at V70 and must be advanced in a dedicated machine-readable consolidation without rewriting prior claims.
