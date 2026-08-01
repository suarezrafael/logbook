# Cumulative scientific state

**Current laboratory:** V73 candidate  
**Updated:** 2026-07-31  
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

V72 also implements

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
C_B(S) = min_{e in S} [C_B(S-{e}) + w(S-{e})],
```

with transitions allowed only when every visited subset has frontier at most `B`. Given the exact subset tables, this uses `O(m 2^m)` transitions and reconstructs an optimum order.

On the six frozen V69–V70 records:

```text
record                 q*   cost at q*   G*_proj   first budget for G*_proj
V69 natural n=6         4        18          15                6
V69 natural n=8         4        16          15                5
V69 natural n=10        4        24          17                7
V69 natural n=12        4        52          29                7
V70 exact n=8           4        31          29                6
V70 exact n=10          5        32          30                7
```

The maximum exact finite price of minimum width is `52/29 = 1.793103...`. One to three units of width slack attain `G*_proj` on these records. This is not an approximation theorem.

## V73 counted branch residuals

At each branch-decomposition node and projected affine residual `A`, V73 stores a multiplicity `mu_t(A)` equal to the number of consistent complete cell selections represented by that residual. At a join, compatible child residuals multiply their counts and equal parent residuals add them. This counts exponentially many complete branches without enumerating every leaf.

For a supplied target output word `y`, if each selected gate fiber `f_i^{-1}(y_i)` is represented as an exact disjoint union of affine cells, then

```text
root multiplicity = 0  iff  y is outside the image.
```

Thus the DP can certify an already supplied target as an avoidance witness.

## Current avoidance-interface barrier

The normalized V66–V73 `partition=0,1,2` compiler represents a selected three-point positive fiber. Cell zero of every normalized gate contains the all-zero local assignment. Therefore the global all-zero input belongs to cell zero of every gate, and every normalized instance has

```text
root multiplicity >= 1.
```

The current normalized schema cannot itself construct an avoidance witness and does not encode enough information to search over output words. The next required extension is explicit output polarity plus exact representations of both gate fibers. Internal cell-branch bits must not be confused with circuit output bits.

## V73 binary-tree compression theorem

Orient each tree edge from parent `p` to child `c`, add a private vertex `z`, and use the partition-zero cells

```text
p=0, c=0, z=0
p=0, c xor z=1.
```

A rooted postorder leaves exactly one projected residual at every nonterminal layer. Since there are `m` nonempty layers,

```text
G*_proj=m.
```

A tree-aligned branch decomposition has at most two residual states at gate leaves and exactly one residual state at every internal node. This holds while support linear width is unbounded. Hence support-width growth does not lower-bound `G*_proj` on this family.

## V73 validation surface

The primary implementation checks:

```text
48 seeded affine systems and 211 exact bicriteria budget comparisons,
96 seeded systems and 808 branch-decomposition nodes,
eight spine-family multiplicity identities through k=8,
seven binary-tree heights through m=254,
six frozen exact bicriteria records.
```

The independent verifier uses brute-force gate orders and direct Boolean-assignment signatures. LaTeX compilation remains a separate CI job.

## Publication and discovery

`v71/MANUSCRIPT.tex` remains the current consolidated article through V71. V72 and V73 are standalone theorem modules pending external review and a future manuscript revision.

No ECCC/arXiv/Zenodo submission, DOI, acceptance, peer review, or novelty confirmation is claimed.

## Lower-bound and constructive route gates

1. Encode output polarity and exact representations of both gate fibers.
2. Verify target-conditioned counting against exhaustive circuit images.
3. Develop target search without confusing internal cell branches with output bits.
4. Seek bounded-treewidth families with genuinely growing `G*_proj`, excluding the compressed partition-zero tree family.
5. Prove a size-preserving translation before importing lower bounds from a standard model.
6. Reach unrestricted `NC0_3-Avoid` in a lower-bound-relevant stretch regime.
7. Establish a complete reduction to NP circuit lower bounds before evaluating any P-versus-NP consequence.

## Historical corrections

**V22 reproducibility correction:** the original V22 certificate dataset is absent, so V22 remains a proof candidate without repository-reproduced finite evidence. V26 remains a justified missing-script skip. The V53 girth-based claims remain retracted. Incomplete `n=9` searches remain falsification/regression only.

## Repository entry points

- `PUBLICATION_INDEX.md` — theorem-status and discovery index;
- `v73/BICRITERIA_AND_MULTIPLICITY.md` — V73 proofs and avoidance-interface boundary;
- `v73/BICRITERIA_BENCHMARK.md` — six exact Pareto comparisons;
- `v73/V73_BICRITERIA_AVOIDANCE_THEOREM.tex` — standalone formal module;
- `v73/v73_bicriteria_avoidance.py` — deterministic result generator;
- `v73/RESULTS.json` — deterministic snapshot;
- `v73/V74_CORE_CONTEXT.md` — next-laboratory constraints;
- `v72/COMPLEXITY_AND_BRANCH_DP.md` — V72 proofs;
- `v71/MANUSCRIPT.tex` — current consolidated manuscript;
- `v70/RESULTS.json` and `v70/WITNESSES.json` — preserved prior records.

`LEDGER.json` remains a conservative historical ledger at V70 and must be advanced in a dedicated machine-readable consolidation without rewriting prior claims.
