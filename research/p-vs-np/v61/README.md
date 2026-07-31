# NC0_k-Avoid Laboratory V61

## Reproducibility repair and prior-art boundary

**Scientific status:** internal audit package. It introduces no new Range-Avoidance theorem. It corrects one historical reproducibility claim, refocuses the manuscript and records a primary-source prior-art audit.

## Main outcomes

1. **V22 correction.** The V22 verifier requires `full_certificate_cases.json`, which is absent. Aggregate `RESULTS.json` counts cannot reconstruct the original 125 cases. V22 is now a proof candidate without repository-executable finite evidence.
2. **Runner repair.** `verify_all.sh` reports V22 as `SKIP` with the missing-artifact reason.
3. **Manuscript refocus.** The main article is built around V56 versus V57: affine tractability versus failure of the natural bijunctive extension.
4. **Supplement cut.** V25's four-input classification is moved out of the main narrative.
5. **Prior-art boundary.** General CNF/2-CNF irredundancy and randomized Avoid sampling are known background. A 2025 paper directly covers monotone `NC0_3-Avoid` at `m>n`.
6. **Novelty remains open.** The exact V56 formulation, orbit-constrained V57 construction and orientation-depth formalism require specialist review.

## Reproduce

```bash
python verify.py
python verify_independent.py
```

From the parent directory:

```bash
bash ./verify_all.sh
```

The V22 row must be `SKIP`, not `FAIL`.
