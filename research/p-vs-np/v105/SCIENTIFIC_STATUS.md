# V105 scientific status

**Classification:** experimental frontier progress; not an official candidate.

Internally established symbolically:

- exact signed-majority target constraints contain three 2-CNF pair clauses;
- a canonical pair edge transports either chosen source polarity by a fixed XOR
  label determined by the two local literal signs;
- an odd canonical-pair triangle can be targeted to give `a -> not a`;
- two vertex-disjoint odd triangles joined by a disjoint path can be targeted so
  the implication graph contains a variable and its negation in one SCC;
- the resulting missing output is polynomial-time constructible;
- an explicit exact-stretch switching-unbalanced family has no proper
  positive-surplus output subset and keeps V97/V101/V102/V103/V104 structural
  scales linear while V105 is polynomial time.

Pre-registration falsification:

- complete original-range checks for the explicit family at `8<=n<=15` produced
  zero counterexamples;
- exact small-instance strong-affine-backdoor values matched `floor(2n/3)`;
- switching imbalance and minimum support degree were checked directly.

Committed but not yet repository-CI validated:

- primary verifier with 500 additional random-polarity complete-range checks;
- independent 2-SAT SCC implementation with implication checks through `n=106`,
  small complete-range checks, and 240 additional random-polarity cases.

Not established:

- polynomial-time avoidance for arbitrary signed-majority exact-stretch circuits;
- a structural theorem forcing an implication dumbbell from `m>n` alone;
- unrestricted polynomial-time `NC0_3-Avoid`;
- improvement of the published unrestricted worst-case exponent;
- novelty, priority, peer review, a new circuit lower bound, or P versus NP.
