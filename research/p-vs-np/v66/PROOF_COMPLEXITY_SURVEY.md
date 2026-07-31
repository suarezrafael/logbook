# Proof-complexity adjacency audit

Affine-cell branching is structurally similar to DPLL-style case analysis, but V66 does not identify its trees with an established proof system. The following neighboring areas constrain future claims.

## Relevant primary sources

- Huang, Li and Zhong, ECCC TR25-049, revision 5: Range Avoidance equivalences specify the algorithmic class, oracle access and stretch needed for lower-bound consequences. The current affine-cell experiments do not meet those hypotheses.
- Itsykson, Knop, Romashchenko and Sokolov, STACS 2017: OBDD-based algorithms can require large representations even for formulas encoding linear systems over `GF(2)`. Easy affine leaves do not automatically imply a small global branching representation.
- Buss, Das and Knop, CSL 2020: decision trees and branching programs are studied as proof-complexity objects with nontrivial simulation and lower-bound questions.
- Raz and Tzameret, Resolution over Linear Equations and multilinear proofs: proof systems allowing linear equations behave differently from ordinary resolution and require separate analysis.
- Gryaznov, Ovcharov and Riazanov, 2024, tree-like resolution with parity: parity-aware branching systems have their own lower-bound landscape.

## Claim discipline

The terms `L_aff`, `D_aff` and `G_aff` are repository-local finite parameters. No equivalence to resolution width, OBDD size, Res-Lin, or tree-like Res(parity) is claimed. Establishing a simulation in either direction is a separate theorem target.
