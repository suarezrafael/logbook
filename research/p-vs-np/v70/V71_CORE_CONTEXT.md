# Frozen context for Laboratory V71

## Stable facts

1. V69 defines `G*_proj` and computes it exactly by subset-lattice dynamic programming.
2. V70 proves `w(S)<=min(2^|S|,A(|F(S)|))` and `G_proj(pi)<=m A(q(pi))`.
3. V70 proves exact factorisation across connected components of the processed support-incidence graph.
4. Support-only polynomial heuristics reduce the preserved `n=14` fixed-order record from `583` to `41`.
5. Finite exact-objective records are `G*_proj=29` at `n=8` and `30` at `n=10`; no asymptotic conclusion follows.
6. No general polynomial good-order theorem, all-orders lower bound, or standard proof-system simulation is proved.
7. The direct P-versus-NP route remains inactive.

## Required V71 behavior

1. Consolidate V54–V70 into one English LaTeX manuscript with a single theorem-status table.
2. Separate proved theorems, finite experiments, retractions, open conjectures, and prior art.
3. State the support-frontier theorem using a standard graph or hypergraph width vocabulary only after verifying the exact correspondence.
4. Test whether tree or path decompositions yield constructible orders and sharper dynamic programs.
5. Add reviewed citation metadata and a stable-release plan; do not create a public DOI before metadata and license review.
6. Prepare an ECCC-ready PDF and submission metadata, but do not claim acceptance or peer review.
7. Preserve V70 records and independent verification.
8. Merge only after quick, full, and LaTeX CI pass.
