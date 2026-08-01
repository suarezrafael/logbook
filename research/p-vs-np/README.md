# NC0_k-Avoid Laboratory

> Structural research on Range Avoidance and circuit lower-bound interfaces. The project is motivated by P versus NP, but it does **not** claim a direct route or a solution.

## Start here

- [PUBLICATION_INDEX.md](PUBLICATION_INDEX.md) — academic entry point and theorem-status index.
- [STATE.md](STATE.md) — cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable historical ledger; a later consolidation will advance its promotion metadata beyond V70.
- [`v71/MANUSCRIPT.tex`](v71/MANUSCRIPT.tex) — current English consolidation of V54–V71.
- [`v68/`](v68/) — explicit spine family separating branching trees from projected residual DAGs.
- [`v69/`](v69/) — exact gate-order optimization and order-robustness experiments.
- [`v70/`](v70/) — support-frontier bounds, component factorisation, and ordering heuristics.
- [`v71/`](v71/) — support-hypergraph linear branch-width and primal pathwidth correspondence.
- [`v72/`](v72/) — rank-three width complexity and branch residual composition.
- [`v73/`](v73/) — bicriteria residual ordering, exact branch multiplicities, avoidance-interface barrier, and binary-tree compression.
- [`verify_all.sh`](verify_all.sh) — cumulative quick/full verifier.

## Current position

V69 exactly audits

```text
G*_proj = min_pi G_proj(pi).
```

V70 proves

```text
w(S) <= min(2^|S|, A(|F(S)|)),
G_proj(pi) <= m A(q(pi)).
```

V71 identifies the optimum support frontier `q*` with vertex-boundary linear branch-width and proves the bounded-rank pathwidth sandwich.

V72 proves NP-completeness of deciding `q*<=k` on simple three-uniform hypergraphs and gives exact subset and branch-decomposition algorithms.

V73 introduces the budgeted recurrence

```text
C_B(S) = min_{e in S} [C_B(S-{e}) + w(S-{e})]
```

for minimizing projected residual cost under a frontier budget. It also counts complete cell selections per branch residual exactly.

For exact affine decompositions of a **supplied** target's gate fibers, root multiplicity zero certifies an avoided target. The current normalized schema cannot search for one because cell zero of every gate contains the all-zero input.

For the V72 private-vertex partition-zero binary-tree family, a rooted postorder has one residual per layer, proving

```text
G*_proj = m
```

although support linear width is unbounded. This rules out that family as a projected-residual lower-bound candidate.

## Contribution chain

| Version | Main contribution | Status |
|---|---|---|
| V16–V27 | Finite classifications and proof candidates | Historical/supplementary |
| V53 | Corrected union-free line and retractions | Partially preserved |
| V54–V58 | Restricted algorithms and affine/bijunctive structure | Internally verified; novelty unconfirmed |
| V59–V65 | Geometry, barriers, reproducibility, manuscript, outreach, and formal modules | Verified/context |
| V66 | Exact affine-cell census and CI hardening | Merged and CI verified |
| V67 | Direct-sum proposition and overlap growth witnesses | Merged and CI verified |
| V68 | Exponential spine-tree lower bound and linear projected DAG | Merged and CI verified |
| V69 | Exact gate-order optimization and robustness audit | Merged and CI verified |
| V70 | Support-frontier theorem, component product lemma, and order heuristics | Merged and CI verified |
| V71 | Linear branch-width vocabulary, pathwidth sandwich, decomposition algorithms, and manuscript | Merged after quick/full/LaTeX CI |
| V72 | Three-uniform NP-completeness, exact width DP, branch residual DP, and width-vs-residual benchmarks | Merged after quick/full/LaTeX CI |
| V73 | Bicriteria optimum, branch multiplicities, normalized-model barrier, and `G*_proj=m` tree compression | Candidate; promotion gated by quick/full/LaTeX CI |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> PR -> quick/full/LaTeX CI -> squash merge to main`. V22 and V26 remain justified skips. The direct P-versus-NP route remains inactive.
