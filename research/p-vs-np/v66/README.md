# P versus NP Laboratory V66

## Affine-cell branching on the non-affine ternary frontier

**Scientific status:** exact finite experiment for `n=3`, deterministic stress search for `n=4`, and infrastructure hardening. This laboratory does not state an asymptotic branching theorem, does not solve unrestricted `NC0_3-Avoid`, and does not imply P differs from NP.

## Main findings

Every essential non-affine ternary fiber is represented as a disjoint union of two nonempty affine cells. A branch chooses one cell per gate. Empty intersections are inconsistency leaves; consistent complete branches receive the affine certificate from V56.

Three finite parameters are recorded:

- `L_aff`: number of leaves in a lexicographically optimal inconsistency-pruned adaptive tree;
- `D_aff`: maximum depth of that tree;
- `G_aff`: number of distinct residual `(feasible inputs, remaining gates)` states reached by the selected optimal policy.

Exact results:

- the V57 gadget has 243 affine-cell partition systems; each has exactly one consistent full branch, while optimal pruning uses 8 or 9 leaves instead of 32;
- the complete `n=3` NPN-expanded domain has 168 non-affine fibers and 392 gate variants;
- after four ordered gates, exact signature-state dynamic programming reaches 919 states and no state has more than four consistent full branches;
- the canonical `n=3`, `m=4` tree census covers 40,920 multisets, with maximum `L_aff=11` and maximum observed `G_aff=17`;
- a fixed-seed sample of 50,000 `n=4`, `m=5` systems observed at most five consistent full branches, `L_aff=14`, and `G_aff=23`.

The `n=4` experiment is a falsification and regression sample, not an exhaustive n=4 theorem. The finite data do not establish polynomial branching.

## Reproduce

```bash
python verify.py
python verify_independent.py
```

The normative expected values are in `AFFINE_CELL_BRANCHING_SPEC.json`. The primary verifier regenerates `RESULTS.json`; the independent verifier rederives the exact `n=3` counts without importing the primary implementation.
