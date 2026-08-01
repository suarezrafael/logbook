# Complexity and branch-residual dynamic programming

## 1. Layout parameter

Let `H=(V,E)` be a finite hypergraph with labelled hyperedges. For `S subseteq E`, define

```text
lambda_H(S) = |V(S) intersect V(E-S)|.
```

For an edge order `pi=(e_1,...,e_m)`, let

```text
q(pi) = max_i lambda_H({e_1,...,e_i}),
q*(H) = min_pi q(pi).
```

V71 identified this parameter exactly with the support-frontier optimum used in the projected affine residual program.

## 2. Rank-three complexity theorem

### Decision problem

`3-UNIFORM VERTEX-BOUNDARY LINEAR BRANCH-WIDTH`

```text
Input: a simple three-uniform hypergraph H and integer k.
Question: is q*(H) <= k?
```

### Theorem

The decision problem is NP-complete.

### Membership in NP

A permutation of the `m` labelled hyperedges is a polynomial-size certificate. Scan it from left to right while maintaining, for each vertex, the number of incident processed and unprocessed edges. The maximum number of vertices having both counts positive is `q(pi)`, computable in polynomial time.

### Hardness

Graph linearwidth uses the same boundary function on an ordering of graph edges and is NP-hard. Given a simple graph `G=(V,E)`, introduce a fresh private vertex `z_e` for every edge `e=uv` and form

```text
H_G = (V union {z_e:e in E}, {{u,v,z_e}: e=uv in E}).
```

`H_G` is simple and three-uniform. For every edge subset `S subseteq E`:

1. a private vertex `z_e` occurs in exactly one hyperedge, so it never belongs to both sides of a cut;
2. an original vertex `v` crosses the hypergraph cut exactly when it is incident to a graph edge in `S` and a graph edge outside `S`.

Therefore

```text
lambda_HG(S) = lambda_G(S)
```

for every `S`, and every labelled edge order has the same width in `G` and `H_G`. Hence

```text
q*(H_G) = linearwidth(G).
```

The transformation is polynomial and parameter preserving. NP-hardness together with membership in NP proves NP-completeness.

## 3. Exact subset dynamic program

Let `D[S]` be the minimum possible maximum frontier along an ordering whose processed set is exactly `S`. The final cut value depends only on `S`, so

```text
D[empty] = 0,
D[S] = min_{e in S} max(D[S-{e}], lambda_H(S)).
```

### Correctness

Take an optimal order of `S` and let `e` be its last edge. The preceding prefix is an order of `S-{e}` and has cost at least `D[S-{e}]`; adding `e` incurs the cut `lambda_H(S)`. Thus the optimum is at least the displayed recurrence. Conversely, append `e` to an order attaining `D[S-{e}]`, proving the matching upper bound.

### Complexity

There are `2^m` subsets and at most `m` predecessor choices per subset. With bitset incidence data, each boundary is computed in polynomial time, yielding

```text
O(m 2^m poly(n)) time,
O(2^m) stored DP values,
```

plus predecessor pointers for order reconstruction.

This is an exact exponential audit algorithm, not a polynomial algorithm for unrestricted instances.

## 4. Branch residual dynamic program

Fix an affine-cell system with gate set `E`. Let `T` be a rooted binary tree whose leaves are the gates. For a node `t`, let `E_t` be its leaf set and define its boundary

```text
partial(t) = V(E_t) intersect V(E-E_t).
```

For every consistent selection of one affine cell from each gate in `E_t`, existentially eliminate all variables outside `partial(t)`. Let `R_t` be the set of distinct nonempty affine residuals obtained.

### Leaf rule

For a leaf gate `g`, project each of its two affine cells onto `partial(g)` and deduplicate the resulting canonical affine systems.

### Join rule

If `t` has children `u` and `v`, then

```text
R_t = {
  project_partial(t)(A intersect B):
  A in R_u,
  B in R_v,
  A intersect B is nonempty
}.
```

The intersection is computed by adjoining the two canonical GF(2) equation bases and rejecting inconsistency.

### Exactness theorem

The join rule computes exactly the residual set obtained by direct enumeration of all cell choices in `E_t`.

### Proof

Proceed by induction on the branch tree. The leaf case is the definition. At an internal node, every cell choice on `E_t` splits uniquely into choices on `E_u` and `E_v`. By the induction hypothesis, their effects on variables visible outside each child are represented by members of `R_u` and `R_v`. Every variable shared between the two children is visible outside each child, so projecting inside the children loses no information needed for their conjunction. Conjoining and then projecting to `partial(t)` therefore gives exactly the direct residual. The reverse inclusion follows by combining the child cell choices witnessing each joined pair.

### State and running-time bound

If the maximum boundary size is `b`, every residual is a nonempty affine subspace of `GF(2)^b`. Hence

```text
|R_t| <= A(b)
```

at every node, where `A(b)` is the number of nonempty affine subspaces. Every internal node examines at most `A(b)^2` pairs, so a supplied decomposition supports an exact algorithm in

```text
O(m A(b)^2 poly(n))
```

time and `O(m A(b) poly(n))` explicit state storage.

## 5. Bounded-treewidth separation

Apply the private-vertex padding transformation to a tree `T`. The primal graph of the resulting three-uniform hypergraph replaces each tree edge by a triangle with a fresh degree-two vertex. It has a tree decomposition with one three-vertex bag per original edge, arranged along the tree, and therefore has treewidth at most two.

The padding preserves every edge-cut boundary, so

```text
q*(H_T) = linearwidth(T).
```

Perfect binary trees have unbounded pathwidth, while graph linearwidth and pathwidth differ by at most one outside the documented tiny exception. Thus this construction gives a simple three-uniform family with

```text
primal treewidth <= 2
```

and unbounded `q*`.

This proves that bounded treewidth does not imply bounded linear support width. It does not prove that the affine projected-DAG optimum `G*_proj` grows superpolynomially on the family.

## 6. Scope

The branch residual algorithm is a repository-local tree-shaped affine feasibility computation. No size-preserving equivalence to OBDD, FBDD, resolution, Res-Lin, communication complexity, or a standard circuit model is asserted. The NP-completeness result concerns ordering-width optimization, not Range Avoidance itself.
