# Laboratory V79 — immutable evidence migration

V79 converts the mutation inventory exposed by V78 into read-only, deterministic verification contracts.

## First wave: V54–V56

- V54 recomputes its certificate diagnostics in memory and no longer creates `VERIFY_RESULTS.json`.
- V55 recomputes the classification and validation counts, compares them with committed `RESULTS.json`, removes wall-clock measurements, and no longer creates `CLASSIFICATION.json`.
- V56 primary and independent verifiers compare recomputed invariants with committed `RESULTS.json` and no longer create repository-validation snapshots.
- The sandbox mutation list is checked against a versioned baseline. Any new, deleted, or unexpectedly restored mutation fails CI.

The first wave reduces the V78 inventory from 21 paths to 15 modified paths and zero newly generated files.

## Remaining waves

1. V57–V59: remove expanded snapshot and timing rewrites while preserving exact finite evidence.
2. V65–V67: separate theorem validation from generated witnesses and benchmark output.
3. V68–V72: reconcile stale snapshots and convert deterministic searches into committed-evidence comparisons.
4. Reduce `EXPECTED_MUTATIONS.tsv` to an empty file.
5. Reconcile `STATE.md`, `LEDGER.json`, and publication indexes through the promoted laboratory.

## Scientific scope

V79 changes reproducibility infrastructure only. It proves no new avoidance theorem, circuit lower bound, or P-versus-NP result.
