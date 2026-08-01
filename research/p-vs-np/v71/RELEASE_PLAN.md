# Stable-release and submission plan

## Current status

V71 prepares, but does not execute, an ECCC/arXiv/Zenodo release. No DOI or submission identifier is claimed.

## Gates before archival

1. Confirm repository and manuscript authorship order.
2. Select and add an explicit repository license; no license is inferred from public visibility.
3. Review every bibliography record against the publisher or report landing page.
4. Obtain at least one external proof read focused on the V70–V71 width arguments.
5. Run quick, full, and LaTeX CI on the V71 pull request.
6. Freeze a tagged release and SHA-256 manifest.
7. Only then mint a Zenodo DOI, if desired.
8. Submit the frozen PDF and metadata to ECCC; optionally cross-post to arXiv after category review.

## Metadata review checklist

- title and abstract do not claim P-versus-NP progress beyond the stated structural interface;
- theorem-status table separates proofs, experiments, retractions, and conjectures;
- all author names, affiliations, ORCIDs, and contact addresses are confirmed by the authors;
- funding and conflict statements are explicit;
- source archive compiles without repository-private dependencies;
- license is compatible with the selected archive;
- version number and commit hash appear in the PDF.

## Prohibited status language before external events

Do not write “accepted”, “peer reviewed”, “published by ECCC”, “novel”, or “DOI” unless the corresponding external record exists and has been checked.
