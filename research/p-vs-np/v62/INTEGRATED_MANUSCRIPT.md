# Range Avoidance for Local Boolean Circuits:
# Affine Algorithms, Bijunctive Barriers, and Orientation Depth

## Draft status

This is an internal manuscript draft assembled from Laboratories V54–V62. The proofs and computations are reproducible inside the repository, but the manuscript has not been peer reviewed. Novelty and priority are deliberately left unresolved. The paper does not claim an unrestricted circuit lower bound or progress toward resolving P versus NP.

## Abstract

Range Avoidance asks, given a stretching Boolean circuit `C:{0,1}^n->{0,1}^m` with `m>n`, for an output outside `Range(C)`. We study local circuits through the logical structure of individual output fibers. Our central positive result is a consistency-or-redundancy algorithm for circuits in which a chosen fiber of every output is represented by an affine system over `GF(2)`: at minimum positive stretch, either the selected systems are inconsistent or one complete equation block is linearly implied by the others, yielding a deterministic missing output. We then show that the natural extension of this argument to bijunctive fibers fails. Five ternary gates from one NPN orbit on four input variables have jointly satisfiable 2-CNF fibers, a unique common assignment, and no redundant gate block; direct sums yield an infinite stretch-one family. In standard terminology, the collapsed conjunction is a clause-irredundant 2-CNF, while the circuit contribution is the partition into essential orbit-constrained gate blocks. To describe what remains algorithmically possible, we define orientation depth as the Hamming distance from a selected image point to the internal boundary of the image. For bijunctive fibers, depth `d` gives an `m^{O(d)} poly(n+m)` deterministic algorithm. Cube isoperimetry shows that the boundary is globally abundant, but the explicit direct-sum family defeats several natural strict-improvement potentials. Finally, we separate this deterministic-localization question from randomized avoidance: whenever image membership is polynomial-time, uniform output sampling finds a missing word in at most two expected trials. The result is a scoped structural account of an affine/bijunctive frontier, not a claim about general `NC0_3-Avoid`.

## 1. Introduction

For a Boolean circuit

```text
C : {0,1}^n -> {0,1}^m,  m>n,
```

Range Avoidance asks for a word `y` not attained by the circuit. The existence of such a word follows from counting. The computational problem is to construct one deterministically.

Range Avoidance has important connections to explicit constructions and circuit lower bounds. Those connections, together with deterministic algorithms for `NC0_2-Avoid` and hardness evidence around `NC0_3-Avoid`, are established in prior work by Ren–Santhanam–Wang, Guruswami–Lyu–Wang, and Gajulapalli–Golovnev–Nagargoje–Saraogi. The present manuscript studies a narrower question: how the logical form of local output fibers controls deterministic avoidance.

The paper is organized around a positive/negative pair.

**Positive side.** If selected output fibers are affine systems over `GF(2)`, minimum positive stretch forces either inconsistency or a redundant complete block. This gives a direct deterministic avoidance algorithm.

**Negative side.** If selected fibers are 2-CNF, consistency and the inequality `m>n` do not force block redundancy. The failure occurs in one ternary NPN orbit at `n=4,m=5` and persists under direct sum.

This pair isolates a genuine structural difference. Affine systems have an ambient rank that bounds complete-block irredundancy. Bijunctive systems have polynomial-time satisfiability and entailment, but no analogous dimension bound for gate blocks.

The later sections ask what can replace fixed-orientation redundancy. Orientation depth parameterizes an exhaustive deterministic search for a boundary edge. Isoperimetry proves that boundary points are plentiful under the uniform measure on image points. Nevertheless, global abundance is not an efficient deterministic locator, and several simple local potentials are flat on an explicit family.

A final counting observation prevents overinterpretation. If membership in `Range(C)` is in polynomial time, uniform output sampling is already a Las Vegas algorithm with success probability at least `1-2^(n-m)`. Thus the bijunctive regime considered here is randomized-easy. Its residual difficulty is deterministic derandomization/localization, not avoidance in the randomized sense.

### 1.1 Contributions and claim boundaries

The manuscript assembles the following internally verified statements.

