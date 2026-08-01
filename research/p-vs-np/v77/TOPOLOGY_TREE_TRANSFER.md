# Restricted topology-tree transfer for support-boundary width

## 1. Setting

Let `M` be the `m` output gates and let

```text
lambda(S) = |union_{i in S} supp(i) intersect union_{i notin S} supp(i)|.
```

A supplied gate branch decomposition is an unrooted subcubic tree `T` whose
leaves are the gates. Every original tree edge displays a gate cut of value at
most `b`.

V76 used labelled top-tree clusters. A top cluster can have two boundary
vertices, and each boundary vertex can expose two source edges, yielding a
safe four-edge cover. V77 changes the prior-art hierarchy: it uses
Frederickson's **topology trees**, whose vertex clusters have a stronger
external-edge invariant.

## 2. Prior-art topology-tree ingredient

A restricted multilevel partition of a ternary tree gives a binary topology
hierarchy of logarithmic height. Every topology cluster is a connected vertex
set satisfying:

1. at most three source-tree edges leave the cluster;
2. a cluster with three leaving edges consists of one vertex;
3. a parent has one or two children from the previous level, and a binary
   parent is their union joined by the unique source-tree edge between them.

The logarithmic-height construction and these cluster rules are prior art due
to Frederickson. Alstrup, Holm, de Lichtenberg, and Thorup explicitly relate
this hierarchy to top trees and describe the same three-boundary-edge
singleton exception.

For an `m`-leaf subcubic branch tree, the number of source vertices is `O(m)`,
so the topology hierarchy has height `O(log m)`.

## 3. Leaf-label pruning lemma

Attach gate label `i` to source leaf `i`. Start with singleton vertex base
clusters, delete topology branches containing no gate label, and suppress every
unary node. The resulting hierarchy is a rooted binary tree whose leaves are
exactly the gate labels. Every retained node is still an original topology
cluster.

**Lemma (retained two-edge lemma).** Every retained label-bearing topology
cluster has at most two source-tree edges leaving it.

**Proof.** If the retained cluster has more than one vertex, the topology-tree
rule excludes external degree three, hence at most two edges leave it. If it
has one vertex and contains a gate label, that vertex is a source-tree leaf and
has degree one. Thus the external degree is at most one in the singleton
case. In all cases it is at most two. `□`

Suppressing unary nodes never increases height. Since the pruned tree has
`m` leaves and height `O(log m)`, its external path length is `O(m log m)`.

## 4. Two-edge support-boundary cover

Let `C` be a retained cluster and `S(C)` its gate labels. Take an input
variable occurring in one gate of `S(C)` and one gate outside `S(C)`. The
unique path between the two source leaves exits the connected vertex cluster
`C`, and therefore crosses one of its at most two boundary edges. The variable
belongs to the middle set of that source edge. Hence

```text
boundary_variables(S(C))
    ⊆ union of the middle sets of at most two original edges.
```

Each original middle set has size at most `b`, so

```text
lambda(S(C)) <= 2b.
```

This proof uses only connectivity of the source tree and the topology-cluster
external-edge invariant. It does not reuse the rejected V76 centroid
invariant.

## 5. Transfer theorem

**Theorem (restricted topology-tree transfer).** From a supplied width-`b`
subcubic gate branch decomposition, one obtains a rooted binary gate tree `T'`
with

```text
width(T') <= 2b,
height(T') = O(log m),
EPL(T') = O(m log m).
```

The hierarchy and logarithmic height are prior art. The new width statement is
the retained two-edge lemma followed by the support-boundary path argument.

## 6. Consequence for V75

V75's symbolic residual circuit on a tree of width `w` and logarithmic height
has incremental prefix-avoidance time

```text
O(m log m A(w)^2 poly(n,m)).
```

Substituting `w <= 2b` gives

```text
O(m log m A(2b)^2 poly(n,m)).
```

This strictly improves the V76 parameter dependence `A(4b)^2`. V76 remains a
correct but dominated four-edge transfer.

## 7. Tightness of the two-edge inequality

A four-gate quartet has a valid connected cluster with exactly two boundary
edges. Put one disjoint block of `b=3` variables across the left boundary
edge and another disjoint block of three variables across the right boundary
edge. Every source middle set has size at most three, while the cluster
support boundary has size six.

Thus the inequality

```text
lambda(S(C)) <= 2b
```

can be tight for a particular valid cluster. This is **not** a lower bound for
every logarithmic-height hierarchy: a different hierarchy may avoid that
cluster.

## 8. Finite validation

The deterministic audit includes:

- `2,055` ordered source-tree shapes through nine leaves;
- `73,239` topology clusters and `33,097` retained label clusters;
- no retained cluster with three boundary edges;
- `256` seeded support systems and `5,132` direct cluster-cover checks;
- an independently checkable static topology certificate;
- all `245,505` simple rank-at-most-three support families on five variables
  through six gates, reduced to `2,802` variable-isomorphism orbits;
- the six V76 seven-gate perfect-height tradeoff witnesses.

The finite experiments validate the implementation and expose the size of the
parameter improvement. They are not the proof of the topology-tree theorem.

## 9. Prior-art boundary

- Greg N. Frederickson, *Ambivalent Data Structures for Dynamic
  2-Edge-Connectivity and k Smallest Spanning Trees*, SIAM J. Comput. 26(2),
  1997, DOI `10.1137/S0097539792226825`.
- Stephen Alstrup, Jacob Holm, Kristian de Lichtenberg, and Mikkel Thorup,
  *Maintaining Information in Fully-Dynamic Trees with Top Trees*,
  arXiv `cs/0310065`.
- Korhonen and Oum's 2026 FPT branchwidth algorithm concerns decomposition
  discovery; V77 assumes a supplied decomposition and transfers it.

V77 does not claim a new topology-tree data structure. The laboratory claim
is the support-boundary corollary after pruning to degree-one gate labels.
Novelty remains unconfirmed.

## 10. Nonclaims

V77 does not establish:

- that factor two is optimal for all logarithmic-height hierarchies;
- that width preservation is impossible;
- unrestricted `NC0_3-Avoid`;
- a standard branching-program, proof-complexity, or circuit lower bound;
- `P != NP` or `P = NP`;
- peer review or confirmed novelty.
