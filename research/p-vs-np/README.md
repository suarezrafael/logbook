# NC0_k-Avoid Laboratory

> Structural research on Range Avoidance and circuit lower-bound interfaces. The project is motivated by P versus NP, but it does **not** claim a direct route or a solution.

## Start here

- [STATE.md](STATE.md) — cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable claims, reproducibility, outreach and promotion ledger.
- [`v62/INTEGRATED_MANUSCRIPT.md`](v62/INTEGRATED_MANUSCRIPT.md) — integrated manuscript.
- [`v67/`](v67/) — direct-sum proposition and overlapping-support branch-growth experiment.
- [`verify_all.sh`](verify_all.sh) — cumulative quick/full verifier.

## Current position

Laboratory V67 separates two mechanisms that V66 left open.

First, direct sums of V57 affine-cell components cannot create branch growth: consistent signatures multiply, every V57 component has `c=1`, and the corresponding tree upper bound is additive across components.

Second, overlapping supports do create substantially larger finite branch sets. A deterministic seed-42 probe over 4,000 positive-fiber `0x07` systems preserves a `c=16` witness at `n=10` and finds `c=36` at `n=11`. For the stronger witness:

```text
36 <= L_aff=61 <= L_greedy=62
G_aff=108
```

This demonstrates finite overlap growth, not an exponential family or a polynomial upper bound. Tree and DAG complexity remain separate questions.

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
| V67 | Direct-sum elimination and overlap branch-growth witnesses | Current laboratory |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> non-draft PR -> quick/full CI -> squash merge to main`. V22 and V26 remain justified skips. The direct P-versus-NP route remains inactive.
