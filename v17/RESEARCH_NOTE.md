# A Finite-Locality Barrier for Signed-Majority Range Avoidance

**Computer-assisted research note — Laboratory V17**

**Author:** Rafael Vieira Suarez  
**Status:** Not peer reviewed. Novelty not established.

## Abstract

We show that no finite catalogue of constant-size unsatisfiable signed-MAJ3 motifs can cover all connected linear 3-uniform range-avoidance instances with more hyperedges than vertices. The argument combines a simple greedy lemma—every signed acyclic motif is satisfiable—with the existence of biregular bipartite graphs of arbitrarily prescribed girth. Interpreting a (3,4)-biregular graph as an incidence graph yields a linear 3-uniform hypergraph with `m=4n/3`, while sufficiently high girth excludes every motif in a fixed finite family. We also provide an explicit deterministic PEG instance with 450 vertices, 600 hyperedges, incidence girth 10, and cycle rank 751; it excludes all three five-edge obstruction supports classified in Laboratory V16. This is a methodological barrier result, not a circuit lower bound and not a resolution of P versus NP.

## 1. Signed-majority motifs

A signed-majority motif is a linear 3-uniform hypergraph `H` and a bit `σ(e)` for each hyperedge. A vertex assignment satisfies the motif when:

```text
MAJ3(x_a, x_b, x_c) = σ(e)
```

for every edge `e={a,b,c}`.

## 2. Acyclic satisfiability lemma

**Lemma.** Every signed connected Berge-acyclic MAJ3 motif is satisfiable.

Root the incidence tree. Assign the first edge consistently with its label. Whenever a new edge shares one assigned vertex and introduces two fresh vertices, assign both fresh vertices to the requested output bit `b`. Then `MAJ(s,b,b)=b`, independently of the shared value `s`.

The independent verifier exhaustively checked 32,054 labelings of all acyclic generated motifs with at most five edges and found zero counterexamples.

## 3. Finite-locality barrier

**Theorem.** For every finite family `F` of connected linear unsatisfiable signed-MAJ3 motifs, there exist arbitrarily large connected linear 3-uniform hypergraphs with `m>n` containing no member of `F`.

Every motif in `F` contains a Berge cycle. Let `L` bound the required cycle lengths. Choose a (3,4)-biregular bipartite graph with girth greater than `2L`. Interpret degree-3 nodes as hyperedges and degree-4 nodes as vertices. The resulting hypergraph is linear and:

```text
3m = 4n, hence m = 4n/3 > n.
```

Its incidence girth excludes every motif in `F`.

The existence of biregular bipartite graphs with prescribed degrees and girth is imported from published graph theory. The corollary's novelty has not been established.

## 4. Explicit witness against the V16 catalogue

The deterministic PEG host has:

```text
n = 450
m = 600
m/n = 1.333333
incidence girth = 10
cycle rank = 751
```

The V16 obstruction supports have incidence girths 6, 6, and 8. Therefore none occurs in the host.

## 5. Implication for future work

A universal strategy must use certificates whose size grows with the instance or another genuinely global invariant. The V18 program is to synthesize signed-cycle automata that generate contradictory implication paths of variable length.

## 6. Limitations

This note does not prove:

- a new general range-avoidance algorithm;
- a new asymptotic Boolean circuit lower bound;
- P=NP or P≠NP;
- novelty relative to all prior literature.

## 7. Reproduction

The complete V17 package contains the generator, explicit host, barrier certificate, independent verifier, evidence ledger, and compact V18 context. The public note should be treated as a draft for specialist review.