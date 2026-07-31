# Proof-complexity boundary

The V68 projected residual DAG is adjacent in spirit to state merging in OBDD/FBDD algorithms and branching-program proof systems, but there is **no simulation theorem** in the repository.

## What V68 establishes

- an exponential lower bound for complete leaves in the specified affine-cell branching-tree model on the spine family;
- a linear explicit upper bound for `G_proj` on the same family;
- a concrete separation between retaining full branch history and projecting dead variables.

## What V68 does not establish

- an OBDD, FBDD, resolution, Res-Lin, or tree-like parity-resolution lower bound;
- equivalence between `G_proj` and a minimum branching program;
- hardness of Tseitin formulas in the affine-cell model;
- a transfer from existing Tseitin/expander lower bounds.

Tseitin-style expander constructions remain a motivated future experiment only. Before importing any known lower bound, V69 must define a size-preserving simulation in at least one direction and verify that the affine-cell transition and terminal semantics match the target model.
