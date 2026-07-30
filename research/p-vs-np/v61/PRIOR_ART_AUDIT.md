# Prior-art audit

## Method

This audit used primary papers or official paper records. It distinguishes:

- **known background** — do not claim novelty;
- **direct overlap** — cite and compare theorem statements;
- **specific contribution, novelty unresolved** — preserve only a narrow claim;
- **not located in this pass** — not evidence of novelty.

## 1. Range Avoidance and lower-bound connections

### Ren, Santhanam and Wang

**Source:** *On the Range Avoidance Problem for Circuits*, ECCC TR22-048, 2022.

The paper frames Avoid, connects algorithms for weak circuit classes to circuit analysis and lower bounds, and gives hardness consequences for weak circuits. Therefore the repository must not present the general bridge from Avoid to explicit constructions or lower bounds as its contribution.

**Classification:** known background.

### Guruswami, Lyu and Wang

**Source:** *Range Avoidance for Low-Depth Circuits and Connections to Pseudorandomness*, RANDOM 2022, DOI `10.4230/LIPIcs.APPROX/RANDOM.2022.20`.

They give polynomial-time algorithms for `NC0_2-Avoid` and hitting-set results for low-depth classes.

**Classification:** known algorithmic baseline.

### Gajulapalli, Golovnev, Nagargoje and Saraogi

**Source:** *Range Avoidance for Constant-Depth Circuits: Hardness and Algorithms*, ECCC TR23-021 / RANDOM 2023.

They identify the general `NC0_3` frontier, prove a rigidity connection for stretch `n+n^(2/3)` with an NP oracle, and give deterministic algorithms at larger stretch.

**Classification:** mandatory context for every `NC0_3-Avoid` statement.

## 2. Monotone ternary overlap

### Kuntewar and Sarma

**Source:** *Range Avoidance in Boolean Circuits via Turan-type Bounds*, arXiv:2503.17114 / ECCC TR25-034, 2025.

They prove deterministic polynomial-time `MONOTONE-NC0_3-Avoid` for `m>n`, using a hypergraph/Turán framework.

**Impact on this repository:**

- V54 cannot claim the first positive-stretch deterministic algorithm for monotone ternary local circuits.
- V54 may still offer a different certificate: an explicit degree-at-most-four separator for pure `AND3`, and a degree-at-most-`k+1` construction for pure `AND_k`.
- The manuscript must compare the exact circuit class, output polarities, certificate form and generality.

**Classification:** direct overlap for monotone `k=3`; exact certificate comparison required.

## 3. CNF and 2-CNF irredundancy

### Liberatore — general CNF

**Source:** *Redundancy in Logic I: CNF Propositional Formulae*, arXiv:cs/0211031, journal DOI `10.1016/j.artint.2004.11.002`.

This work studies redundant clauses and irredundant equivalent subsets of CNF formulas.

**Classification:** the general notion is prior art.

### Liberatore — 2-CNF and Horn

**Source:** *Redundancy in Logic II: 2CNF and Horn Propositional Formulae*, arXiv:cs/0506074, journal DOI `10.1016/j.artint.2007.06.003`.

This work specifically studies redundancy and irredundant equivalent subsets in 2-CNF, including the role of cyclicity.

**Impact on V57:**

V57 must not claim novelty for:

- checking whether a 2-CNF clause/block follows from the others;
- irredundant equivalent subsets as a concept;
- implication-graph approaches to redundancy.

A defensible narrow contribution would be the constrained circuit-image construction:

- every block is a local fiber from one ternary NPN orbit;
- five blocks on four variables at stretch one;
- complete finite classification of the 12 normalized families into one variable-isomorphism class;
- an infinite direct-sum family under the same gate restrictions.

**Classification:** general concept known; specific constrained construction novelty unresolved.

### Savický — UCP irredundancy

**Source:** *On CNF formulas irredundant with respect to unit clause propagation*, arXiv:2309.01750, 2023.

This defines and studies UCP-equivalence and UCP-irredundant formulas.

**Impact on V59:**

The unit-propagation plateau should be described as a Range-Avoidance-specific barrier for a particular potential, not as a new theory of UCP irredundancy.

**Classification:** neighboring established notion.

## 4. Randomized output sampling

The observation that a uniformly random output misses the range with probability at least `1-2^(n-m)` follows immediately from `|Range(C)|<=2^n`. Modern Range-Avoidance papers explicitly describe a natural randomized algorithm.

**Impact on V60:** scope theorem only; no novelty claim.

## 5. Affine fibers

The V56 proof uses consistency of affine systems, translation by a common solution and a complete-block linear-dependence argument.

This audit did not locate a source stating the exact theorem for arbitrary mixtures of efficiently represented affine output fibers at minimum positive stretch.

That absence is not evidence of novelty. Searches must continue in:

- linear and affine CSP redundancy;
- matroid representations of grouped equations;
- coding-theoretic syndrome avoidance;
- affine relation clones and co-clones;
- Range Avoidance for XOR/linear circuits.

**Classification:** exact prior art not located; novelty unconfirmed.

## 6. Orientation depth

This audit did not locate the exact parameter:

> Hamming distance from a selected image point to the internal boundary, used as the exponent in an orientation-enumeration algorithm for bijunctive fibers.

Potential neighboring literatures include:

- CSP solution graphs and reconfiguration;
- distance to boundary in Boolean relation graphs;
- nearest counterexample and model-based diagnosis;
- implication-graph sensitivity;
- parameterized SAT backdoors.

**Classification:** exact prior art not located; novelty unconfirmed.

## Claim language for the manuscript

Use:

- “we give an explicit orbit-constrained construction”;
- “we formulate orientation depth for this Range-Avoidance setting”;
- “we provide a reproducible finite minimality audit”;
- “to our knowledge, subject to external review”.

Do not use:

- “we introduce irredundant 2-CNF”;
- “the first monotone `NC0_3-Avoid` algorithm at `m>n`”;
- “a new randomized algorithm for Avoid”;
- “this advances P versus NP”.
