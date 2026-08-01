# NC0_k-Avoid Laboratory

> Structural research on Range Avoidance and circuit lower-bound interfaces. The project is motivated by P versus NP, but it does **not** claim a direct route or a solution.

## Start here

- [PUBLICATION_INDEX.md](PUBLICATION_INDEX.md) — academic entry point and theorem-status index.
- [STATE.md](STATE.md) — cumulative scientific state.
- [LEDGER.json](LEDGER.json) — conservative machine-readable historical ledger.
- [`v17/`](v17/) and [`v20/`](v20/) — archived historical packages.
- [`v71/MANUSCRIPT.tex`](v71/MANUSCRIPT.tex) — current English consolidation through V71.
- [`v68/`](v68/) — spine family separating branching trees from projected residual DAGs.
- [`v69/`](v69/) — exact gate-order optimization.
- [`v70/`](v70/) — support-frontier bounds and component factorisation.
- [`v71/`](v71/) — linear branch-width and pathwidth correspondence.
- [`v72/`](v72/) — rank-three width complexity and branch residual composition.
- [`v73/`](v73/) — bicriteria ordering, branch multiplicities, and tree compression.
- [`v74/`](v74/) — exact two-fiber counting and constructive bounded-width avoidance.
- [`v75/`](v75/) — symbolic paired-variable counting and incremental prefix evaluation.
- [`verify_all.sh`](verify_all.sh) — cumulative quick/full verifier.

## Current position

V74 represents both Boolean output fibers by exact disjoint affine-cell decompositions. Its weighted branch dynamic program computes exact target and prefix preimage counts. For `m>n`, repeated prefix counting constructs an avoided output on a supplied boundary-width-`b` gate decomposition in

```text
O(m^2 A(b)^2 poly(n,m)).
```

V75 compiles the weighted recurrence once into a monotone arithmetic DAG for the paired generating polynomial

```text
P_C(u,v) = sum_x product_i z_{i,C_i(x)}.
```

The DAG has

```text
S = O(m A(b)^2)
```

arithmetic operations. Incremental prefix search takes

```text
O(A(b)^2 (m + sum_i depth_T(i)) poly(n,m)).
```

A supplied logarithmic-height tree therefore yields `O(m log m A(b)^2 poly(n,m))`. A caterpillar has quadratic external path length, so V75 does not prove an unconditional improvement for arbitrary supplied decompositions.

The next structural target is a rigorous width/depth balancing theorem or tradeoff for the support-boundary connectivity function. The 2026 FPT algorithm of Korhonen and Oum addresses parameterized branch-decomposition discovery, but not the depth guarantee needed by V75.

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
| V74 | Exact two fibers, weighted preimage counts, prefix avoidance, and OR-path `3m-3` | Merged; final Copilot remediation completed |
| V75 | Symbolic generating circuit and depth-sensitive incremental avoidance | Candidate; final CI and Copilot gates required |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> draft PR -> quick/full/LaTeX CI -> final-diff Copilot review -> squash merge to main`. Any new commit restarts both gates. V22 and V26 remain justified skips. The direct P-versus-NP route remains inactive.
