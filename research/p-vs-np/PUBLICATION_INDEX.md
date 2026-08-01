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
| `v71/V71_WIDTH_CORRESPONDENCE_THEOREM.tex` | exact linear branch-width vocabulary, pathwidth sandwich, and decomposition algorithms | candidate; local verification passed, PR CI required |

## Consolidated article

The current integrated manuscript is `v71/MANUSCRIPT.tex`. It consolidates V54–V71 in English and uses `v71/THEOREM_STATUS.md` to separate proved theorems, finite experiments, retractions, open conjectures, and prior-art anchors.

The older `v62/INTEGRATED_MANUSCRIPT.md` remains historical.

## Reproducibility

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

GitHub Actions is configured to publish quick/full transcripts and compile both V71 PDFs. Historical missing artifacts and retractions remain visible in `STATE.md` and `LEDGER.json`.

## Release candidate files

- `v71/MANUSCRIPT.tex` — consolidated source;
- `v71/V71_WIDTH_CORRESPONDENCE_THEOREM.tex` — standalone proof module;
- `v71/REFERENCES.bib` — reviewed bibliographic metadata seed;
- `v71/ECCC_METADATA.yaml` — draft, explicitly not submitted;
- `v71/RELEASE_PLAN.md` — authorship, license, review, tag, DOI, and submission gates.

## Publication status

- No ECCC or arXiv submission has been made from this index.
- No Zenodo DOI has been minted for the consolidated project.
- No theorem is marked peer reviewed or novelty confirmed.
- The direct P-versus-NP route is inactive.
- V71 must pass quick, full, and LaTeX pull-request CI before promotion.

The intended sequence is external proof review, authorship and license confirmation, stable tagged release, optional Zenodo archival, ECCC technical-report submission, and optional arXiv cross-post.
