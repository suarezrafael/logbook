# Labelled top-tree transfer for support-boundary width

## 1. Setting

Let `M` be the set of `m` output gates. For `S ⊆ M`, define

```text
lambda(S) = | union_{i in S} supp(i) intersect union_{i notin S} supp(i) |.
```

This is the number of input variables occurring on both sides of the gate cut.
It is normalized, symmetric, and submodular, since it is a sum of one-variable
cut indicators.

A supplied branch decomposition is an unrooted subcubic tree whose leaves are
the gates. Every original tree edge induces a gate cut of value at most `b`.

## 2. Prior-art ingredient: labelled top trees

Alstrup, Holm, de Lichtenberg, and Thorup define a top tree as a binary
hierarchy of connected tree clusters. Each cluster has at most two boundary
vertices, sibling clusters merge at one vertex, and logarithmic-height top
trees can be maintained. Their labelled extension permits application labels
attached to tree vertices and counts omitted labels when defining a cluster
boundary.

Attach gate `i` as a unique label to leaf `i` of the supplied branch tree. The
underlying labelled tree has `O(m)` edges, vertices, and labels. A standard
binary labelled top tree therefore has height `O(log m)`.

Choose unit-size base clusters so that every gate label is a separate top-tree
leaf. Delete edge-only leaves and suppress unary nodes. The remaining binary
tree has exactly the gate labels as leaves, does not increase height, and every
retained node still corresponds to a labelled top-tree cluster.

## 3. Four-cut cover lemma

**Lemma (Four-cut cover lemma).** Let `C` be a retained labelled top-tree
cluster of a subcubic supplied branch tree, and let `S(C)` be its gate labels.
Then the support-boundary variables of `S(C)` are covered by the middle sets of
at most four original branch edges.

### Proof

A top-tree cluster is connected and has at most two boundary vertices. At one
boundary vertex of a subcubic tree, at most two incident tree edges can cross
between the cluster and its complement. If a gate label at a leaf vertex is
included without its incident edge, or omitted while the leaf vertex belongs
to the cluster, the leaf's unique incident branch edge represents that label
crossing. Thus each boundary vertex contributes at most two original branch
edges, for at most four original branch edges in total.

Take an input variable `x` occurring in one gate of `S(C)` and one gate outside
`S(C)`. In the supplied branch tree, the unique path between those two gate
leaves must cross the labelled-cluster boundary. Hence it crosses one of the
selected original branch edges. The variable `x` belongs to that edge's middle
set. Therefore

```text
boundary_variables(S(C))
    ⊆ union of at most four original middle sets.
```

Every selected edge has middle-set size at most `b`, so

```text
lambda(S(C)) <= 4b.
```

The implementation exhaustively checks this path/cut cover directly from raw
incidence sets, including clusters that omit labels at boundary leaf vertices.

## 4. Top-tree transfer theorem

**Theorem (Top-tree transfer theorem).** From a supplied width-`b` subcubic
gate branch decomposition, one can construct a rooted binary gate decomposition
`T'` such that

```text
width(T') <= 4b,
height(T') = O(log m),
EPL(T') = O(m log m).
```

The logarithmic-height labelled top tree is the standard prior-art
construction. The width statement follows from the four-cut cover lemma at
every retained node. Since the gate tree has `m` leaves and logarithmic height,
its external path length is `O(m log m)`.

## 5. V75 consequence

V75 compiles the exact weighted residual recurrence on a supplied tree of width
`w` into a monotone arithmetic DAG and bounds incremental work through the
external path length. Rebuild that circuit on `T'` with `w <= 4b`. This gives

```text
O(m log m A(4b)^2 poly(n,m))
```

incremental prefix-avoidance time.

This closes the *depth* gap for the parameterized, supplied-decomposition
regime. The cost of replacing `b` by `4b` may be large because `A` grows
rapidly, so tightening the transfer remains important.

## 6. Perfect-height tradeoff witness

For the rank-two supports

```text
{0}, {1}, {0,2}, {0,3}, {1,2}, {1,3}, {2,3},
```

all `10,395` rooted unordered binary gate trees were enumerated. The exact
nondominated `(width,height,EPL)` frontier is

```text
(2,4,21), (3,3,20).
```

Since `ceil(log2 7)=3`, width two cannot coexist with the minimum possible leaf
height on this instance. This finite result **does not refute width-preserving
O(log m)** balancing: height four remains logarithmic. It also does not prove
that the factor four above is optimal.

## 7. Failed-route record

An earlier candidate used recursive weighted centroids and claimed width `2b`.
That proof was rejected before publication. In a recursive component, the side
facing a previously removed centroid need not remain one side of a single
original branch edge; the proposed invariant could accumulate boundary cuts.
The final V76 result makes no `2b` centroid claim. This discarded centroid
argument is retained here as a methodological control against optimistic
balancing proofs.

## 8. Prior-art and discovery boundary

- Alstrup--Holm--de Lichtenberg--Thorup provide logarithmic-height labelled top
  trees and the two-boundary cluster framework.
- Fomin and Korhonen study factor-two approximation for branchwidth of general
  connectivity functions.
- Korhonen and Oum give an FPT algorithm for finding width-`k` branch
  decompositions of oracle connectivity functions.

V76 assumes or receives a supplied decomposition and then transfers it. It does
not claim a new top-tree data structure or replace decomposition discovery.
Novelty of the support-boundary corollary is unconfirmed.

## 9. Nonclaims

V76 does not establish any of the following:

- that `4b` is optimal;
- that a `2b`, `b+O(1)`, or width-preserving logarithmic transfer is impossible;
- a polynomial dependence on unrestricted branchwidth, since `A(4b)` remains
  parameter dependent;
- unrestricted `NC0_3-Avoid`;
- a standard branching-program, proof-complexity, or circuit lower bound;
- `P != NP` or `P = NP`;
- peer review or confirmed novelty.
