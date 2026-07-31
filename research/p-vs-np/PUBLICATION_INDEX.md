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

## Consolidated article

The existing integrated manuscript is `v62/INTEGRATED_MANUSCRIPT.md`. It predates V68–V70 and is not yet the current submission document. V71 is reserved for an English LaTeX consolidation with one theorem-status table, one bibliography, and explicit separation among theorems, finite experiments, retractions, and open questions.

## Reproducibility

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

GitHub Actions publishes quick/full transcripts and compiled formal-module PDFs. Historical missing artifacts and retractions remain visible in `STATE.md` and `LEDGER.json`.

## Publication status

- No ECCC or arXiv submission has been made from this index.
- No Zenodo DOI has been minted for the consolidated project.
- No theorem is marked peer reviewed or novelty confirmed.
- The direct P-versus-NP route is inactive.

The intended sequence is consolidated manuscript review, stable release metadata, Zenodo archival, ECCC technical-report submission, and optional arXiv cross-post.
