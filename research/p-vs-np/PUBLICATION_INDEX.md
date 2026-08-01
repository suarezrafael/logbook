# Academic entry point and publication index

This page is the discovery-oriented entry point for the `NC0_k-Avoid Laboratory`. The repository is an audit trail; readers should not be expected to follow every laboratory chronologically.

## Current mathematical modules

| Module | Result | Status |
|---|---|---|
| `v64/V57_BLOCK_IRREDUNDANCY_THEOREM.tex` | five-block orbit-`0x07` irredundancy obstruction | internally verified; novelty unconfirmed |
| `v65/V56_AFFINE_FIBER_THEOREM.tex` | affine consistency-or-redundancy algorithm | internally verified; novelty unconfirmed |
| `v68/V68_SPINE_TREE_DAG_THEOREM.tex` | exponential complete-tree lower bound and linear projected DAG | internally verified; novelty unconfirmed |
| `v69/V69_ORDER_ROBUSTNESS_THEOREM.tex` | exact projected-DAG optimization over gate orders | internally verified; novelty unconfirmed |
| `v70/V70_SUPPORT_FRONTIER_THEOREM.tex` | support-frontier and component-factorisation upper bounds | internally verified; novelty unconfirmed |
| `v71/V71_WIDTH_CORRESPONDENCE_THEOREM.tex` | linear branch-width vocabulary and pathwidth sandwich | merged after quick/full/LaTeX CI; novelty unconfirmed |
| `v72/V72_BRANCH_RESIDUAL_THEOREM.tex` | rank-three width NP-completeness and branch residual composition | merged after quick/full/LaTeX CI; novelty unconfirmed |
| `v73/V73_BICRITERIA_AVOIDANCE_THEOREM.tex` | budgeted ordering, branch multiplicities, and binary-tree compression | merged after quick/full/LaTeX CI; novelty unconfirmed |
| `v74/V74_TWO_FIBER_AVOIDANCE_THEOREM.tex` | exact two gate fibers, weighted preimage counting, bounded-width prefix avoidance, and OR-path `3m-3` | merged after quick/full/LaTeX CI; novelty unconfirmed |
| `v75/V75_SYMBOLIC_PREFIX_THEOREM.tex` | paired generating polynomial, monotone residual circuit, and depth-sensitive incremental avoidance | merged after quick/full/LaTeX CI and final Copilot review; novelty unconfirmed |
| `v76/V76_TOP_TREE_TRANSFER_THEOREM.tex` | labelled top-tree transfer from supplied width `b` to width at most `4b` and logarithmic height | merged after quick/full/LaTeX CI and final Copilot review; correct but dominated by V77 |
| `v77/V77_TOPOLOGY_TREE_TRANSFER_THEOREM.tex` | restricted topology-tree transfer from supplied width `b` to width at most `2b` and logarithmic height | candidate; internal proof and finite audit, PR gates required, novelty unconfirmed |

## Consolidated article

The current integrated manuscript is `v71/MANUSCRIPT.tex`. It consolidates V54–V71 in English and uses `v71/THEOREM_STATUS.md` to separate proved theorems, finite experiments, retractions, open conjectures, and prior-art anchors.

V72–V77 are standalone extensions pending external proof review before a future consolidated release. The older `v62/INTEGRATED_MANUSCRIPT.md` remains historical.

## V75 package

- `v75/SYMBOLIC_PREFIX_CIRCUIT.md` — theorem, proof invariant, complexity, and literature boundary;
- `v75/EXHAUSTIVE_RESULTS.md` — finite validation ledger;
- `v75/V75_SYMBOLIC_PREFIX_THEOREM.tex` — formal theorem module;
- `v75/symbolic_prefix_circuit.py` — monotone arithmetic DAG and incremental evaluator;
- `v75/v75_symbolic_prefix.py` — deterministic exhaustive and seeded generator;
- `v75/verify.py` and `v75/verify_independent.py` — primary and independent audits;
- `v75/RESULTS.json` — deterministic snapshot;
- `v75/V76_CORE_CONTEXT.md` — frozen V76 starting constraints.

## V76 package

- `v76/TOP_TREE_TRANSFER.md` — four-cut lemma, transfer proof, prior-art boundary, and rejected centroid route;
- `v76/V76_TOP_TREE_TRANSFER_THEOREM.tex` — formal theorem module;
- `v76/decomposition_pareto.py` — exact width/height/external-path Pareto dynamic programs;
- `v76/cluster_cut_cover.py` — labelled-cluster four-cut certificate auditor;
- `v76/v76_top_tree_transfer.py` — deterministic classification and regression generator;
- `v76/verify.py` and `v76/verify_independent.py` — primary and independent audits;
- `v76/EXHAUSTIVE_RESULTS.md` and `v76/RESULTS.json` — finite ledger and deterministic snapshot;
- `v76/V77_CORE_CONTEXT.md` — frozen factor-tightening target.

## V77 package

- `v77/TOPOLOGY_TREE_TRANSFER.md` — retained two-edge lemma, transfer proof, prior-art boundary, and tightness scope;
- `v77/V77_TOPOLOGY_TREE_TRANSFER_THEOREM.tex` — formal theorem module;
- `v77/topology_tree_certificate.py` — deterministic static hierarchy, certificate verifier, label pruning, and transfer auditor;
- `v77/v77_topology_tree_transfer.py` — deterministic source-shape, support-orbit, and regression generator;
- `v77/STATIC_TOPOLOGY_CERTIFICATE.json` — independently checkable representative topology hierarchy;
- `v77/verify.py` and `v77/verify_independent.py` — primary and independently written audits;
- `v77/EXHAUSTIVE_RESULTS.md` and `v77/RESULTS.json` — finite ledger and deterministic snapshot;
- `v77/V78_CORE_CONTEXT.md` — frozen factor-two-versus-width-preservation target.

The logarithmic-height restricted topology hierarchy is attributed to Frederickson's prior work and its relation to top trees. The V77-specific claim is that pruning to gate labels on degree-one leaves eliminates every external-degree-three cluster, leaving a two-edge support-boundary cover and the V75 consequence `A(2b)^2`. Novelty is not confirmed.

## Reproducibility

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

GitHub Actions publishes quick/full transcripts and compiled formal-module PDFs. Historical missing artifacts and retractions remain visible in `STATE.md` and `LEDGER.json`.

## Release metadata

The V71 release-candidate files remain `v71/MANUSCRIPT.tex`, `v71/REFERENCES.bib`, `v71/ECCC_METADATA.yaml`, and `v71/RELEASE_PLAN.md`. V72–V77 do not change publication status.

## Publication status

- No ECCC or arXiv submission has been made from this index.
- No Zenodo DOI has been minted for the consolidated project.
- No theorem is marked peer reviewed or novelty confirmed.
- The direct P-versus-NP route is inactive.
- V77 must pass quick, full, and LaTeX pull-request CI and final-diff Copilot review before promotion.

The intended sequence remains external proof review, authorship and license confirmation, stable tagged release, optional Zenodo archival, ECCC technical-report submission, and optional arXiv cross-post.
