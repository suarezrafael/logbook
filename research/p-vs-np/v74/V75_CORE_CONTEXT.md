# Frozen context for Laboratory V75

## Stable facts

1. V74 encodes arbitrary fan-in-at-most-three Boolean gates by truth masks and explicit output polarity.
2. Both output fibers are represented exactly as pairwise-disjoint affine cells.
3. Every ternary fiber needs at most three affine cells, and the eight seven-point fibers need exactly three.
4. A weighted branch-residual DP computes the exact preimage count of a target output word.
5. Exact prefix counts construct an avoided output in `O(m^2 A(b)^2 poly(n,m))` time from a supplied width-`b` branch decomposition.
6. Exhaustive validation covers all 4,096 two-input/three-output binary-gate circuits and all 32,768 targets.
7. For prefix-feasible systems, `C_B/G*_proj <= A(B)`.
8. The OR=1 path family has primal treewidth one and exact `G*_proj=3m-3` for `m>=2`.
9. No unrestricted avoidance algorithm, decomposition-construction algorithm, superpolynomial lower bound, standard-model simulation, or P-versus-NP consequence is proved.

## Required V75 behavior

1. Avoid recomputing the full weighted tree DP independently for every output prefix; seek an incremental, memoized, or symbolic prefix-count data structure.
2. Determine whether a width-parameterized branch decomposition can be found or approximated with guarantees sufficient for the V74 avoidance algorithm.
3. Tighten the `A(B)` bicriteria price bound or produce explicit instances showing substantial width-price tradeoffs.
4. Search for bounded-treewidth families with superlinear `G*_proj`, now using exact arbitrary-fiber gates rather than the compressed partition-zero schema.
5. Compare the weighted residual object with arithmetic branching programs, tensor networks, or junction-tree inference only after proving a size-preserving translation.
6. Consolidate V72–V75 into the manuscript only after external proof review and metadata checks.
7. Preserve all nonclaims and merge only after quick, full, and LaTeX GitHub Actions pass.
