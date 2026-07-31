# Frozen context for Laboratory V69

## Stable facts

1. The V68 spine family has `n=2k+1`, `m=n+1`, and `c=2^(k-1)=2^((n-3)/2)`.
2. Therefore complete inconsistency-pruned affine-cell branching trees require exponentially many leaves on this family.
3. Under existential projection onto future-active variables, the same family has an explicit ordered DAG with `G_proj=3k+4` nonterminal states.
4. `G_proj` is repository-local and is not identified with OBDD, FBDD, resolution, Res-Lin, or another standard proof system.
5. The direct P-versus-NP route remains inactive.
6. Earliest external follow-up date remains 2026-08-24.

## Required V69 behavior

1. Search for an explicit family with superpolynomial `G_proj`, or a general polynomial construction for projected affine residual DAGs.
2. Treat tree and projected-DAG complexity as separate objects.
3. Extend the bitset engine to gate-order optimization, component decomposition, and all six non-affine ternary classes.
4. Test parity/support-expansion and Tseitin-style incidence patterns only as experiments until a formal simulation is proved.
5. Preserve the smallest witness for every new `G_proj` record and verify it independently.
6. If invoking OBDD/FBDD or proof-complexity lower bounds, first state and prove a size-preserving simulation theorem.
7. Do not infer unrestricted `NC0_3-Avoid`, a circuit lower bound, or P versus NP from the spine theorem.
8. Merge only after quick, full, and LaTeX CI pass.
