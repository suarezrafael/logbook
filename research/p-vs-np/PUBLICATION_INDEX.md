# Academic entry point and publication index

This page is the discovery-oriented entry point for the `NC0_k-Avoid Laboratory`. The repository is an audit trail; readers should not be expected to follow every laboratory chronologically.

## Current mathematical modules

| Module | Result | Status |
|---|---|---|
| `v64/V57_BLOCK_IRREDUNDANCY_THEOREM.tex` | five-block orbit-`0x07` irredundancy obstruction | internally verified; novelty unconfirmed |
| `v65/V56_AFFINE_FIBER_THEOREM.tex` | affine consistency-or-redundancy algorithm | internally verified; novelty unconfirmed |
| `v68/V68_SPINE_TREE_DAG_THEOREM.tex` | exponential complete-tree lower bound and linear projected DAG for the spine family | internally verified; novelty unconfirmed |
| `v69/V69_ORDER_ROBUSTNESS_THEOREM.tex` | exact optimization of projected DAG size over gate orders | internally verified; novelty unconfirmed |
| `v70/V70_SUPPORT_FRONTIER_THEOREM.tex` | support-frontier and component-factorisation upper bounds | internally verified; novelty unconfirmed |
| `v71/V71_WIDTH_CORRESPONDENCE_THEOREM.tex` | linear branch-width vocabulary, pathwidth sandwich, and decomposition algorithms | merged after quick/full/LaTeX CI; novelty unconfirmed |
| `v72/V72_BRANCH_RESIDUAL_THEOREM.tex` | three-uniform width NP-completeness, exact subset DP, branch affine residual composition, and bounded-treewidth separation | merged after quick/full/LaTeX CI; novelty unconfirmed |
| `v73/V73_BICRITERIA_AVOIDANCE_THEOREM.tex` | exact budgeted residual ordering, branch multiplicities, supplied-target certificate, normalized-schema barrier, and binary-tree compression | candidate; PR CI required, novelty unconfirmed |

## Consolidated article

The current integrated manuscript is `v71/MANUSCRIPT.tex`. It consolidates V54–V71 in English and uses `v71/THEOREM_STATUS.md` to separate proved theorems, finite experiments, retractions, open conjectures, and prior-art anchors.

V72 and V73 are standalone extensions pending external proof review before a future consolidated release. The older `v62/INTEGRATED_MANUSCRIPT.md` remains historical.

## V72 package

- `v72/COMPLEXITY_AND_BRANCH_DP.md` — definitions and proofs;
- `v72/PATHWIDTH_BENCHMARK.md` — frozen V69–V70 comparison table;
- `v72/PRIOR_ART.md` — scoped graph-layout literature audit;
- `v72/V72_BRANCH_RESIDUAL_THEOREM.tex` — formal theorem module;
- `v72/v72_branch_residual.py` — exact subset and branch residual algorithms;
- `v72/verify.py` and `v72/verify_independent.py` — primary and semantic checks.

## V73 package

- `v73/BICRITERIA_AND_MULTIPLICITY.md` — exact recurrences and proofs;
- `v73/BICRITERIA_BENCHMARK.md` — six exact Pareto comparisons;
- `v73/V73_BICRITERIA_AVOIDANCE_THEOREM.tex` — formal theorem module;
- `v73/bicriteria.py` — budgeted subset optimization;
- `v73/multiplicity.py` — multiplicity-enhanced branch residual DP;
- `v73/tree_compression.py` — private-vertex tree compression checks;
- `v73/verify.py` and `v73/verify_independent.py` — primary and independent semantic checks;
- `v73/V74_CORE_CONTEXT.md` — frozen next-step constraints.

## Reproducibility

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

GitHub Actions publishes quick/full transcripts and compiled formal-module PDFs. Historical missing artifacts and retractions remain visible in `STATE.md` and `LEDGER.json`.

## Release metadata

The V71 release-candidate files remain:

- `v71/MANUSCRIPT.tex`;
- `v71/REFERENCES.bib`;
- `v71/ECCC_METADATA.yaml`, explicitly `draft_not_submitted`;
- `v71/RELEASE_PLAN.md`.

V72 and V73 do not change publication status.

## Publication status

- No ECCC or arXiv submission has been made from this index.
- No Zenodo DOI has been minted for the consolidated project.
- No theorem is marked peer reviewed or novelty confirmed.
- The direct P-versus-NP route is inactive.
- V73 must pass quick, full, and LaTeX pull-request CI before promotion.

The intended sequence remains external proof review, authorship and license confirmation, stable tagged release, optional Zenodo archival, ECCC technical-report submission, and optional arXiv cross-post.
