# Support frontiers as linear branch-width

## 1. Support hypergraph and connectivity function

Let `H=(X,E)` be the support hypergraph of an affine-cell gate system. The vertices `X` are input variables and each gate contributes one hyperedge equal to its support. Parallel supports may be retained as distinct labelled hyperedges.

For $S \subseteq E$, write

```text
V(S) = union_{e in S} e,
lambda_H(S) = |V(S) intersect V(E \ S)|.
```

The function is symmetric and is the standard vertex-boundary connectivity function used by hypergraph branch decompositions.

For an edge order `pi=(e_1,...,e_m)`, let `S_i={e_1,...,e_i}` and

```text
q(pi) = max_i lambda_H(S_i).
```

The V70 support frontier satisfies `F(S)=V(S) intersect V(E\S)`, so `|F(S)|=lambda_H(S)` identically.

## 2. Exact vocabulary theorem

A linear branch decomposition is a branch decomposition whose decomposition tree is a caterpillar; equivalently, it is a linear order of the ground-set elements. Applied to the hyperedge ground set with connectivity `lambda_H`, its width is `q(pi)`. Consequently,

```text
q* = min_pi q(pi)
```

is exactly the linear branch-width of `H` under the vertex-boundary connectivity function. For rank-two hypergraphs (ordinary graphs), this is the classical linear-width edge-ordering parameter.

This is an exact change of vocabulary, not a new numerical inequality.

## 3. From an edge order to a primal path decomposition

Let the rank of `H` be at most `r`. Let `P(H)` be its primal graph: two variables are adjacent when they occur in a common support. Given `pi=(e_1,...,e_m)`, define

```text
B_i = F(S_{i-1}) union e_i.
```

Every primal edge lies in a support and hence in the bag assigned to that support. For each variable `x`, let `a` and `b` be the first and last positions of supports containing `x`. The variable appears in `B_a` and `B_b`, and for every `a<i<b` it lies in the frontier `F(S_{i-1})`. Thus the bags containing `x` form an interval.

Therefore `(B_1,...,B_m)` is a path decomposition and

```text
|B_i| <= q(pi)+r,
pw(P(H)) <= q(pi)+r-1.
```

Minimizing over `pi` gives

```text
pw(P(H)) <= q*+r-1.
```

## 4. From a primal path decomposition to an edge order

Let `(B_1,...,B_t)` be a path decomposition of `P(H)` of width `p`. Every hyperedge is a clique in the primal graph. The subpaths of bags containing its vertices pairwise intersect, so the interval Helly property gives a bag containing the whole hyperedge.

For each hyperedge `e`, let `rho(e)` be the rightmost bag containing all of `e`. Order hyperedges by nondecreasing `rho`, breaking ties deterministically.

At any cut in this order, let `x` be a frontier variable. A processed support containing `x` has a complete-support bag at or before the current `rho` value, while an unprocessed support containing `x` has one at or after that value. Since bags containing `x` form an interval, `x` belongs to the current bag. The same argument handles cuts inside one tie block because both complete supports lie in that tied bag.

Hence

```text
q(pi) <= max_i |B_i| <= p+1,
q* <= pw(P(H))+1.
```

Combining both directions:

```text
q* <= pw(P(H))+1,
pw(P(H)) <= q*+r-1.
```

For ternary supports, the additive gap is at most two in the second direction.

## 5. Constructive projected-DAG consequence

The rightmost-bag order is computed by scanning the decomposition and sorting labelled supports. Thus a supplied width-`p` path decomposition gives a gate order in polynomial time with `q(pi)<=p+1`.

V70 proves

```text
G_proj(pi) <= m A(q(pi)),
```

so V71 obtains

```text
G_proj(pi) <= m A(p+1).
```

This is an FPT-size construction parameterized by primal pathwidth. It does not show that unrestricted instances have small pathwidth.

## 6. Tree decomposition DP and its limitation

Let `(T,B)` be a tree decomposition of primal width `k`, converted to a nice decomposition. Assign each gate to a bag containing its whole support. A bottom-up DP stores, at each bag, the set of distinct nonempty affine residual subspaces on the bag variables induced by cell choices in the processed subtree.

- assigned gate: intersect each state with either affine cell;
- forget variable: existentially project that coordinate;
- introduce variable: add it unconstrained;
- join: intersect compatible child residuals and deduplicate.

There are at most `A(k+1)` possible nonempty affine residuals per bag. A direct join uses at most `A(k+1)^2` pairs, with polynomial-time Gaussian elimination in `k`. This gives an exact FPT feasibility DP for the affine-cell consistency problem.

It is not the linear projected residual DAG of V68–V70. Treewidth alone does not bound `q*`: graph trees have treewidth one while their pathwidth, and therefore linear-layout width, is unbounded.

## 7. Scientific boundary

The results establish a standard width interface and two parameterized algorithms. They do not prove a general polynomial good order, an all-orders lower bound, a simulation into a standard proof system, unrestricted `NC0_3-Avoid`, or a P-versus-NP consequence.
