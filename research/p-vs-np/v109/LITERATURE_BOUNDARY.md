# V109 literature boundary

The V109 result is calibrated against the same current primary range-avoidance sources used in V108:

- Guruswami, Lyu, Wang, *Range Avoidance for Low-depth Circuits and Connections to Pseudorandomness* (ECCC TR22-102).
- Gajulapalli, Golovnev, Nagargoje, Saraogi, *Range Avoidance for Constant-Depth Circuits: Hardness and Algorithms* (ECCC TR23-021 / arXiv:2303.05044).
- Kuntewar, Sarma, *Range Avoidance in Boolean Circuits via Turan-type Bounds* (ECCC TR25-034 / arXiv:2503.17114).
- Huang, Li, Zhong, *New Algorithms and Hardness Results for Range Avoidance* (ECCC TR25-049).

Targeted searches for MUX, multiplexer, bijunctive, implication-graph, Menger, gate-disjoint paths, and range avoidance did not locate a primary-source theorem matching the V109 gate-capacitated return-flow dichotomy.

The graph-theoretic ingredients themselves are standard: integral max-flow/min-cut, Menger-style vertex/gate splitting, SCC reachability, and 2-SAT implication reasoning.  V109 makes no novelty or priority claim for those ingredients or for their composition here without external specialist review.

The most important external-check target is the exact correspondence between two units of gate-capacitated return flow and two output-gate-disjoint MUX implication cycles, together with the claim that a value-one minimum cut must be a single gate split edge rather than a source edge.