1. A degree-at-most-`k+1` forcing-core separator for pure `AND_k` circuits with positive stretch.
2. A deterministic affine-fiber algorithm at `m>n` for arbitrary mixtures of efficiently represented affine fibers.
3. An explicit orbit-`0x07` block-irredundancy example and an infinite stretch-one family.
4. A finite minimality audit for the searched `n=3,m=4` universe and a complete `n=4,m=5` normalized classification.
5. Orientation depth and an `m^{O(d)} poly(n+m)` deterministic algorithm for bijunctive fibers.
6. A classical isoperimetric lower bound on internal-boundary abundance.
7. An explicit barrier to exact-forcing, unit-propagation, and fiber-size monotone potentials.
8. A scope theorem showing that easy membership gives at most two expected random trials.

The manuscript does not claim novelty for general CNF/2-CNF irredundancy, unit-propagation irredundance, cube isoperimetry, randomized output sampling, or deterministic monotone `NC0_3-Avoid` at `m>n`.

## 2. Preliminaries

### 2.1 Output fibers and orientations

For an output coordinate `C_i` and a bit `a`, define the fiber

```text
F_{i,a} = {x : C_i(x)=a}.
```

An orientation `y in {0,1}^m` selects one fiber per output, and its preimage is

```text
F_y = intersection_i F_{i,y_i}.
```

The orientation is in the circuit image exactly when `F_y` is nonempty.

A selected block `F_{i,y_i}` is redundant at `y` when

```text
intersection_{j != i} F_{j,y_j} subseteq F_{i,y_i}.
```

If the orientation is consistent and block `i` is redundant, then flipping output `i` produces a missing word.

### 2.2 NPN equivalence

Two local Boolean functions are NPN equivalent when one is obtained from the other by permuting inputs, negating inputs, and optionally complementing the output. For ternary functions, the 256 truth tables form 14 NPN classes. Four essential classes have affine fibers in a suitable orientation; six essential classes have no affine fiber. The orbit represented by `0x07` has bijunctive fibers on both sides and supplies the main negative example.

### 2.3 2-CNF redundancy and IES terminology

For a set of clauses `F`, a clause is redundant if it is entailed by the remaining clauses. An irredundant equivalent subset is an equivalent subformula with no redundant clause. These concepts and their complexity for 2-CNF are due to prior work, especially Liberatore.

The circuit setting groups clauses by gate. We therefore distinguish clause redundancy from **block redundancy**, where all clauses describing one local fiber are removed together.

### 2.4 Image boundary

Let `S=Range(C)`. The internal vertex boundary is

```text
partial_in S = {y in S : exists i, y xor e_i notin S}.
```

A consistent orientation has a redundant block exactly when it is on this internal boundary.

## 3. Forcing-core certificates for pure AND gates

Let `H=(V,E)` be a `k`-uniform support hypergraph and define the pure monomial circuit

```text
C_H(x)_e = product_{v in e} x_v.
```

If `|E|>|V|`, repeated deletion of degree-zero vertices and degree-one vertices together with their unique incident edge cannot destroy positive excess. Therefore the support hypergraph has a nonempty 2-core.

Choose a core edge `e`. For each vertex of `e`, choose a distinct-or-reused witness edge `f != e` in the core containing that vertex. Let `F_e` be the set of witness edges. Whenever all witness outputs equal one, every input of `e` equals one, so output `e` must also equal one. Hence

```text
Q_e(Y) = (1-Y_e) product_{f in F_e} Y_f
```

vanishes on the circuit range. Its degree is at most `k+1`, and the output setting `Y_e=0`, `Y_f=1` for witnesses is absent.

For `AND3`, this gives a degree-at-most-four separator at `m>n`.

### 3.1 Relationship to monotone NC0_3-Avoid

Kuntewar and Sarma prove deterministic polynomial-time `MONOTONE-NC0_3-Avoid` for `m>n` using Turán-type hypergraph structure and loose chi-cycles. Their theorem is algorithmically more general than the pure-`AND3` corollary above. We therefore make no priority claim for monotone ternary avoidance.

