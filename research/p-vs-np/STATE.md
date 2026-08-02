# Cumulative scientific state

**Current laboratory:** V77  
**Updated:** 2026-08-01  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP research active:** exploratory  
**Direct P-versus-NP route active:** no  
**P versus NP resolved:** no  
**External review:** requested, replies pending  
**External contact:** sent  
**Publication status:** no DOI, submission, acceptance, peer review, or novelty confirmation  
**Promotion status:** V77 merged to `main` after quick, full, and LaTeX CI plus final-diff Copilot review  
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

The V76 four-cut support-boundary lemma proves that every retained label-bearing cluster is covered by the middle sets of at most four original branch-tree edges. Therefore a supplied width-`b` gate decomposition can be transferred to a rooted binary gate tree satisfying

```text
width <= 4b,
height = O(log m),
external path length = O(m log m).
```

Rebuilding the V75 symbolic residual circuit on the transferred tree gives

```text
O(m log m A(4b)^2 poly(n,m)).
```

The top-tree height construction is prior art. V76's four-edge transfer remains correct, but V77 gives a stronger parameter bound.

## V76 finite validation and proof controls

The exact subset recurrence was checked against direct tree enumeration on `1,470` small support families and `16,212` rooted trees. All `9,907` simple rank-at-most-three families on four variables through seven gates were classified. Exactly six seven-gate families exhibit a perfect-height width tradeoff. The canonical frontier is

```text
(2,4,21), (3,3,20).
```

This shows that width two cannot coexist with the minimum possible height three on that finite instance. It does not refute width-preserving `O(log m)` balancing because height four remains logarithmic.

The labelled-cluster auditor checked `101,213` valid states and attained the full four-edge cover. An independently written verifier reconstructs raw incidence boundaries, all `10,395` witness trees, cluster cuts, the six tradeoff families, and the V72 private-vertex regression.

An earlier recursive centroid argument claiming width `2b` was rejected before publication because recursive components need not remain one side of a single original edge. V77 does not revive that invalid invariant; it uses a different topology-cluster theorem.

## V77 restricted topology-tree transfer

Frederickson's restricted multilevel partitions/topology trees give a binary hierarchy of logarithmic height on a ternary tree. Every topology cluster has at most three leaving source-tree edges, and an external-degree-three cluster is necessarily a singleton vertex.

Attach each gate label to its degree-one source leaf. Delete topology branches without gate labels and suppress unary nodes. Every retained node remains an original topology cluster. If it is non-singleton, it has at most two leaving edges. If it is a singleton containing a gate label, it is a source leaf and has one leaving edge. Thus every retained label-bearing cluster has at most two boundary edges.

For any input variable occurring in a retained gate set and its complement, the path between the corresponding gate leaves exits the connected cluster through one of those boundary edges. Hence its support boundary is contained in the union of at most two original middle sets. From a supplied width-`b` decomposition, V77 obtains

```text
width <= 2b,
height = O(log m),
external path length = O(m log m).
```

Rebuilding the V75 symbolic residual circuit gives

```text
O(m log m A(2b)^2 poly(n,m))
```

incremental prefix avoidance in the supplied-decomposition parameterized regime. The logarithmic-height topology hierarchy is prior art; the retained two-edge support-boundary corollary is the internally proved V77 step. Novelty remains unconfirmed.

## V77 support-branchwidth FPT composition

For the output-gate ground set `M`, define

```text
lambda_C(S)
  = |union_{i in S} supp(i) intersect union_{i notin S} supp(i)|.
```

Each input variable contributes the cut indicator of the gates containing it. Therefore `lambda_C` is normalized, symmetric, integer valued, nonnegative, and submodular: it is a connectivity function in the exact sense required by the Korhonen--Oum branchwidth theorem. With explicit fan-in-three supports, one oracle evaluation costs `gamma=O(m)`.

Korhonen and Oum prove that a width-`k` branch decomposition of an oracle connectivity function on `m` elements can be found, or nonexistence certified, in

```text
2^{O(k^2)} gamma m^6 log m
```

time. Let `k=branchwidth(lambda_C)`. Their prior-art algorithm supplies the decomposition; V77 transfers it to width at most `2k` and logarithmic height; V75 compiles the symbolic residual DAG; and V74 follows zero-preimage prefixes. For `m>n`, the final word lies outside the range. The total runtime is

```text
2^{O(k^2)} gamma m^6 log m
  + O(m log m A(2k)^2 poly(n,m)).
```

Thus `NC0_3-Avoid` is fixed-parameter tractable when parameterized by support connectivity branchwidth **without a supplied decomposition**. This is the qualitative completion missing from V76. V77 does not implement the Korhonen--Oum algorithm; it invokes that theorem as prior art.

