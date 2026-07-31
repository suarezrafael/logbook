# Frozen context for Laboratory V70

## Stable facts

1. V68 gives an exponential complete-tree lower bound and a linear projected DAG for the spine family.
2. V69 defines `G*_proj=min_pi G_proj(pi)` and proves exact subset-lattice optimization.
3. Natural-order adversarial records through `n=12` collapse to small exact optima (`15,15,17,29`).
4. A finite exact-objective search preserves `G*_proj=20` at `n=6` and `28` at `n=8`; these are budget records, not asymptotic evidence.
5. No polynomial good-order theorem and no all-orders superpolynomial lower bound is proved.
6. No standard proof-system simulation is proved.
7. The direct P-versus-NP route remains inactive.

## Required V70 behavior

1. Develop polynomial-time ordering heuristics from support separators, elimination width, and component decomposition.
2. Compare heuristic orders against exact `G*_proj` on all tractable preserved witnesses.
3. Search for families robust under every tested order, optimizing the exact objective only where feasible.
4. Attempt a parameterized upper bound in support-graph treewidth or separator size.
5. Treat communication complexity, OBDD/FBDD, and Tseitin lower bounds as unavailable until a size-preserving simulation is proved.
6. Preserve every new record and verify it independently.
7. Do not infer unrestricted `NC0_3-Avoid`, circuit lower bounds, or P versus NP.
8. Merge only after quick, full, and LaTeX CI pass.
