# NC0_k-Avoid Laboratory

> Structural research on Range Avoidance and circuit lower-bound interfaces. The project is motivated by P versus NP, but it does **not** claim a direct route or a solution.

## Start here

- [STATE.md](STATE.md) — cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable claims, reproducibility, outreach and promotion ledger.
- [`v62/INTEGRATED_MANUSCRIPT.md`](v62/INTEGRATED_MANUSCRIPT.md) — integrated manuscript.
- [`v68/`](v68/) — explicit spine family separating branching trees from projected residual DAGs.
- [`v69/`](v69/) — exact gate-order optimization and order-robustness experiments.
- [`verify_all.sh`](verify_all.sh) — cumulative quick/full verifier.

## Current position

V68 proves that complete affine-cell branching trees can be exponential while a projected residual DAG is linear for the explicit spine family.

V69 now minimizes projected-DAG size over gate orders:

```text
G*_proj = min_pi G_proj(pi).
```

For a processed gate set `S`, the projected residual layer depends only on `S`, not on the order used to reach it. Therefore a fixed order has cost

```text
G_proj(pi) = sum_i w(prefix_i),
```

and `G*_proj` is computed exactly as a shortest path in the subset lattice. The algorithm is exponential in the number of gates and is used as an audit oracle, not as an unrestricted avoidance algorithm.

Deterministic hill climbing found natural-order values `48, 99, 263, 580` for `n=6,8,10,12`, but exact optimization reduces those witnesses to `15,15,17,29`. A separate exact-objective search preserves finite budget records `G*_proj=20` at `n=6` and `28` at `n=8`. No asymptotic polynomial upper bound or all-orders lower bound follows.

## Contribution chain

| Version | Main contribution | Status |
|---|---|---|
| V16–V27 | Finite classifications and proof candidates | Historical/supplementary |
| V53 | Corrected union-free line and retractions | Partially preserved |
| V54 | Pure-`AND_k` degree separator | Verified; overlap recorded |
| V56 | Affine consistency-or-redundancy | Verified; formally packaged in V65 |
| V57 | Orbit-`0x07` block-irredundancy and direct sums | Verified construction |
| V58 | Orientation depth and parameterized avoidance | Verified; novelty unconfirmed |
| V59–V60 | Geometry, barriers and randomized regime | Verified/context |
| V61–V65 | Reproducibility, manuscript, outreach, CI and formal modules | Verified |
| V66 | Exact affine-cell census and CI hardening | Merged and CI verified |
| V67 | Direct-sum proposition and overlap growth witnesses | Merged and CI verified |
| V68 | Exponential spine-tree lower bound and linear projected DAG | Merged and CI verified |
| V69 | Exact gate-order optimization and robustness audit | Current laboratory |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> non-draft PR -> quick/full/LaTeX CI -> squash merge to main`. V22 and V26 remain justified skips. The direct P-versus-NP route remains inactive.
