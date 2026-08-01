# NC0_k-Avoid Laboratory

> Structural research on Range Avoidance and circuit lower-bound interfaces. The project is motivated by P versus NP, but it does **not** claim a direct route or a solution.

## Start here

- [PUBLICATION_INDEX.md](PUBLICATION_INDEX.md) — academic entry point and theorem-status index.
- [STATE.md](STATE.md) — cumulative scientific state.
- [LEDGER.json](LEDGER.json) — conservative machine-readable historical ledger.
- [`v71/MANUSCRIPT.tex`](v71/MANUSCRIPT.tex) — current English consolidation of V54–V71.
- [`v68/`](v68/) — spine family separating branching trees from projected residual DAGs.
- [`v69/`](v69/) — exact gate-order optimization.
- [`v70/`](v70/) — support-frontier bounds and component factorisation.
- [`v71/`](v71/) — linear branch-width and pathwidth correspondence.
- [`v72/`](v72/) — rank-three width complexity and branch residual composition.
- [`v73/`](v73/) — bicriteria ordering, branch multiplicities, and tree compression.
- [`v74/`](v74/) — exact two-fiber counting and constructive bounded-width avoidance.
- [`verify_all.sh`](verify_all.sh) — cumulative quick/full verifier.

## Current position

V69 defines `G*_proj`, V70 bounds residual layers by the support frontier, V71 connects that frontier to standard width parameters, and V72 proves rank-three width NP-completeness while giving exact subset and branch-decomposition algorithms.

V73 minimizes residual cost under a frontier budget and augments branch residuals with multiplicities of complete cell choices. It also proves `G*_proj=m` for the private-vertex partition-zero binary-tree family, ruling out that family as a lower-bound candidate.

V74 replaces the normalized schema by an explicit Boolean gate model with truth masks, output polarity, and exact disjoint decompositions of both output fibers. Every ternary fiber uses at most three affine cells. A weighted branch DP computes the exact number of inputs mapping to a target output. Exact prefix counts then construct an avoided output for `m>n` in

```text
O(m^2 A(b)^2 poly(n,m))
```

when a width-`b` branch decomposition is supplied.

V74 also proves a treewidth-one family of OR gates with

```text
G*_proj = 3m-3  for m>=2.
```

This is a bounded-width algorithm and an exact linear lower-bound family. It is not an unrestricted `NC0_3-Avoid` algorithm and not a superpolynomial lower bound.

## Contribution chain

| Version | Main contribution | Status |
|---|---|---|
| V16–V27 | Finite classifications and proof candidates | Historical/supplementary |
| V53 | Corrected union-free line and retractions | Partially preserved |
| V54–V65 | Restricted algorithms, barriers, reproducibility, and formal modules | Internally verified/context |
| V66 | Exact affine-cell census and CI hardening | Merged and CI verified |
| V67 | Direct-sum proposition and overlap witnesses | Merged and CI verified |
| V68 | Exponential tree leaves and linear projected DAG | Merged and CI verified |
| V69 | Exact gate-order optimization | Merged and CI verified |
| V70 | Support-frontier theorem and component factorisation | Merged and CI verified |
| V71 | Width correspondence and consolidated manuscript | Merged after quick/full/LaTeX CI |
| V72 | Rank-three width NP-completeness and branch residual DP | Merged after quick/full/LaTeX CI |
| V73 | Bicriteria optimum, exact branch multiplicities, and tree compression | Merged after quick/full/LaTeX CI |
| V74 | Exact two fibers, weighted preimage counts, prefix avoidance, and OR-path `3m-3` | Candidate; promotion gated by quick/full/LaTeX CI |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> PR -> quick/full/LaTeX CI -> squash merge to main`. V22 and V26 remain justified skips. The direct P-versus-NP route remains inactive.
