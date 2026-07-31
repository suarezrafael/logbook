# Laboratory V68 — spine tree–DAG separation

V68 answers the tree-side question left by V67 with an explicit stretch-one family.

For every `k>=1`, the spine system `S_k` has

```text
n = 2k+1
m = 2k+2 = n+1
c(S_k) = 2^(k-1) = 2^((n-3)/2)
```

All gates lie in the NPN orbit of `0x07`, and every selected branch cell is affine. Since every consistent complete branch requires a distinct complete leaf, every inconsistency-pruned branching tree has at least `2^(k-1)` leaves.

The same family has a linear explicit DAG after existentially projecting variables that do not occur in remaining gates. Under the fixed V68 ordering, the projected residual DAG has exactly `3k+4` nonterminal states. This parameter is named `G_proj`; it is not the historical `G_aff`, and no equivalence to OBDD, FBDD, resolution, Res-Lin, or another standard proof system is claimed.

## Entry points

- `SPINE_FAMILY_THEOREM.md` — construction and proof.
- `V68_SPINE_TREE_DAG_THEOREM.tex` — standalone formal module.
- `v68_spine_family.py` — generator, exact checks and `c=36` structural analysis.
- `affine_bitset.py` — persistent bitset RREF and projected-state hashing.
- `PROJECTED_DAG_MODEL.md` — exact quotient used by `G_proj`.
- `C36_STRUCTURE_ANALYSIS.md` — reconstruction of the V67 witness mechanism.
- `PROOF_COMPLEXITY_BOUNDARY.md` — claim boundary around OBDD/FBDD/Tseitin analogies.
- `verify.py` and `verify_independent.py` — primary and independent checks.

## Reproduce

```bash
python v68_spine_family.py
python verify.py
python verify_independent.py
```

The direct P-versus-NP route remains inactive. V68 proves a barrier for one branching-tree method and an upper bound for one explicit family; it does not solve unrestricted `NC0_3-Avoid` or establish a circuit lower bound.
