# V112 literature boundary

## Range avoidance

Current primary-source calibration:

- Kuntewar and Sarma, ECCC TR25-034, *Range Avoidance in Boolean Circuits via Turan-type Bounds* (2025).  The published exact-stretch polynomial result is for monotone `NC0_3`; their abstract also records the much weaker general `NC0_3` stretch regime known at that point.
- Huang, Li, and Zhong, ECCC TR25-049 revision 5, *Range Avoidance and Remote Point: New Algorithms and Hardness* (2025).  This gives improved general range-avoidance algorithms and hardness connections, but the low-stretch local-circuit problem remains nontrivial.

The targeted search through August 2026 did not locate an explicit theorem matching the V112 statement: exact signed-MUX serial support recognition plus local target-phase transfer yielding a missing word.  Search absence is not novelty evidence.

## Path-selection caution

V112 deliberately restricts to a serial two-lobe template because compatibility selection is not generically benign.

- Kováč, arXiv:1111.3996, studies Path Avoiding Forbidden Pairs and gives NP-hard restricted cases together with polynomial structured cases.
- German, arXiv:2605.12457, gives further 2026 width-sensitive hardness/FPT boundaries for PAFP, including NP-completeness in narrow DAG regimes and a 2-SAT tractable exact-length-width-two case.
- Fluschnik, Kratsch, Niedermeier, and Sorge, arXiv:1602.01739, study Minimum Shared Edges and show that generic shared-path optimization has its own nontrivial parameterized complexity.

None of these results is imported as a hardness theorem for MUX target compatibility.  They are used only as a warning against assuming that compatibility over arbitrary alternative flows must be polynomial.

## Novelty discipline

V112 claims no novelty or priority.  External review should focus on:

1. whether the serial support template or an equivalent bijunctive-CSP decomposition is already standard;
2. correctness and completeness of the local phase-transfer factorization for the stated lobe-disjoint certificate class;
3. whether the mixed optimum-face example is already implicit in labeled-path or implication-graph literature.