The reason to retain the forcing-core proof is its direct algebraic certificate and its pure-`AND_k` degree bound. Whether this separator is an immediate corollary of the Turán proof remains under external review.

## 4. Affine fibers: consistency or complete-block redundancy

Assume that for every output coordinate we choose a value `alpha_i` with a polynomial-size affine description

```text
F_i = {x in GF(2)^n : A_i x = b_i}.
```

Empty fibers are allowed.

### Theorem 4.1 — affine-fiber avoidance

If `m>n`, an output outside the circuit range can be constructed deterministically in polynomial time.

### Proof structure

There are two branches.

#### Inconsistent branch

If the union of all selected equations is inconsistent, find an inclusion-minimal inconsistent equation subsystem. Let `G` be the gate blocks represented in that subsystem. Activating exactly those selected fibers is impossible, so the corresponding output is absent. A product of their normalized output indicators gives a separator of degree at most `n+1`.

#### Consistent branch

Suppose all selected systems share a solution `x*`. Translate `x=x*+z`, turning every system homogeneous. Let

```text
W_i = rowspace(A_i) <= GF(2)^n.
```

Consider a minimal subfamily of blocks whose sum equals `sum_i W_i`. Each block in such a minimal subfamily must increase dimension by at least one, so the subfamily has at most `n` members. Since `m>n`, some block lies outside it and is contained in the sum of the selected blocks. Thus there is an `i` and a set `J` of at most `n` other gates such that

```text
W_i <= sum_{j in J} W_j.
```

Activating the blocks in `J` forces every equation of block `i`. Requesting block `i` inactive gives a missing output.

### 4.2 Interpretation

The proof uses a rank-like measure on **complete equation blocks**. It is stronger than finding one redundant scalar equation: it identifies a whole output fiber whose constraints are implied by other complete output fibers.

The dimension argument is elementary, and the exact prior-art status of this Range-Avoidance formulation is unresolved. The manuscript claims the theorem as an internal result, not as a confirmed first result.

### 4.3 Ternary consequence

The essential affine ternary NPN representatives are

```text
0x01, 0x06, 0x18, 0x69.
```

Arbitrary mixtures of efficiently represented affine fibers from these classes are covered at `m>n`.

## 5. Bijunctive fibers: the block-redundancy analogy fails

The affine proof suggests a tempting conjecture:

```text
m>n and consistent 2-CNF gate blocks
    => some complete gate block is implied by the others.
```

This is false.

### Theorem 5.1 — explicit block-irredundant gadget

There are five gates from the ternary NPN orbit `0x07` on variables `x0,x1,x2,x3` whose selected three-point fibers are

```text
B1 = ¬x0 ∧ (¬x1 ∨  x2)
B2 = ¬x0 ∧ ( x1 ∨ ¬x2)
B3 = ¬x0 ∧ (¬x1 ∨  x3)
B4 = ¬x0 ∧ ( x1 ∨ ¬x3)
B5 = ¬x0 ∧ (¬x2 ∨ ¬x3).
```

Their intersection is the singleton `{0000}`, but deleting any complete block strictly enlarges the model set.

### 5.2 Translation to standard IES terminology

After duplicate copies of `¬x0` are collapsed, the conjunction contains six unique clauses: the unit clause and five binary clauses. Every one of these six clauses is essential. Therefore the collapsed formula is a clause-irredundant 2-CNF and hence an IES of itself.

The circuit-specific statement is stronger in a different direction: the clauses come partitioned into five local gate-fiber blocks, every block is essential, all blocks arise from one NPN orbit, and the instance has minimum positive stretch.

This does not introduce 2-CNF irredundancy. It gives a constrained realization of it inside a local circuit image.

### 5.3 Finite minimality and classification

Under the convention of essential ternary gates with three distinct inputs, exhaustive search over the normalized `n=3,m=4` universe found no consistent completely block-irredundant example. At `n=4,m=5`, 12 normalized families occur; they form one class under variable permutation.

The minimality is computer-assisted and restricted to the enumerated universe. The explicit gadget and its irredundancy have direct proofs.

### 5.4 Infinite family

Taking a direct sum with balanced three-variable, three-output components produces, for every `k>=0`, an example with

