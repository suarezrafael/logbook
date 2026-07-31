# Minimal Unsatisfiable Signed-Majority Motifs in Linear 3-Uniform Hypergraphs

**A computer-assisted research note**

**Author:** Rafael Vieira Suarez  
**Laboratory version:** V16  
**Status:** Public research note; not peer reviewed; novelty not established.

## Abstract

We study connected linear 3-uniform hypergraphs whose hyperedges are labeled by bits. A labeled edge `{a,b,c}` requires `MAJ(a,b,c)=label`. Equivalently, every labeled hyperedge contributes three clauses to a structured 2-CNF formula. We completely enumerate this constraint family up to five hyperedges. Every labeling on at most four hyperedges is satisfiable. At five hyperedges, exactly 792 labeled constraints are unsatisfiable, carried by 396 generated hypergraphs. They form six signed isomorphism classes and three classes after identifying global bit-complementation. Every witness is minimally unsatisfiable and admits exactly three decompositions into a four-edge one-live forcing motif plus a cap edge. An independent implementation regenerates the universe, verifies every witness by exhaustive truth-table evaluation, and confirms the classification. The result is a finite, computer-assisted classification, not a circuit lower bound and not a resolution of P versus NP.

## 1. Definitions

A **signed-majority motif** is a pair `(H, σ)`, where:

- `H` is a connected linear 3-uniform hypergraph;
- `σ : E(H) → {0,1}`;
- a vertex assignment satisfies the motif when `MAJ(x_a,x_b,x_c)=σ(e)` for every edge `e={a,b,c}`.

A motif is **minimally unsatisfiable** when it is unsatisfiable and deletion of any edge makes it satisfiable.

Global complementation maps every vertex bit and every edge label to its complement. We identify classes related by this symmetry when explicitly stated.

## 2. Structured 2-SAT translation

For an edge `{a,b,c}` labeled `1`, the constraint is equivalent to:

- `(a ∨ b)`;
- `(a ∨ c)`;
- `(b ∨ c)`.

For label `0`, it is equivalent to:

- `(¬a ∨ ¬b)`;
- `(¬a ∨ ¬c)`;
- `(¬b ∨ ¬c)`.

Therefore satisfiability can be checked using implication graphs.

## 3. Main finite theorem

**Theorem (computer-assisted, finite scope).** Among connected linear 3-uniform signed-majority motifs with at most five hyperedges:

1. every motif with at most four hyperedges is satisfiable;
2. the minimum number of hyperedges in an unsatisfiable motif is five;
3. there are 792 unsatisfiable labeled motifs in the generated canonical universe, supported on 396 hypergraphs;
4. there are six signed isomorphism classes, or three after global complementation;
5. every witness is minimally unsatisfiable;
6. every witness has exactly three decompositions obtained by removing a cap edge, leaving a four-edge one-live forcing motif.

### Enumeration counts

| Edges | Hypergraphs | Labelings | Unsatisfiable |
|---:|---:|---:|---:|
| 1 | 1 | 2 | 0 |
| 2 | 3 | 12 | 0 |
| 3 | 27 | 216 | 0 |
| 4 | 471 | 7,536 | 0 |
| 5 | 13,059 | 417,888 | 792 |

## 4. Three obstruction classes

### U1 — block graph `K5−e`

Representative edges:

```text
(0,1,2)
(0,3,5)
(1,4,6)
(2,3,4)
(2,5,6)
```

Representative labels: `01100`; complement: `10011`.

A contradictory implication cycle is witnessed by:

```text
1 → -2 → 5 → -4 → 6 → -7 → 2 → -1
-1 → 4 → -5 → 7 → -6 → 1
```

### U2 — seven-edge block graph

Representative edges:

```text
(0,1,2)
(0,4,5)
(1,6,7)
(2,3,4)
(3,5,6)
```

Representative labels: `01110`; complement: `10001`.

### U3 — block graph `K2,3`

Representative edges:

```text
(0,1,2)
(0,5,8)
(1,3,4)
(2,6,7)
(3,5,6)
```

Representative labels: `01110`; complement: `10001`.

## 5. Cap decomposition

Removing a suitable edge from any five-edge witness leaves a four-edge motif with exactly two satisfying assignments. At least one remaining vertex is free and every other used vertex is an affine expression in that bit: `0`, `1`, `x`, or `¬x`.

The removed edge evaluates to a constant on both assignments, including all extensions of vertices occurring only in the removed edge. Requesting the opposite label creates the contradiction.

The exhaustive result is stronger: every one of the 792 witnesses has exactly three such cap decompositions.

## 6. Independent verification

The standalone verifier uses:

- an independently implemented incremental hypergraph generator;
- Tarjan SCC for 2-SAT;
- exhaustive truth-table evaluation of every unsatisfiable witness;
- exhaustive verification that deleting any edge makes the motif satisfiable;
- exact canonicalization under all five gate permutations.

It reproduces:

```text
hypergraphs: 1, 3, 27, 471, 13059
unsatisfiable labelings: 0, 0, 0, 0, 792
labeled witness hypergraphs: 396
signed classes: 6
classes up to complement: 3
cap decompositions: exactly 3 for every witness
```

## 7. The V14 counterexample

The policy counterexample with seed `18100004` has 28 inputs and 29 outputs. It contains 19 copies of the three obstruction structures. One certificate uses output gates `0,2,5,7,11` with the partial output `01010`; the complementary pattern `10101` is also impossible. Thus the local obstruction method resolves the instance directly, without the learned policy or rollout.

## 8. Completeness and limitations

The enumeration is complete for the stated finite scope because each connected 3-uniform hypergraph can be constructed incrementally, and each new edge introduces at most two fresh vertices. All legal intersections are enumerated and linearity is checked.

This note does **not** establish:

- a new asymptotic range-avoidance algorithm;
- a new lower bound for unrestricted Boolean circuits;
- novelty relative to all existing literature;
- `P=NP` or `P≠NP`.

## 9. Related work

- Kuntewar and Sarma, *Range Avoidance in Boolean Circuits via Turan-type Bounds*, arXiv:2503.17114 / ECCC TR25-034.
- Aharoni and Linial, *Minimal non-two-colorable hypergraphs and minimal unsatisfiable formulas*, JCTA 43(2), 1986.
- Karve and Hirani, *The complete set of minimal simple graphs that support unsatisfiable 2-CNFs*, arXiv:1812.10849.
- Carmosino, Dang, and Jackman, *Convergent Gate Elimination and Constructive Circuit Lower Bounds*, arXiv:2602.17942.

## 10. Publication status

This repository should be treated as an open computational research note. The classification should be reviewed by specialists before being described as novel or cited as a theorem.