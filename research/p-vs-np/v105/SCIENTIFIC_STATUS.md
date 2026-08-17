# V105 scientific status

**Classification:** frontier progress; V104 is promoted and V105 is the official candidate pending repository gates.

Established symbolically in the candidate package:

- a fixed signed-majority output target is exactly a conjunction of three binary
  2-CNF clauses;
- a chosen canonical pair transports either source polarity by the XOR label
  `delta_e = 1 XOR p_u XOR p_v`;
- odd transport around a pair cycle flips the propagated literal;
- two edge-disjoint odd cycles in a simple bicyclic barbell or figure-eight can
  be targeted to put a variable and its negation in one implication SCC;
- such components are recognized constructively in polynomial time by leaf
  pruning and 2-core degree/path tracing;
- the strict exact-stretch switching-unbalanced family has no proper
  positive-surplus output subset and satisfies
  `lambda=mu=nu=eta_AF=n`, `beta=floor(2n/3)`, while V105 is polynomial time;
- Karve--Hirani's four known simple 2GraphSAT obstruction skeletons were
  independently classified under the stricter majority-induced complementary
  pair clauses: `K4/Butterfly/Bowtie/K1,1,3` have respectively
  `8/16/32/48` compatible transport signings.

Candidate verification package:

- primary complete-range checks for the strict family at `8<=n<=15`;
- 500 additional random-polarity complete-range cases;
- arbitrary-length odd barbell and figure-eight checks, plus explicit theta
  rejection by the canonical-pair detector;
- exact small-instance backdoor and proper-surplus audits;
- independent 2-SAT SCC implementation with complete-range checks, 240 random
  polarity cases, SCC checks through `n=106`, and exhaustive sign/target census
  on all four Karve--Hirani skeletons.

Repository quick/LaTeX, compatibility and full replay gates have not yet been
run on the V105 candidate head.

Promising but **not proved** and not part of the V105 theorem:

- adaptive selection of one of the three pair clauses per majority output. Small
  nondegenerate searches found no counterexample so far, including exhaustive
  `n=3` function classes and random `n=4..6` samples, but the current selector is
  exponential and there is no universal theorem.

Not established:

- polynomial-time avoidance for arbitrary signed-majority exact-stretch circuits;
- a polynomial or structural theorem for adaptive pair selection;
- unrestricted polynomial-time `NC0_3-Avoid`;
- improvement of the published unrestricted worst-case exponent;
- novelty, priority, peer review, a new circuit lower bound, or P versus NP.
