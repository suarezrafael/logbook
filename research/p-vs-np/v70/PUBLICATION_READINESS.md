# Publication and discovery readiness

A public GitHub repository is useful for auditability and reproducibility, but it is not the academic discovery layer for this project.

## Intended publication stack

1. **Consolidated mathematical manuscript.** The article, not the laboratory sequence, should be the primary reading path. V62 must be updated through V70 and converted to standalone English LaTeX before submission.
2. **ECCC technical report.** The report should cite the repository as its reproducibility artifact and be submitted only after mathematical and metadata review.
3. **Zenodo software snapshot.** After metadata review, enable the repository in Zenodo and archive a stable GitHub release to receive a DOI. Repository-wide citation metadata is deferred until the title, author list, abstract, license, and release scope are frozen.
4. **arXiv cross-post.** Consider `cs.CC` only after the manuscript and authorship metadata are reviewed and any account endorsement requirement is resolved.

## V70 action

V70 adds a discoverability index and freezes the publication package requirements, but it does not submit or claim acceptance, peer review, novelty, or priority. External publication is irreversible enough that the consolidated manuscript should receive human mathematical review first.

## Release checklist

- English title and abstract;
- author name and ORCID decision;
- explicit license for manuscript and code;
- current theorem-status table and retraction note;
- compiled PDF with bibliography;
- source archive and verifier instructions;
- root-level citation metadata reviewed for the whole repository;
- stable GitHub release tag;
- Zenodo DOI added back to the manuscript and repository;
- ECCC submission metadata and keywords;
- no P-versus-NP claim beyond the documented interface.
