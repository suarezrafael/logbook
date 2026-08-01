# Cumulative scientific state

**Current laboratory:** V75 candidate  
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

V68 proves an explicit stretch-one affine-cell family with exponentially many complete branching-tree leaves and a linear projected residual DAG. V69 defines and exactly optimizes `G*_proj` over gate orders. V70 bounds projected residual layers by the support frontier and proves component factorisation. V71 identifies the frontier optimum with vertex-boundary linear branch-width and relates it to primal pathwidth. V72 proves rank-three width NP-completeness, gives an exact `O(m 2^m poly(n))` subset algorithm, and establishes exact branch residual composition on a supplied decomposition. V73 adds exact budgeted ordering, counted residuals, and the private-vertex tree compression result `G*_proj=m`.

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

V74 also proves the exact OR-path residual cost `G*_proj=3m-3` for `m>=2`. This is linear and does not imply a standard-model or superpolynomial lower bound.

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

A supplied logarithmic-height tree gives `O(m log m A(b)^2 poly(n,m))`. A caterpillar has external path length `Theta(m^2)`, so V75 does not prove a general improvement for arbitrary supplied decompositions.

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

The independent verifier imports neither the arithmetic builder nor the affine engine. It reconstructs direct Boolean semantics, prefix avoidance, seeded gates, and tree-depth identities.

## Literature boundary and V76 target

Korhonen and Oum's 2026 FPT algorithm constructs width-`k` branch decompositions for oracle connectivity functions. This reduces the parameterized decomposition-discovery obstacle for the support-boundary function but does not give the logarithmic-depth guarantee needed for V75's improved incremental bound.

Bodlaender's graph tree-decomposition transformation achieves logarithmic depth with width at most `3k+2`. No transfer to the gate branch decomposition with controlled support-boundary width is claimed here.

V76 must prove a width/depth transfer, derive a weaker explicit tradeoff, or find a counterexample family. It must keep branchwidth, linear width, primal treewidth, height, external path length, arithmetic size, and dynamic work distinct.

## Publication and historical controls

`v71/MANUSCRIPT.tex` remains the consolidated article through V71. V72–V75 are standalone modules pending external proof review. No ECCC/arXiv/Zenodo submission, DOI, acceptance, peer review, or novelty confirmation is claimed.

V22 remains a proof candidate with a missing original certificate dataset. V26 remains a justified missing-script skip. The V53 girth implications remain retracted. Incomplete `n=9` searches remain falsification/regression only. `LEDGER.json` remains a conservative historical ledger and may lag the current promoted package.

## Repository entry points

- `PUBLICATION_INDEX.md`
- `v75/SYMBOLIC_PREFIX_CIRCUIT.md`
- `v75/V75_SYMBOLIC_PREFIX_THEOREM.tex`
- `v75/symbolic_prefix_circuit.py`
- `v75/RESULTS.json`
- `v75/V76_CORE_CONTEXT.md`
- `v74/TWO_FIBER_AVOIDANCE.md`
- `v71/MANUSCRIPT.tex`
