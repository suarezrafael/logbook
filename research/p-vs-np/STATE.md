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

V68 gives a stretch-one affine-cell family with exponentially many complete branching-tree leaves and a linear projected residual DAG.

V69 defines and exactly audits

```text
G*_proj = min over gate orders pi of G_proj(pi).
```

V70 proves, for support frontier `F(S)`,

```text
w(S) <= min(2^|S|, A(|F(S)|)),
G_proj(pi) <= m A(q(pi)),
```

and proves exact component factorisation of projected residual sets.

V71 identifies `q*` with vertex-boundary linear branch-width and proves for rank `r`:

```text
q* <= pw(P(H)) + 1,
pw(P(H)) <= q* + r - 1.
```

## V72 width complexity and branch DP

Private-vertex padding preserves every graph edge-cut boundary, so deciding `q*<=k` is NP-complete even for simple three-uniform support hypergraphs.

The exact subset recurrence is

```text
D[empty] = 0,
D[S] = min_{e in S} max(D[S-{e}], lambda(S)),
```

with `O(m 2^m poly(n))` time.

A supplied binary gate decomposition of boundary width `b` supports exact affine residual composition with at most `A(b)` states per node and `A(b)^2` child pairs per join.

## V73 bicriteria and counted residuals

For frontier budget `B`, V73 exactly minimizes projected residual cost using

```text
C_B(empty) = 0,
C_B(S) = min_{e in S} [C_B(S-{e}) + w(S-{e})].
```

On six frozen records, the finite price of minimum width is at most `52/29`, and one to three units of width slack attain `G*_proj`. This is not an approximation theorem.

At each branch node and residual `A`, V73 stores a multiplicity `mu_t(A)` counting consistent complete cell selections. For an exact affine decomposition of a supplied target's fibers,

```text
root multiplicity = 0 iff the supplied target is outside the image.
```

The normalized V66–V73 schema does not encode both output fibers. Cell zero of every normalized gate contains the all-zero local assignment, so the all-zero input always gives a consistent branch.

For the private-vertex partition-zero binary-tree family, rooted postorder leaves one residual per nonterminal layer, proving

```text
G*_proj=m.
```

Thus support-width growth alone does not lower-bound `G*_proj` on that family.

## V74 exact two-fiber model

Each fan-in-at-most-three Boolean gate is represented by

```text
support,
truth_mask,
output_flip.
```

The output flip records polarity. Each output bit selects its exact fiber, represented as a pairwise-disjoint union of affine cells. Internal cell branches are not circuit output bits.

Every subset of `GF(2)^3` is a disjoint union of at most three affine subspaces; seven-point fibers require three. The exhaustive minimum partition histogram over all 256 ternary subsets is:

```text
0 cells:   1
1 cell:   51
2 cells: 196
3 cells:   8
```

## V74 weighted target counting

For a branch node `t`, V74 stores a weight `mu_t(A)` for each projected residual `A` on the boundary. It counts internal assignments per boundary assignment.

At a leaf, projection from cell `C` to residual `A` contributes

```text
2^(dim(C)-dim(A)).
```

At a join, compatible child residuals intersect to `C`; projection to parent residual `P(C)` contributes

```text
mu_u(A) * mu_v(B) * 2^(dim(C)-dim(P(C))).
```

Disjoint fiber cells prevent double counting. The root weight equals the exact number of inputs mapping to the selected output word, including unused-input factors.

For boundary width `b`, there are at most `A(b)` residual keys per node and `A(b)^2` pairs per join.

## V74 constructive bounded-width avoidance

For output prefix `p`, let `N(p)` be its exact preimage count. Unfixed gates use the tautological full cube, and exact fibers give

```text
N(p0)+N(p1)=N(p).
```

Since `m>n`, start with `N(empty)=2^n<2^m`. At each position choose a child prefix whose count is below its remaining completion capacity. After `m` choices, the selected output has zero preimages.

Given a supplied width-`b` branch decomposition, runtime is

```text
O(m^2 A(b)^2 poly(n,m)).
```

This is constructive for bounded support branch width. It does not find the decomposition and does not solve unrestricted `NC0_3-Avoid`.

## V74 bicriteria bound and exact family

For a prefix-feasible system,

```text
m <= G*_proj <= C_B <= m A(B),
C_B/G*_proj <= A(B).
```

The bound is width-dependent, not rank-only.

For path variables and binary OR gates with selected output one, the primal graph has treewidth one. Endpoint order has residual profile `1,2,3,...,3`; every order satisfies the matching lower bound:

```text
G*_proj = 3m-3 for m>=2.
```

This is an exact linear all-orders lower bound, not a superpolynomial lower bound or a standard-model lower bound.

## V74 validation

```text
256 exact ternary fiber partitions,
4,096 exhaustive binary circuits,
32,768 exact target counts,
4,096 constructed avoided outputs,
2,048 polarity checks,
96 seeded ternary circuits and 1,536 targets,
OR-path exact optimization through m=9.
```

The independent verifier uses varied ternary supports, direct Boolean images, and all gate permutations for OR paths through `m=7`.

## Publication and next gates

`v71/MANUSCRIPT.tex` remains the consolidated article through V71. V72–V74 are standalone modules pending external proof review. No ECCC/arXiv/Zenodo submission, DOI, acceptance, peer review, or novelty confirmation is claimed.

Next targets are incremental prefix-count reuse, decomposition construction or approximation, tighter bicriteria bounds, bounded-treewidth superlinear families, and only size-preserving comparisons with standard models.

## Historical corrections

**V22 reproducibility correction:** the original V22 certificate dataset is absent, so V22 remains a proof candidate without repository-reproduced finite evidence. V26 remains a justified missing-script skip. The V53 girth-based claims remain retracted. Incomplete `n=9` searches remain falsification/regression only.

## Repository entry points

- `PUBLICATION_INDEX.md`
- `v74/TWO_FIBER_AVOIDANCE.md`
- `v74/V74_TWO_FIBER_AVOIDANCE_THEOREM.tex`
- `v74/two_fiber_model.py`
- `v74/or_path_family.py`
- `v74/RESULTS.json`
- `v74/V75_CORE_CONTEXT.md`
- `v73/BICRITERIA_AND_MULTIPLICITY.md`
- `v72/COMPLEXITY_AND_BRANCH_DP.md`
- `v71/MANUSCRIPT.tex`

`LEDGER.json` remains a conservative historical ledger at V70 and must be advanced without rewriting prior claims.
