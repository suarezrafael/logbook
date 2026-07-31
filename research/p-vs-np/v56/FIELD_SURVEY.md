# V56 field survey and prior-art status

## Closest Range-Avoidance literature

Gajulapalli, Golovnev, Nagargoje, and Saraogi identify minimum-stretch `NC0_3-Avoid` as open and show that an efficient `P^NP` algorithm already at output length `n+n^(2/3)` would imply explicit rigid matrices and super-linear lower bounds for log-depth circuits.

Kuntewar and Sarma give polynomial-time algorithms for monotone `NC0_3-Avoid` at positive stretch using Turán-type hypergraph structure. Their result does not directly cover arbitrary mixtures of the nonmonotone affine-fiber classes `0x06`, `0x18`, and `0x69`.

Guruswami, Lyu, and Wang solve `NC0_2-Avoid` and use linear/algebraic structure in positive results. Affine output functions themselves are naturally handled by linear dependence. V56 differs because the output truth table need not be affine: only one selected output fiber must be affine.

## Constraint-language context

Schaefer's dichotomy established affine, bijunctive, Horn, and dual-Horn Boolean relation classes as central tractable constraint languages. V56 uses the affine branch as a certificate-producing Range-Avoidance mechanism rather than merely as a satisfiability algorithm.

The phrase `block-subspace redundancy` is internal. Equivalent formulations may exist in affine CSP, linear matroids, coding theory, subspace arrangements, functional dependencies, or linear secret-sharing language.

## Targeted novelty search

Searches were performed for combinations of:

```text
affine fiber range avoidance
block subspace redundancy
selected output fiber affine circuit
consistency or redundancy affine constraints
NC0_3 antipodal pair avoid
```

No exact match for the theorem or the mixed-class stretch-one application was located in the examined sources. This is not a novelty determination. The result remains an internally verified proof candidate pending specialist review.

## Remaining frontier

The six remaining essential classes divide naturally by Schaefer-style polymorphisms:

- bijunctive on both fibers: `0x07`, `0x17`, `0x1b`;
- not bijunctive on both fibers: `0x16`, `0x19`, `0x1e`.

## Primary references

1. K. Gajulapalli, A. Golovnev, S. Nagargoje, S. Saraogi, *Range Avoidance for Constant-Depth Circuits: Hardness and Algorithms*, ECCC TR23-021 / APPROX-RANDOM 2023.
2. N. Kuntewar, J. Sarma, *Avoiding Range via Turan-Type Bounds*, APPROX-RANDOM 2025 / ECCC TR25-034.
3. V. Guruswami, X. Lyu, X. Wang, *Range Avoidance for Low-Depth Circuits and Connections to Pseudorandomness*, RANDOM 2022 / ECCC TR22-102.
4. T. J. Schaefer, *The Complexity of Satisfiability Problems*, STOC 1978.
