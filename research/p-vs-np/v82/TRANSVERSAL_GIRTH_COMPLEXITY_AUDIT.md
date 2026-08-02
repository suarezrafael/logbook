# Transversal-girth complexity audit

## 1. Definitions

Let `G=(M,X;E)` be a bipartite graph. The ground set is `M`; a set
`I subseteq M` is independent in the transversal matroid `T(G)` exactly when
there is a matching saturating `I` into `X`.

Write

```text
delta(S) = |S| - |N(S)|
h*(G) = min { |N(S)| : delta(S) > 0 }.
```

The quantity `h*` is the exact `MIN-NEIGHBORHOOD-HALL` objective isolated in
V81.

## 2. Hall neighborhood equals transversal girth minus one

### Lemma 2.1

Assume that `T(G)` has a dependent set. Then

```text
h*(G) = girth(T(G)) - 1.
```

### Proof

Choose, among the sets attaining `h*`, one that is inclusion-minimal; call it
`S`. If a proper subset `R` of `S` were Hall deficient, then
`N(R) subseteq N(S)`, so `|N(R)| <= h*`. The definition of `h*` forces
`|N(R)|=h*`, contradicting the inclusion-minimal choice of `S`. Thus every
proper subset of `S` is matchable while `S` is not, so `S` is a circuit of the
transversal matroid.

For any element `e in S`, the set `S-e` is matchable into `N(S)`. Hence

```text
|N(S)| >= |S|-1.
```

Dependence gives `|N(S)|<|S|`; therefore `|N(S)|=|S|-1`. This proves
`h* >= girth(T(G))-1`.

Conversely, let `C` be a shortest circuit. The same argument gives
`|N(C)|=|C|-1`, so `h* <= girth(T(G))-1`. Equality follows.

## 3. Separation of the two deficiency objectives

### Corollary 3.1

Every inclusion-minimal `h*` minimizer has deficiency exactly one.

This is stronger than a convention about algorithmic arms. The certificate
that minimizes the number of variables is structurally a matroid circuit and
therefore spends exactly one unit of Hall deficiency. High-deficiency
certificates optimize a different quantity. They can improve the success
probability of random sampling with an NP range-membership oracle, but they are
not the minimizers relevant to direct enumeration.

## 4. Verified general hardness

Colbourn and Elmallah prove in Theorem 2.1 of

> C. J. Colbourn and E. S. Elmallah, “Reliable assignments of processors to
> tasks and factoring on matroids,” *Discrete Mathematics* 114 (1993),
> 115–129, DOI `10.1016/0012-365X(93)90360-6`

that determining the minimum circuit cardinality of a transversal matroid
presented by a bipartite graph is NP-hard. Their proof is a reduction from
Clique. Together with Lemma 2.1, this settles the general complexity of exact
`h*`.

The article also proves a counting hardness result for minimum circuits. V82
does not need that stronger counting statement.

Some secondary discussions attribute an earlier reduction to Stockmeyer through
a thesis citation chain. The original item was not verified in this audit.
Accordingly, the published Colbourn–Elmallah theorem is the primary citation;
“Stockmeyer” is retained only as a provenance note, not as the proof source.

## 5. Degree at most two: bicircular boundary

Suppose every gate belongs to at most two supports. Make a multigraph on `X`:

- a gate supported on `{u,v}` becomes the edge `uv`;
- a gate supported on `{u}` becomes a loop/half-edge at `u`.

A gate set is matchable precisely when each connected component of its graph is
a pseudoforest, equivalently has at most one cycle. Thus the resulting
transversal matroid is the bicircular matroid of the presenting graph.

Its circuits are the minimal connected subgraphs with two cycles:

1. a theta graph;
2. two cycles meeting in one vertex (tight handcuff);
3. two vertex-disjoint cycles joined by a path (loose handcuff).

This is the standard bicircular circuit characterization originating with
Simões-Pereira; the characterization of bicircular matroids as transversal
presentations in which each ground element belongs to at most two sets is due
to Matthews and is recorded in later bicircular-matroid literature.

With the graph presentation supplied, shortest-circuit computation is
polynomial: enumerate the constant number of branch/attachment vertices for
the three topologies, then solve the resulting fixed-terminal disjoint-path or
min-cost-flow instances. This is an algorithmic consequence supplied here;
V82 does not claim that a particular cited bicircular paper stated this exact
girth algorithm.

Therefore degree two is a tractable control, while degree three is the first
unresolved support-degree boundary in this audit.

## 6. Parameterized algorithms and the target regime

Panolan, Ramanujan, and Saurabh study Matroid Girth and Connectivity in

> F. Panolan, M. S. Ramanujan, and S. Saurabh, “On the Parameterized
> Complexity of Girth and Connectivity Problems on Linear Matroids,” WADS
> 2015, LNCS 9214, 566–577, DOI `10.1007/978-3-319-21840-3_47`.

Their results include FPT algorithms under combined rank/field parameters and
special handling of transversal matroids and gammoids that avoids exponential
dependence on the representation field size.

This does not close the V82 target. In the three audited target-stretch
families, the transversal ranks are `7,8,9`, equal to the number of active
variables, and the girths are `7,8,9`. In the asymptotic regime both rank and
the desired circuit size can grow linearly with `n`. Parameterized algorithms
in either quantity therefore do not, by themselves, imply polynomial time for
the unrestricted degree-three family.

V82 deliberately records only this mismatch. It does not assert that the
parameterized algorithms are optimal or unusable on every structured
subfamily.

## 7. Degree-three question and stopping rule

The exact question carried forward is:

```text
Given a transversal presentation in which every ground element has at most
three neighbors, compute its girth (equivalently, compute h*).
```

The literature located in this audit establishes neither a polynomial
algorithm nor NP-hardness for this exact restriction.

The preferred first route is a bounded-degree hardness gadget replacing the
high-degree incidence in the general Clique reduction. Every proposed gadget
must first survive exact finite tests for unintended short circuits.

The algorithmic route remains open: degree three may force a structural
decomposition not present in general transversal matroids.

After three focused mathematical iterations without a complete reduction or
algorithm, the promotable outcome becomes the extended census specified by
V81: sunflower profiles, affine-cell invariant, `G*_proj` growth, and explicit
counterexamples to monotone conjectures.

## 8. Bounded arithmetic

No `APC^1` expansion occurs in V82. The only authorized second-front target
remains the V56 affine certificate, and only after a demonstrated blocker or an
independently valuable proof-complexity theorem.

## 9. Nonclaims

The degree-three boundary is not solved. No novelty or peer-review claim is
made. No direct route to P versus NP is active.
