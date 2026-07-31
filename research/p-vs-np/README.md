# NC0_k-Avoid Laboratory

> Structural research on Range Avoidance and circuit lower-bound interfaces. The project is motivated by P versus NP, but it does **not** claim a direct route or a solution.

## Start here

- [PUBLICATION_INDEX.md](PUBLICATION_INDEX.md) — academic entry point and theorem-status index.
- [STATE.md](STATE.md) — cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable claims, reproducibility, outreach and promotion ledger.
- [`v62/INTEGRATED_MANUSCRIPT.md`](v62/INTEGRATED_MANUSCRIPT.md) — historical integrated manuscript, pending V71 update.
- [`v68/`](v68/) — explicit spine family separating branching trees from projected residual DAGs.
- [`v69/`](v69/) — exact gate-order optimization and order-robustness experiments.
- [`v70/`](v70/) — support-frontier bounds, component factorisation, and ordering heuristics.
- [`verify_all.sh`](verify_all.sh) — cumulative quick/full verifier.

## Current position

V69 defines

```text
G*_proj = min_pi G_proj(pi)
```

and computes it exactly by a subset-lattice shortest path.

V70 supplies a structural upper bound. For a processed gate set `S`, let `F(S)` be the variables that occur in both processed and unprocessed supports. If `A(b)` is the number of nonempty affine subspaces of `GF(2)^b`, then

```text
w(S) <= min(2^|S|, A(|F(S)|))
G_proj(pi) <= sum_i min(2^i, A(b_i)) <= m A(q(pi)).
```

Thus bounded support-frontier width gives an FPT-size projected residual DAG. V70 also proves exact factorisation over connected components of the processed support-incidence graph.

A deterministic support lookahead reduces the preserved `n=14` fixed-order witness from `583` states to `41`. Exact-objective searches preserve new finite records `G*_proj=29` at `n=8` and `30` at `n=10`. These are search-budget records, not asymptotic lower bounds.

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
| V69 | Exact gate-order optimization and robustness audit | Merged and CI verified |
| V70 | Support-frontier theorem, component product lemma, and order heuristics | Current laboratory |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> non-draft PR -> quick/full/LaTeX CI -> squash merge to main`. V22 and V26 remain justified skips. The direct P-versus-NP route remains inactive.