```text
n = 4+3k,
m = 5+3k = n+1.
```

All selected blocks remain consistent and essential. Thus the failure is not confined to one small instance.

## 6. Orientation depth

The negative result concerns a fixed orientation. It does not rule out changing selected output values.

For `S=Range(C)` and a baseline `b in S`, define

```text
rho_S(b) = min_{y in partial_in S} d_H(b,y).
```

This is the distance from the baseline to an image point with a missing Hamming neighbor.

### Theorem 6.1 — boundary equivalence

For `y in S`, gate block `i` is redundant in the fiber formula for `y` if and only if

```text
y xor e_i notin S.
```

Hence finding a consistent orientation with a redundant block is exactly finding the internal boundary.

### Theorem 6.2 — FPT algorithm

When both fibers of every output have constant-size 2-CNF descriptions, enumerate all orientations within distance `d` of `b`. For each orientation:

1. test consistency by 2-SAT;
2. if inconsistent, output it as a missing word;
3. otherwise test each block for entailment by the remaining blocks;
4. if a redundant block is found, flip its output coordinate.

The running time is

```text
O((sum_{j=0}^d binom(m,j)) m poly(n+m)).
```

Thus constant orientation depth gives a deterministic polynomial-time algorithm.

### 6.3 Nearby literature

Boolean CSP solution graphs, connectivity, reconfiguration and component diameter are established topics. Orientation depth differs in two ways:

- its vertices are **output words in the circuit image**, not satisfying input assignments of one formula;
- the target is the nearest image vertex with an edge leaving the image, rather than connectivity between two solutions.

No exact equivalent was located in the V62 search. This is not evidence of novelty.

### 6.4 Finite audit

For homogeneous orbit-`0x07` stretch-one circuits, exact normalized search found depth at most one through `n=8`. The case `n=9` remains incomplete and has no theorem status.

## 7. Boundary abundance and localization barriers

For any nonempty set `S` occupying at most half of the `m`-cube, the vertex-isoperimetric theorem implies

```text
|partial_in S| / |S|
  >= binom(m,floor(m/2)) / 2^(m-1)
   = Theta(1/sqrt(m)).
```

Thus boundary points are not exponentially rare under the uniform distribution on distinct image points.

This geometric fact does not automatically produce a deterministic algorithm. It also does not control the distribution induced by a uniform random input, because image points can have highly unequal fiber sizes.

### 7.1 Flat-potential family

In the V57 direct-sum family, the unique interior point and all of its image neighbors have:

- singleton fibers;
- all input variables logically forced;
- zero variables discovered by the chosen unit-propagation count.

Therefore three natural scalar potentials are flat on the first step:

1. exact number of forced variables;
2. number fixed by unit propagation;
3. inverse or size of the exact fiber.

No proof that requires strict improvement of one of these quantities at every step can be universal.

This does not rule out memory, nonmonotone rules, vector potentials, canonical tie-breaking, or other deterministic methods.

## 8. Easy-membership randomized regime

Suppose membership in `Range(C)` is decidable in polynomial time. A uniform `y in {0,1}^m` is outside the range with probability

```text
1 - |Range(C)|/2^m >= 1-2^(n-m).
```

For `m>n`, this is at least `1/2`. Repeating until a missing word is found is a Las Vegas algorithm with expected number of membership tests at most

```text
1/(1-2^(n-m)) <= 2.
```

At stretch one, equality is possible for injective circuits.

For bijunctive fibers, image membership is a 2-SAT test. Consequently the regime studied in Sections 5–7 is randomized-easy. The open issue is deterministic localization or derandomization.

## 9. Computational methodology

The finite results use:

- exact NPN orbit generation;
- normalization by a common solution;
- exhaustive enumeration in explicitly bounded universes;
- complete-object variable-isomorphism checks;
- primary and independent implementations;
- deterministic seeds for randomized diagnostics;
- serialized results and SHA-256 manifests;
- formal preservation of failed conjectures and counterexamples.

Incomplete searches are never promoted to theorems. The `n=9` search remains an open finite audit.

