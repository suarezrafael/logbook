# V115 literature boundary

## DAG two-disjoint paths

Torsten Tholey, **Linear time algorithms for two disjoint paths problems on directed acyclic graphs**, *Theoretical Computer Science* 465 (2012), 35--48. DOI: `10.1016/j.tcs.2012.09.025`.

Tholey proves optimal linear-time algorithms for the 2-disjoint-paths problem on directed acyclic graphs, for vertex- and edge-disjoint variants. V115 uses only the weaker fact that the relevant fixed-terminal two-flow subproblems in an acyclic stage are polynomial; the implementation uses ordinary integral max flow with unit output-gate capacities rather than importing Tholey's specialized data structure.

## General directed hardness

Steven Fortune, John Hopcroft, James Wyllie, **The directed subgraph homeomorphism problem**, *Theoretical Computer Science* 10(2) (1980), 111--121. DOI: `10.1016/0304-3975(80)90009-2`.

This classical work underlies the hardness of directed disjoint linkage already at two terminal pairs. V114 uses this boundary to show that a generic arbitrary extra-shared-gate completion oracle is not available on unrestricted directed return graphs.

## Claim boundary

V115 does not claim novelty for DAG disjoint-path algorithms or directed linkage hardness. Its internal theorem is a transfer statement specific to the signed-MUX range-avoidance framework:

- V113 common gate-dominator stages;
- signed branch/source phases and target compatibility;
- one extra shared non-dominator gate;
- a DAG separation lemma allowing prefix/suffix flow factorization;
- exact positive-stretch separation from the V113 `Delta=0` regime.

Whether this transfer is novel in the broader range-avoidance/circuit-complexity literature remains unconfirmed pending external review.
