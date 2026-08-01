# Frozen context for Laboratory V72

## Stable facts

1. V71 identifies `q*` exactly as linear branch-width of the support hypergraph under vertex-boundary connectivity.
2. For rank `r`, `q* <= pw(primal)+1` and `pw(primal) <= q*+r-1`.
3. A supplied width-`p` primal path decomposition constructs an order with `G_proj <= m A(p+1)`.
4. A tree decomposition yields an affine feasibility DP but does not imply a small linear `G*_proj`.
5. The integrated manuscript and draft submission metadata exist, but no external publication or peer review is claimed.
6. No general polynomial good-order theorem, all-orders lower bound, standard-model simulation, unrestricted avoidance algorithm, or P-versus-NP consequence is proved.

## Required V72 behavior

1. Determine the computational complexity of minimizing support-hypergraph linear branch-width for rank-three systems, with exact reductions or carefully scoped prior art.
2. Implement an FPT or approximation pipeline that consumes a path decomposition and compare its orders against V70 exact `G*_proj` records.
3. Search for families with bounded treewidth but growing `G*_proj`, separating tree-shaped feasibility DP from linear residual DAG complexity.
4. Test whether branch decompositions, rather than path decompositions, support a rigorously defined non-linear residual DAG with compositional size bounds.
5. Seek external review of the V70–V71 proofs before any public DOI or submission claim.
6. Preserve all nonclaims and merge only after quick, full, and LaTeX CI pass.
