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
- [`v72/`](v72/) — rank-three width complexity, exact subset DP, branch residual composition, and path-order benchmarks.
- [`verify_all.sh`](verify_all.sh) — cumulative quick/full verifier.

## Current position

V69 defines and exactly audits

```text
G*_proj = min_pi G_proj(pi).
```

V70 proves the support-frontier upper bound

```text
w(S) <= min(2^|S|, A(|F(S)|)),
G_proj(pi) <= m A(q(pi)).
```

V71 identifies the optimum frontier width `q*` with vertex-boundary linear branch-width. For rank-`r` supports and primal graph `P(H)`:

```text
q* <= pw(P(H)) + 1,
pw(P(H)) <= q* + r - 1.
```

V72 proves that deciding `q*<=k` is NP-complete even on simple three-uniform hypergraphs, via private-vertex padding that preserves every graph edge-cut boundary. It also implements

```text
D[S] = min_{e in S} max(D[S-{e}], lambda(S))
```

in `O(m 2^m poly(n))` time and gives a branch-decomposition affine residual DP with at most `A(b)` states per boundary-`b` node and at most `A(b)^2` child pairs per join.

Private-vertex padding of perfect binary trees gives primal treewidth at most two but unbounded linear support width. This separates tree-shaped feasibility from linear ordering; it does not prove a growing or superpolynomial `G*_proj` lower bound.

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
| V72 | Three-uniform NP-completeness, exact width DP, branch residual DP, and width-vs-residual benchmarks | Current laboratory; promotion gated by quick/full/LaTeX CI |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> PR -> quick/full/LaTeX CI -> squash merge to main`. V22 and V26 remain justified skips. The direct P-versus-NP route remains inactive.
