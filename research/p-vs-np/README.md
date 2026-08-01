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
- [`v76/`](v76/) — logarithmic-depth top-tree transfer with width at most `4b`.
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

The DAG has `S = O(m A(b)^2)` arithmetic operations, and incremental prefix search takes

```text
O(A(b)^2 (m + sum_i depth_T(i)) poly(n,m)).
```

V76 removes the arbitrary-depth obstruction in the **supplied-decomposition parameterized regime**. Standard labelled top trees provide a logarithmic-height hierarchy. The V76 four-cut lemma transfers every retained cluster to the union of at most four original middle sets. Therefore a supplied width-`b` subcubic gate decomposition yields a rooted gate tree with

```text
width <= 4b,
height = O(log m),
external path length = O(m log m).
```

Rebuilding the V75 circuit on the transferred tree gives

```text
O(m log m A(4b)^2 poly(n,m)).
```

The top-tree height construction is prior art; the four-cut support-boundary corollary is internally proved and novelty remains unconfirmed. V76 does not show that factor four is optimal or that width-preserving logarithmic balancing is impossible.

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
| V74 | Exact two fibers, weighted preimage counts, prefix avoidance, and OR-path `3m-3` | Merged; memoization maintenance also promoted |
| V75 | Symbolic generating circuit and depth-sensitive incremental avoidance | Merged after quick/full/LaTeX CI and final Copilot review |
| V76 | Top-tree `4b` width/depth transfer and exact Pareto tradeoff audit | Candidate; PR gates required |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> draft PR -> quick/full/LaTeX CI -> final-diff Copilot review -> squash merge to main`. Any new commit restarts both gates. V22 and V26 remain justified skips. The direct P-versus-NP route remains inactive.
