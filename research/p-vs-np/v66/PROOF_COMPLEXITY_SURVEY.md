# Proof-complexity adjacency audit

Affine-cell branching is structurally similar to DPLL-style case analysis, but the repository does not identify its trees or DAGs with an established proof system.

## Relevant primary sources

- Huang, Li and Zhong, ECCC TR25-049, revision 5: Range Avoidance equivalences specify the algorithmic class, oracle access and stretch needed for lower-bound consequences. The current affine-cell results do not meet those hypotheses.
- Itsykson, Knop, Romashchenko and Sokolov, STACS 2017: OBDD-based algorithms can require large representations even for formulas encoding linear systems over `GF(2)`. Easy affine leaves do not automatically imply a small global branching representation.
- Buss, Das and Knop, CSL 2020: decision trees and branching programs are proof-complexity objects with nontrivial simulation and lower-bound questions.
- Raz and Tzameret, Resolution over Linear Equations: proof systems allowing linear equations behave differently from ordinary resolution and require separate analysis.

## V68 update

V68 proves an exponential lower bound for complete leaves in one repository-local affine-cell tree model, while the same spine family has a linear DAG after existential projection of dead variables. This demonstrates that tree history and projected residual state are not interchangeable.

The V68 parameter `G_proj` is not identified with OBDD size, FBDD size, resolution size, Res-Lin size, or another standard measure. Tseitin/expander systems are future experimental candidates, but no existing lower bound can be imported until a size-preserving simulation theorem is stated and proved.

## Claim discipline

The terms `L_aff`, `D_aff`, `G_aff`, and `G_proj` are repository-local parameters with different state semantics. Establishing a simulation in either direction remains a separate theorem target.
