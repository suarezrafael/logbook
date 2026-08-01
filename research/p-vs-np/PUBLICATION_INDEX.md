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
| `v74/V74_TWO_FIBER_AVOIDANCE_THEOREM.tex` | exact two gate fibers, weighted preimage counting, bounded-width prefix avoidance, and OR-path `3m-3` | candidate; PR CI required, novelty unconfirmed |

## Consolidated article

The current integrated manuscript is `v71/MANUSCRIPT.tex`. It consolidates V54–V71 in English and uses `v71/THEOREM_STATUS.md` to separate proved theorems, finite experiments, retractions, open conjectures, and prior-art anchors.

V72–V74 are standalone extensions pending external proof review before a future consolidated release. The older `v62/INTEGRATED_MANUSCRIPT.md` remains historical.

## V74 package

- `v74/TWO_FIBER_AVOIDANCE.md` — definitions and proofs;
- `v74/EXHAUSTIVE_RESULTS.md` — finite validation ledger;
- `v74/V74_TWO_FIBER_AVOIDANCE_THEOREM.tex` — formal theorem module;
- `v74/two_fiber_model.py` — exact fibers, weighted counts, and target search;
- `v74/or_path_family.py` — exact treewidth-one residual family;
- `v74/v74_two_fiber_avoidance.py` — deterministic result generator;
- `v74/verify.py` and `v74/verify_independent.py` — primary and independent audits;
- `v74/RESULTS.json` — deterministic snapshot;
- `v74/V75_CORE_CONTEXT.md` — frozen next-step constraints.

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

V72–V74 do not change publication status.

## Publication status

- No ECCC or arXiv submission has been made from this index.
- No Zenodo DOI has been minted for the consolidated project.
- No theorem is marked peer reviewed or novelty confirmed.
- The direct P-versus-NP route is inactive.
- V74 must pass quick, full, and LaTeX pull-request CI before promotion.

The intended sequence remains external proof review, authorship and license confirmation, stable tagged release, optional Zenodo archival, ECCC technical-report submission, and optional arXiv cross-post.
