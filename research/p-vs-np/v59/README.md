# P versus NP Laboratory V59

## Boundary abundance versus deterministic localization

**Scientific status:** internally proved, adversarially audited and independently verified. Not peer reviewed. Novelty is not established. This package does not solve deterministic `0x07-Avoid`, general `NC0_3-Avoid`, unrestricted circuit lower bounds, or P versus NP.

## Main results

1. Harper's vertex-isoperimetric theorem implies that every image `S` of size at most half the output cube has

```text
|internal boundary| / |S| >= binom(m,floor(m/2))/2^(m-1)
                         = Theta(1/sqrt(m)).
```

2. If `alpha=|Range(C)|/2^n`, a uniform input hits the boundary with probability at least `kappa_m alpha`. For bijunctive fibers, the missing neighbor is found with polynomially many 2-SAT tests.

3. The V57 direct-sum family refutes three strict-improvement potentials: exact forced variables, unit propagation and exact fiber size are flat between the unique interior point and all of its boundary neighbors.

4. The old exact search remains incomplete at `n=9`. A SAT Modulo Symmetries encoding blueprint is included.

## Reproduce

```bash
python verify.py
python verify_independent.py
python boundary_sampling_experiment.py
python harper_profile.py
```

The partial exact search can be rebuilt with:

```bash
g++ -O3 -std=c++17 -fopenmp exact_single_flip_search_select.cpp -o exact_search
./exact_search 9 9 100000 8 1
./exact_search 9 9 100000 8 3
```

These exact runs are incomplete and must not be interpreted as proofs.

## Rich output files

- `SCIENTIFIC_STATUS.md`;
- `THEOREM.md` and `PROOF.md`;
- `ISOPERIMETRIC_LOCALIZATION.md`;
- `WALKING_BARRIER.md`;
- `SMS_N9_BLUEPRINT.md` and `N9_SEARCH_STATUS.md`;
- `LAY_SUMMARY.md`;
- `PROMOTION_INDEX.md` and `PROGRESS_INDEX.md`;
- `DISTANCIA_ATE_P_VS_NP.md`;
- `FIELD_SURVEY.md`;
- `V60_CORE_CONTEXT.md`;
- primary and independent verifiers;
- machine-readable results, validation logs and hashes.
