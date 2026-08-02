# Deficiency conservation and the Minimum p-Union boundary

## 1. Setting

Let `M` be the output gates, `X=N(M)` the active input variables, and

```text
sigma = |M| - |X|.
```

For `S subseteq M`, define

```text
N(S)      = union of the supports of gates in S,
delta(S)  = |S| - |N(S)|,
lambda(S) = |N(S) intersect N(M\S)|.
```

Deficiency may be negative. Hall deficiency means `delta(S)>0`.

## 2. Conservation law

**Theorem 1 (deficiency conservation).** For every `S subseteq M`,

```text
delta(S) + delta(M\S) = sigma - lambda(S).
```

**Proof.** Inclusion-exclusion gives

```text
|N(S)| + |N(M\S)| = |X| + lambda(S).
```

Subtract this equality from

```text
|S| + |M\S| = |M|.
```

The result is

```text
(|S|-|N(S)|) + (|M\S|-|N(M\S)|)
  = |M|-|X|-lambda(S).
```

This is the claimed identity. `square`

The V80 inequality is the special case in which both deficiencies are
nonpositive. The equality carries more information: width is exactly the
amount of global stretch not present as deficiency on the two sides.

## 3. Constructive balanced-edge consequence

**Lemma 2 (balanced edge).** Every unrooted subcubic tree with `m>=2` labelled
leaves has an edge whose two leaf sides have sizes in

```text
[ceil(m/3), floor(2m/3)].
```

**Proof.** Orient an edge toward a side containing more than `2m/3` leaves,
when such a side exists. There is no directed cycle, so some vertex has no
outgoing incident edge. Every component at that vertex has at most `2m/3`
leaves. At most three components meet there and their leaf counts sum to `m`,
so one has at least `m/3` leaves. Its incident edge is balanced. `square`

**Theorem 3 (width-deficiency tradeoff).** Given a width-`w` support branch
decomposition, scan its edges to find the balanced edge from Lemma 2. For one
of its sides `S`,

```text
delta(S) >= ceil((sigma-w)/2).
```

**Proof.** The displayed cut has `lambda(S)<=w`. Theorem 1 yields

```text
delta(S)+delta(M\S) >= sigma-w.
```

At least one of two integers has value at least the ceiling of half their sum.
The scan is polynomial once the decomposition is supplied. `square`

This theorem does not derandomize avoidance. High deficiency only improves the
success probability of the randomized NP-oracle procedure already available
from the full gate set. The value is structural: it makes the low-width arm of
the V80 dichotomy output a quantitative Hall witness as well as an FPT
avoidance decomposition.

## 4. Minimum-neighborhood Hall as Minimum p-Union

Define the Minimum `p`-Union profile

```text
U(p) = min { |N(S)| : S subseteq M and |S|=p }.
```

**Proposition 4.** The minimum neighborhood size of a Hall-deficient gate set is

```text
h* = min { U(p) : U(p)<p }.
```

**Proof.** Every deficient `S` of size `p` has `U(p)<=|N(S)|<p`, so the
right-hand side is at most the optimum. Conversely, a minimizer defining any
`U(p)<p` is Hall deficient and has neighborhood `U(p)`. `square`

This identifies the exact combinatorial object. It is not ordinary
submodular minimization because the feasibility condition compares the
coverage value to the selected cardinality while the objective asks to
minimize coverage.

## 5. What Lagrangian submodular minimization does solve

For rational `alpha>=0`, define

```text
F_alpha(S) = |N(S)| - alpha |S|.
```

The coverage term is submodular and the cardinality term is modular, so
`F_alpha` is submodular. In fact it is a minimum-weight closure problem:

- give each gate a benefit `alpha`;
- give each variable a cost `1`;
- add an infinite-capacity implication from a selected gate to every variable
  in its support.

An `s-t` minimum cut finds a minimizer. A parametric cut algorithm can enumerate
the **supported** points of the lower envelope `(p,U(p))`.

The limitation is exact: an unsupported point can be the first or lowest point
below the Hall diagonal `U(p)=p`. No value of `alpha` then returns it.

## 6. Finite counterexamples to Lagrangian completeness

For the three V80 rank-three families, the complete curves are:

```text
n=7: U = [0,3,4,4,5,5,6,6,6,7,7,7]
n=8: U = [0,3,4,4,5,6,6,7,7,7,8,8,8]
n=9: U = [0,3,4,5,5,6,6,7,8,8,8,9,9,9,9]
```

Their minimum-neighborhood Hall points are respectively

```text
(p,U(p)) = (7,6), (8,7), (9,8).
```

Exact rational interval analysis shows that none is Lagrangian supported. In
all three examples, the only supported point with positive deficiency is the
full set `(m,n)`.

Therefore the suggested Lagrangian scan is a valid polynomial subroutine but
not a complete algorithm for `MIN-NEIGHBORHOOD-HALL`.

## 7. Complexity boundary

The profile `U(p)` is the Minimum `p`-Union problem for the support
hypergraph. For support rank three this is the three-uniform Minimum `p`-Union
regime studied alongside Densest `k`-Subhypergraph and small-set bipartite
vertex expansion.

V81 does not prove either of the following:

1. exact polynomial-time computation of the first Hall-diagonal crossing;
2. NP-hardness of that exact crossing problem under the rank-three and stretch
   promises used by the laboratory.

Either result would be a valid V82 advance. Counterexamples to candidate
algorithms must be promoted before conjectures.

## 8. Tightness control

A rank-one family with eight gates and four active variables admits a balanced
cut with

```text
lambda=0,
delta(S)=2,
delta(M\S)=2,
sigma=4.
```

Thus the factor `1/2` in Theorem 3 is tight if one uses only the conservation
identity for a single balanced cut.

## 9. Nonclaims

The conservation theorem is not a deterministic avoidance algorithm, does not
show that low width occurs in unrestricted circuits, does not solve Minimum
`p`-Union, and does not imply a circuit lower bound or P versus NP.
