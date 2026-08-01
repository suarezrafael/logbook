# Frozen context for Laboratory V73

## Stable facts

1. V71 identifies the support-frontier optimum `q*` with vertex-boundary linear branch-width and relates it to primal pathwidth at bounded rank.
2. V72 proves that deciding `q*<=k` is NP-complete even for simple three-uniform support hypergraphs by private-vertex padding of graph linearwidth.
3. V72 implements and validates an exact `O(m 2^m poly(n))` subset DP for `q*`.
4. A supplied binary gate decomposition of boundary width `b` supports exact affine residual composition with at most `A(b)` states per node and `A(b)^2` child pairs per join.
5. Simple three-uniform private-vertex paddings of perfect binary trees have primal treewidth at most two and unbounded linear support width.
6. On six preserved V69–V70 records, exact pathwidth-derived orders have `G_proj/G*_proj` between `1.379` and `2.059`; no approximation theorem follows.
7. Width minimization and residual-state minimization are distinct objectives.
8. No all-orders superpolynomial `G*_proj` lower bound, standard-model simulation, unrestricted avoidance algorithm, or P-versus-NP consequence is proved.

## Required V73 behavior

1. Develop a bicriteria dynamic program that minimizes projected residual cost subject to a frontier-width budget, rather than minimizing width alone.
2. Determine whether the branch-residual DP can produce an avoidance witness, not merely decide affine-cell consistency, without enumerating an exponential output space.
3. Analyze the private-vertex binary-tree family under the exact `G*_proj` objective using provable recurrences or certified larger instances.
4. Seek a rigorous lower bound on branch-residual state count, or exhibit stronger compression than the generic `A(b)` bound.
5. Compare branch-residual states with a precisely defined standard model only if a size-preserving translation is proved.
6. Preserve external-review and publication gates; do not claim novelty, peer review, DOI, submission, or a P-versus-NP implication.
7. Merge only after quick, full, and LaTeX GitHub Actions pass.