The cumulative runner reports `PASS`, `FAIL`, or a reasoned `SKIP`. V22 is a `SKIP` because the historical serialized certificate dataset was never committed; aggregate counts cannot reconstruct it.

## 10. Related work

### 10.1 Range Avoidance

Ren–Santhanam–Wang and Guruswami–Lyu–Wang establish the broader Range-Avoidance/lower-bound framework and low-depth connections. Gajulapalli et al. give hardness and algorithms for constant-locality circuits and identify the `NC0_3` frontier. These works are the mandatory context; the present manuscript does not re-claim their general reductions or baseline algorithms.

### 10.2 Monotone ternary circuits

Kuntewar–Sarma prove deterministic polynomial-time monotone `NC0_3-Avoid` for `m>n`. Their theorem subsumes the algorithmic pure-`AND3` conclusion. Our V54 argument is retained only for its explicit forcing-core separator and pure-`AND_k` formulation.

### 10.3 Redundancy in 2-CNF

Liberatore develops redundancy and IES theory for CNF and 2-CNF. The V57 construction is described using that terminology. The open claim is not the existence of irredundant 2-CNF, but the exact gate-block/orbit-constrained realization and its finite classification.

Savický's UCP-irredundance is neighboring terminology. The V59 unit-propagation result is only a counterexample to one Range-Avoidance walking potential.

### 10.4 Solution-space geometry

Gopalan et al. and subsequent CSP-reconfiguration literature study solution graphs induced by Hamming-one moves. This provides natural neighboring language for orientation depth, but an exact correspondence has not been identified.

### 10.5 Cube isoperimetry

The boundary lower bound is a classical application of Harper's vertex-isoperimetric theorem, not a new inequality.

## 11. Limitations and open problems

The current work leaves open:

1. the exact prior-art status of the grouped affine-fiber theorem;
2. the exact prior-art status of the orbit-constrained V57 gadget and direct sums;
3. whether orientation depth matches an existing parameter under a translation;
4. deterministic avoidance for meaningful non-affine subclasses not already covered by monotone algorithms;
5. whether depth is bounded or efficiently navigable for the `0x07` orbit;
6. the finite `n=9` one-flip classification;
7. whether the forcing-core separator is implicit in Kuntewar–Sarma's proof.

The paper does not establish a deterministic algorithm for general `NC0_3-Avoid`, a universal bounded orientation depth, an unrestricted circuit lower bound, or `P != NP`.

## 12. External review status

On 2026-07-30, prior-art questions were sent to:

- Karthik Gajulapalli, Jayalal Sarma and Neha Kuntewar for the Range-Avoidance comparison;
- Paolo Liberatore for grouped-clause/IES terminology.

The manuscript is awaiting replies. Sending a question is not peer review, and silence is not evidence of novelty.

## References used in this draft

- P. Gopalan, P. Kolaitis, E. Maneva and C. Papadimitriou, *The Connectivity of Boolean Satisfiability: Computational and Structural Dichotomies*, SIAM J. Comput. 38(6), 2009.
- K. Gajulapalli, A. Golovnev, S. Nagargoje and S. Saraogi, *Range Avoidance for Constant-Depth Circuits: Hardness and Algorithms*, RANDOM 2023 / ECCC TR23-021.
- V. Guruswami, X. Lyu and X. Wang, *Range Avoidance for Low-Depth Circuits and Connections to Pseudorandomness*, RANDOM 2022.
- L. Harper, vertex-isoperimetry of the Boolean cube.
- N. Kuntewar and J. Sarma, *Range Avoidance in Boolean Circuits via Turan-type Bounds*, 2025.
- P. Liberatore, *Redundancy in Logic I: CNF Propositional Formulae*, Artificial Intelligence 163, 2005.
- P. Liberatore, *Redundancy in Logic II: 2CNF and Horn Propositional Formulae*, Artificial Intelligence 172, 2008.
- L. Ren, R. Santhanam and R. Wang, *On the Range Avoidance Problem for Circuits*, ECCC TR22-048, 2022.
- P. Savický, *On CNF formulas irredundant with respect to unit clause propagation*, 2023.
