# V111 literature boundary

## Range avoidance

Primary-source calibration used in this laboratory includes:

- Kuntewar and Sarma, *Range Avoidance in Boolean Circuits via Turan-type Bounds* (ECCC TR25-034 / arXiv:2503.17114).  Their exact-stretch polynomial result is for monotone `NC0_3`; the general low-stretch `NC0_3` frontier remains difficult.
- Huang, Li, and Zhong, *Range Avoidance and Remote Point: New Algorithms and Hardness* (ECCC TR25-049, revision 5).  They give improved general `NC0_k-Avoid[n,n+1]` algorithms but still exponential local running time in the worst case.

The targeted search did not locate an explicit published theorem phrased as essential signed MUX/bijunctive exact-stretch avoidance via target-compatible shared return flows.  Search absence is not evidence of novelty.

## Shared-path optimization

The path-optimization part of V111 is not claimed as novel.

- Fluschnik, Kratsch, Niedermeier, and Sorge study the *Minimum Shared Edges* problem (FSTTCS 2015; arXiv:1602.01739).  Their formulation is different and can be NP-hard; it is useful as a warning that general shared-path problems should not be conflated with the special two-unit common-sink flow used here.
- Standard integral min-cost-flow methods compute fixed-amount flows with additive costs.  V111's network encodes a convex two-level use cost for each output gate by two parallel unit-capacity gate edges of costs zero and one.

Accordingly, V111 attributes no novelty to min-cost flow or to the generic concept of shared-edge minimization.  The laboratory-specific claim is the composition rule tying a shared MUX output to one globally consistent target bit and lifting two opposite-phase implication cycles to a missing circuit output.

## Novelty discipline

No novelty or priority claim is made.  Before external dissemination, the exact shared-target composition theorem and its relation to bijunctive CSP / implication-graph literature should receive expert review.
