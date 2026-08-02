# Laboratory V79 — immutable evidence migration

V79 converts the mutation inventory exposed by V78 into read-only, deterministic verification contracts.

## Completed migrations: V54–V59

- V54 recomputes certificate diagnostics in memory and no longer creates `VERIFY_RESULTS.json`.
- V55 recomputes classification and validation counts, compares them with committed `RESULTS.json`, removes wall-clock measurements, and no longer creates `CLASSIFICATION.json` or rewrites its snapshot.
- V56 primary and independent verifiers compare stable recomputed invariants with committed `RESULTS.json` and no longer create repository-validation snapshots.
- V57 recomputes the exhaustive n=3/n=4 censuses, boundary theorem, explicit gadget, and direct-product family without rewriting results or creating `CERTIFICATES.json`.
- V58 preserves the committed exact-search and independent-audit metadata while recomputing its fiber, orientation-depth, direct-sum, random-circuit, boundary, and universal-bound evidence read-only.
- V59 recomputes Harper constants, random sampling bounds, and direct-sum potential barriers without timing or snapshot rewrites.
- The sandbox mutation list is checked against a versioned baseline. Any new, deleted, or unexpectedly restored mutation fails CI.

These migrations reduce the V78 inventory from 21 paths to nine modified snapshots. No newly generated path remains in the baseline.

## Remaining waves

1. V65–V67: separate theorem validation from generated witnesses and benchmark output.
2. V68–V72: reconcile stale snapshots and convert deterministic searches into committed-evidence comparisons.
3. Reduce `EXPECTED_MUTATIONS.tsv` to an empty file.
4. Reconcile `STATE.md`, `LEDGER.json`, and publication indexes through the promoted laboratory.

## Scientific scope

V79 changes reproducibility infrastructure only. It proves no new avoidance theorem, circuit lower bound, or P-versus-NP result.
