# Laboratory V79 — immutable evidence migration

V79 converts the mutation inventory exposed by V78 into read-only, deterministic verification contracts.

## Completed migrations: V54–V57

- V54 recomputes certificate diagnostics in memory and no longer creates `VERIFY_RESULTS.json`.
- V55 recomputes classification and validation counts, compares them with committed `RESULTS.json`, removes wall-clock measurements, and no longer creates `CLASSIFICATION.json` or rewrites its snapshot.
- V56 primary and independent verifiers compare stable recomputed invariants with committed `RESULTS.json` and no longer create repository-validation snapshots.
- V57 primary and independent verifiers recompute the exhaustive n=3/n=4 censuses, boundary theorem, explicit gadget, and direct-product family; they compare committed evidence without rewriting either results file or creating `CERTIFICATES.json`.
- The sandbox mutation list is checked against a versioned baseline. Any new, deleted, or unexpectedly restored mutation fails CI.

These migrations reduce the V78 inventory from 21 paths to 13 modified snapshots. No newly generated path remains in the baseline.

## Remaining waves

1. V58–V59: remove snapshot and timing rewrites while preserving exact-search and probabilistic audit metadata.
2. V65–V67: separate theorem validation from generated witnesses and benchmark output.
3. V68–V72: reconcile stale snapshots and convert deterministic searches into committed-evidence comparisons.
4. Reduce `EXPECTED_MUTATIONS.tsv` to an empty file.
5. Reconcile `STATE.md`, `LEDGER.json`, and publication indexes through the promoted laboratory.

## Scientific scope

V79 changes reproducibility infrastructure only. It proves no new avoidance theorem, circuit lower bound, or P-versus-NP result.
