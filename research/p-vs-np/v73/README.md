# Laboratory V73 — Bicriteria ordering and counted branch residuals

V73 separates three questions that were conflated in earlier width experiments:

1. minimize projected residual cost while respecting a frontier-width budget;
2. count complete affine-cell branches on a supplied branch decomposition;
3. determine whether that branch computation can actually produce a Range Avoidance witness.

## Main results

- An exact subset DP computes the optimum `G_proj` among orders whose support frontier never exceeds a supplied budget `B`.
- A multiplicity-enhanced branch DP counts complete cell selections represented by every projected residual without enumerating all branch leaves.
- For a **supplied target output** with exact affine decompositions of its gate fibers, root multiplicity zero certifies that target outside the image.
- The current normalized `partition=0,1,2` schema cannot discover such a witness: cell zero of every normalized gate contains the all-zero input, so the all-zero complete branch is always consistent.
- On the V72 private-vertex binary-tree family, a postorder has one projected residual at every layer. Hence `G*_proj=m` although support linear width is unbounded.
- A tree-aligned branch decomposition of that family uses at most two states at gate leaves and exactly one state at every internal node.

## Reproduce

```bash
python v73_bicriteria_avoidance.py
python verify.py
python verify_independent.py
```

The package is exploratory and internally verified. It does not claim novelty, peer review, unrestricted `NC0_3-Avoid`, a standard-model simulation, or a P-versus-NP consequence.
