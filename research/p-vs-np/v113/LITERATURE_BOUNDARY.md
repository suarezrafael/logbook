# V113 literature boundary

## Classical ingredients

### Dominators

Thomas Lengauer and Robert E. Tarjan, **A Fast Algorithm for Finding Dominators in a Flowgraph**, ACM TOPLAS 1(1), 1979, pp. 121–141, DOI `10.1145/357062.357071`.

The dominator-tree viewpoint used by V113 is classical. V113's reference implementation deliberately uses repeated deletion/reachability rather than claiming a new dominator algorithm.

### Disjoint paths / max-flow

The proof that two routes can be made gate-disjoint outside the common dominators uses standard node splitting, integral max-flow, and max-flow/min-cut reasoning. V113 makes no novelty claim for these graph-algorithm tools.

### Minimum Shared Edges

Till Fluschnik, Stefan Kratsch, Rolf Niedermeier, Manuel Sorge, **The Parameterized Complexity of the Minimum Shared Edges Problem**, JCSS 106 (2019), 23–48; earlier FSTTCS 2015 version DOI `10.4230/LIPIcs.FSTTCS.2015.448`.

That literature studies a more general shared-edge routing objective (including arbitrary path multiplicity) and records hardness/FPT phenomena. It is a calibration warning against extrapolating V113's very special two-route, common-sink, gate-resource structure to general shared-path problems.

## What V113 does not claim as prior-art-free

V113 does not claim novelty for:

- dominators or dominator trees;
- node splitting;
- max-flow/min-cut;
- integral two-flow decomposition;
- dynamic programming over a constant state space in general.

## Project-specific statement requiring external review

The statement that has not been located explicitly in the targeted search is the following composition for signed essential MUX range avoidance:

1. for a fixed opposite-phase first pair, minimum shared return-gate overlap equals the number of common gate dominators;
2. optimum pairs decompose into gate-disjoint dominator intervals;
3. target compatibility over the entire optimum face is decided by four branch states per common dominator plus ordinary two-flow transition tests;
4. an accepted witness constructs a missing circuit output.

The first two bullets are close to standard graph-flow consequences; the last two use the signed-MUX target semantics. No novelty or priority claim is made until expert comparison with the literature is performed.

## Range-avoidance boundary

V113 remains a special-class result inside the ongoing `NC0_3-Avoid` program. It does not supersede current general local range-avoidance algorithms and does not prove unrestricted `NC0_3-Avoid` in deterministic polynomial time.
