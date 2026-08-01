# Frozen context for Laboratory V74

## Stable facts

1. V73 gives an exact subset DP minimizing `G_proj` under a frontier budget.
2. On six frozen records, the exact cost at minimum width is between `1.067` and `1.793` times `G*_proj`; one to three units of width slack attain `G*_proj`.
3. A branch decomposition can count complete cell selections per projected residual exactly by storing multiplicities.
4. For exact affine decompositions of a supplied target's gate fibers, root multiplicity zero certifies an avoided target.
5. The current normalized partition schema cannot produce such a witness because the all-zero input lies in cell zero of every gate.
6. The private-vertex partition-zero binary-tree family has unbounded support linear width but exactly `G*_proj=m` under postorder.
7. A tree-aligned decomposition of that family has at most two residual states at leaves and one at every internal node.
8. No unrestricted avoidance algorithm, all-orders lower bound, standard-model simulation, novelty, peer review, or P-versus-NP consequence is proved.

## Required V74 behavior

1. Extend the data model to encode output polarity and exact representations of both gate fibers.
2. Implement target-conditioned branch counting and verify `count(y)=0 iff y` is absent on exhaustive small circuits.
3. Develop a target-search DP or prove a precise obstruction; do not confuse internal cell branches with output bits.
4. Study whether the bicriteria price can be bounded as a function of rank, width slack, or residual-state structure.
5. Search for explicit families where `G*_proj` grows despite bounded treewidth, excluding the compressed partition-zero tree family.
6. Preserve publication and external-review gates.
7. Merge only after quick, full, and LaTeX GitHub Actions pass.