The connectivity-oracle audit exhaustively checks all `127` nonempty simple support families on three variables:

```text
2,186 subset values,
78,124 ordered submodularity pairs,
zero normalization, symmetry, or submodularity violations.
```

The finite audit validates the implementation. The proof is the per-variable cut-indicator decomposition.

## V77 finite validation and proof controls

The deterministic static constructor and strict verifier audited:

```text
2,055 ordered source-tree shapes through nine gates,
31,042 source vertices,
73,239 topology clusters,
33,097 retained label clusters,
zero retained clusters of external degree three,
256 seeded support systems,
5,132 direct two-edge cover checks.
```

A representative static topology certificate is committed and independently reconstructed from raw adjacency, cluster vertex sets, children, levels, and boundary edges.

All `245,505` simple rank-at-most-three support families on five variables through six gates were reduced under variable permutations to `2,802` isomorphism orbits. No perfect-height width inflation occurred in that finite range. The six V76 seven-gate witnesses remain valid regressions.

A four-gate rank-three gadget has supplied width `b=3` and a valid two-boundary-edge cluster of width six. This shows that the two-edge inequality can attain `2b` for one cluster. It does not prove that every logarithmic-height hierarchy requires factor two, and it does not refute a width-preserving transfer.

## Reproducibility and API debt frozen for V78

A clean checkout is not currently guaranteed to remain clean after the cumulative verifier. Reported causes include noncanonical JSON rewrites, committed wall-clock fields, a V53 generator that can erase the committed `scientific_status` retraction block, and stale V70/V72 snapshots. The current CI does not end with a clean-tree assertion.

V78 priority zero is therefore a reproducibility firewall:

- make committed verification artifacts deterministic and read-only by default;
- move timing measurements outside versioned snapshots;
- preserve retractions in immutable status records;
- reconcile stale snapshots;
- update `LEDGER.json` and strengthen runner coverage independently of the ledger;
- add blocking `git diff --exit-code` and clean-status gates;
- replace hand-maintained LaTeX enumeration with a validated manifest or safe discovery rule.

V78 priority one is removal of the silent `balanced_branch_tree(range(m))` fallback from theorem-facing V74/V75 APIs. Missing decompositions must fail explicitly; naive or heuristic trees may remain only in clearly named experimental helpers with measured width recorded.

Only after these controls are green should the laboratory return to factor-two-versus-width-preservation.

## Literature and scope

Frederickson supplies the restricted topology-tree hierarchy; Alstrup, Holm, de Lichtenberg, and Thorup relate topology trees to top trees. Korhonen and Oum supply exact FPT decomposition discovery for oracle connectivity functions. Fomin and Korhonen give an earlier factor-two approximation framework.

The FPT theorem remains parameterized by `k=branchwidth(lambda_C)`. V77 does not show that unrestricted circuits have bounded `k`, does not prove an unrestricted polynomial-time avoidance algorithm, and does not prove a standard-model lower bound. The direct P-versus-NP route remains inactive.

## Publication and historical controls

`v71/MANUSCRIPT.tex` remains the consolidated article through V71. V72–V77 are standalone modules pending external proof review. No ECCC/arXiv/Zenodo submission, DOI, acceptance, peer review, or novelty confirmation is claimed.

The V22 reproducibility correction remains active: V22 is a proof candidate with a missing original certificate dataset, and the aggregate snapshot cannot reconstruct the original certificates. V26 remains a justified missing-script skip. The V53 girth implications remain retracted. Incomplete `n=9` searches remain falsification/regression only. `LEDGER.json` remains a conservative historical ledger, currently records through V70, and is scheduled for reconciliation under V78 priority zero.

## Repository entry points

- `PUBLICATION_INDEX.md`
- `v77/TOPOLOGY_TREE_TRANSFER.md`
- `v77/FPT_SUPPORT_WIDTH_COMPOSITION.md`
- `v77/V77_TOPOLOGY_TREE_TRANSFER_THEOREM.tex`
- `v77/V77_FPT_SUPPORT_WIDTH_THEOREM.tex`
- `v77/topology_tree_certificate.py`
- `v77/support_connectivity_oracle.py`
- `v77/STATIC_TOPOLOGY_CERTIFICATE.json`
- `v77/RESULTS.json`
- `v77/COMPOSITION_RESULTS.json`
- `v77/V78_CORE_CONTEXT.md`
- `v76/TOP_TREE_TRANSFER.md`
- `v75/SYMBOLIC_PREFIX_CIRCUIT.md`
- `v74/TWO_FIBER_AVOIDANCE.md`
- `v71/MANUSCRIPT.tex`
