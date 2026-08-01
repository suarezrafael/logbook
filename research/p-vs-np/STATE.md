# Cumulative scientific state

**Current laboratory:** V76 candidate  
**Updated:** 2026-08-01  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP research active:** exploratory  
**Direct P-versus-NP route active:** no  
**P versus NP resolved:** no  
**External review:** requested, replies pending  
**External contact:** sent  
**Publication status:** no DOI, submission, acceptance, peer review, or novelty confirmation  
**Promotion policy:** quick, full, and LaTeX GitHub Actions plus final-diff Copilot review must pass before merge

## Structural chain through V73

V68 proves an explicit stretch-one affine-cell family with exponentially many complete branching-tree leaves and a linear projected residual DAG measured by `G_proj`. V69 defines and exactly optimizes `G*_proj` over gate orders. V70 bounds projected residual layers by the support frontier and proves component factorisation. V71 identifies the frontier optimum with vertex-boundary linear branch-width and relates it to primal pathwidth. V72 proves rank-three width NP-completeness, gives an exact `O(m 2^m poly(n))` subset algorithm, and establishes exact branch residual composition on a supplied decomposition. V73 adds exact budgeted ordering, counted residuals, and the private-vertex partition-zero/all-zero target tree compression result `G*_proj=m`.

## V74 exact two-fiber counting

Every fan-in-at-most-three Boolean gate is represented by support, truth mask, and output polarity. Both output fibers are exact pairwise-disjoint unions of affine cells; every ternary fiber needs at most three cells.

For a branch node `t`, V74 stores a weight for each projected affine residual. Leaf and join projection factors count eliminated assignments uniformly. The root weight is the exact preimage count of a supplied target or prefix. Exact fibers satisfy

```text
N(p0)+N(p1)=N(p).
```

For `m>n`, repeated exact prefix counts construct an absent output. On a supplied boundary-width-`b` gate decomposition, the runtime is

```text
O(m^2 A(b)^2 poly(n,m)).
```

V74 also proves the exact OR-path residual cost `G*_proj=3m-3` for `m>=2`. This is linear and does not imply a standard-model or superpolynomial lower bound. A later maintenance patch memoized affine fibers, branch metadata, prefix subtrees, and OR-path tables without changing the mathematical output.

## V75 paired generating polynomial

V75 introduces paired variables `z_{i,0}=u_i`, `z_{i,1}=v_i` and the polynomial

```text
P_C(u,v)=sum_x product_i z_{i,C_i(x)}.
```

Each output-word coefficient equals its exact preimage count. Prefix substitution fixes selected pairs to `1/0` and leaves both variables of unfixed outputs at one.

The V74 weighted residual recurrence is compiled into one monotone arithmetic DAG. On a supplied boundary-width-`b` branch tree, the arithmetic size is

```text
S = O(m A(b)^2).
```

Let `D_T(i)` be the operation-node dependency cone of output coordinate `i`. A complete incremental prefix search uses

```text
O(S + sum_i D_T(i))
```

arithmetic reevaluations, with

```text
D_T(i)=O(A(b)^2 depth_T(i)).
```

Therefore the parameterized runtime is

```text
O(A(b)^2 (m + sum_i depth_T(i)) poly(n,m)).
```

A supplied logarithmic-height tree gives `O(m log m A(b)^2 poly(n,m))`. A caterpillar has external path length `Theta(m^2)`, so V75 alone does not prove a general improvement for arbitrary supplied decompositions.

## V75 validation

```text
4,096 exhaustive binary circuits,
32,768 exact coefficients,
61,440 exact prefixes,
4,096 incrementally constructed avoided outputs,
48 varied-support ternary circuits on two tree shapes,
6,144 seeded coefficient checks,
12,192 seeded prefix checks,
balanced/caterpillar identities through 64 leaves.
```

The independent verifier imports neither the arithmetic builder nor the affine engine. It reconstructs direct Boolean semantics, prefix avoidance, seeded gates, and tree-depth identities. V75 was promoted after quick, full, and LaTeX CI plus final-diff Copilot review.

## V76 labelled top-tree transfer

V76 treats the supplied gate branch decomposition as a labelled subcubic tree. Standard labelled top trees, due to Alstrup, Holm, de Lichtenberg, and Thorup, give a binary hierarchy of connected clusters with at most two boundary vertices and height `O(log m)`.

The new four-cut support-boundary lemma proves that every retained label-bearing cluster is covered by the middle sets of at most four original branch-tree edges. Therefore a supplied width-`b` gate decomposition can be transferred to a rooted binary gate tree satisfying

```text
width <= 4b,
height = O(log m),
external path length = O(m log m).
```

Rebuilding the V75 symbolic residual circuit on the transferred tree gives

```text
O(m log m A(4b)^2 poly(n,m))
```

incremental prefix-avoidance time in the supplied-decomposition parameterized regime. This removes the arbitrary-tree depth obstruction at the cost of replacing `b` by `4b`.

The top-tree height construction is prior art. The V76-specific contribution is the four-cut support-boundary transfer, its exact certificate auditor, and the finite width/height/EPL analysis. Novelty remains unconfirmed.

## V76 finite validation and proof controls

The exact subset recurrence was checked against direct tree enumeration on `1,470` small support families and `16,212` rooted trees. All `9,907` simple rank-at-most-three families on four variables through seven gates were classified. Exactly six seven-gate families exhibit a perfect-height width tradeoff. The canonical frontier is

```text
(2,4,21), (3,3,20).
```

This shows that width two cannot coexist with the minimum possible height three on that finite instance. It does not refute width-preserving `O(log m)` balancing because height four remains logarithmic.

The labelled-cluster auditor checked `101,213` valid states and attained the full four-edge cover. An independently written verifier reconstructs raw incidence boundaries, all `10,395` witness trees, cluster cuts, the six tradeoff families, and the V72 private-vertex regression.

An earlier recursive centroid argument claiming width `2b` was rejected before publication because recursive components need not remain one side of a single original edge. V76 makes no factor-two claim and does not claim factor four is optimal.

## Literature and next target

Korhonen and Oum's 2026 FPT algorithm constructs width-`k` branch decompositions for oracle connectivity functions. This reduces the parameterized decomposition-discovery obstacle but is distinct from the V76 transfer on a supplied decomposition. Fomin and Korhonen study general branchwidth approximation. V77 must tighten `4b`, construct a genuine obstruction, or produce independently checkable static top-tree certificates.

## Publication and historical controls

`v71/MANUSCRIPT.tex` remains the consolidated article through V71. V72–V76 are standalone modules pending external proof review. No ECCC/arXiv/Zenodo submission, DOI, acceptance, peer review, or novelty confirmation is claimed.

The V22 reproducibility correction remains active: V22 is a proof candidate with a missing original certificate dataset, and the aggregate snapshot cannot reconstruct the original certificates. V26 remains a justified missing-script skip. The V53 girth implications remain retracted. Incomplete `n=9` searches remain falsification/regression only. `LEDGER.json` remains a conservative historical ledger and may lag the current promoted package.

## Repository entry points

- `PUBLICATION_INDEX.md`
- `v76/TOP_TREE_TRANSFER.md`
- `v76/V76_TOP_TREE_TRANSFER_THEOREM.tex`
- `v76/decomposition_pareto.py`
- `v76/cluster_cut_cover.py`
- `v76/RESULTS.json`
- `v76/V77_CORE_CONTEXT.md`
- `v75/SYMBOLIC_PREFIX_CIRCUIT.md`
- `v74/TWO_FIBER_AVOIDANCE.md`
- `v71/MANUSCRIPT.tex`
