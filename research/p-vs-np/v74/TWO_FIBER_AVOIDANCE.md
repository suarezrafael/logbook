# Exact two-fiber counting and bounded-width avoidance

## 1. Gate model

A gate has a support of arity at most three, a truth-table mask, and an explicit output-polarity bit. Local coordinate `j` is the bit attached to `support[j]`. The effective truth table is the stored mask, complemented when `output_flip=1`.

For each output bit `a in {0,1}`, the fiber `f^{-1}(a)` is represented as an exact **pairwise-disjoint** union of affine cells. Internal cell choices and output bits are now separate objects: the target output bit selects a fiber, while a cell branch selects one affine piece inside that fiber.

## 2. Three-cell theorem for ternary fibers

**Theorem.** Every subset of `GF(2)^3` is a disjoint union of at most three affine subspaces. Three cells are sometimes necessary.

**Proof.** Affine cells have sizes `1,2,4,8`. Sets of size at most six can be partitioned into at most three pairs and possibly one singleton, using fewer cells in the smaller cases. A seven-point set is the complement of one point. Choose an affine plane not containing the missing point; the remaining three points split into an affine pair and a singleton. The full cube is one affine cell. A seven-point set cannot be the disjoint union of at most two affine cells because seven is not the sum of at most two powers from `{1,2,4,8}`. Therefore the maximum is exactly three.

The implementation enumerates the 51 nonempty affine subspaces of `GF(2)^3` and returns a deterministic minimum disjoint partition. Across all 256 local subsets, the minimum-cell histogram is:

```text
0 cells:   1 subset
1 cell:   51 subsets
2 cells: 196 subsets
3 cells:   8 subsets
```

The eight worst cases are precisely the seven-point subsets.

## 3. Weighted residual invariant

Fix a binary branch decomposition of the output gates. For a node `t`, let `X_t` be the variables used below the node and let

```text
partial(t) = X_t intersect X_outside(t).
```

For every projected affine residual `A` on `partial(t)`, store an integer `mu_t(A)`. Its invariant is:

> for each boundary assignment in `A`, `mu_t(A)` equals the total number of assignments to `X_t - partial(t)` represented by the disjoint cell branches that project to `A`.

At a leaf, an affine cell `C` projects to `A`. Every point of `A` has exactly

```text
2^(dim(C)-dim(A))
```

preimages in `C`, so that value is added to `mu_t(A)`.

At a join with child residuals `A` and `B`, form the affine intersection `C=A intersect B`. If it is inconsistent, discard the pair. Otherwise project `C` to the parent residual `P(C)` and add

```text
mu_u(A) * mu_v(B) * 2^(dim(C)-dim(P(C)))
```

to the parent weight. Equal projected residuals add their weights.

Because the selected fiber cells of each gate are disjoint, different complete cell choices do not double-count an input. Uniform affine projection fibers prove the invariant by induction. At the root, the boundary is empty and

```text
mu_root(empty) = number of inputs mapped to the selected output word.
```

Unused input variables contribute the explicit factor `2^(n-|X_root|)`.

If the branch boundary has size at most `b`, there are at most `A(b)` residual keys at each node and at most `A(b)^2` residual pairs at a join. Counts are at most `2^n`, so their binary length is polynomial in `n`.

## 4. Constructing an avoided output

Let `C:{0,1}^n -> {0,1}^m` with `m>n`. For an output prefix `p`, let `N(p)` be the exact number of inputs whose circuit output starts with `p`. Gates outside the prefix are represented by the tautological full cube, so the same weighted branch DP computes `N(p)`.

Initially,

```text
N(empty)=2^n < 2^m.
```

Suppose a prefix of length `k` satisfies

```text
N(p) < 2^(m-k).
```

Exact fibers partition the parent condition, hence

```text
N(p0)+N(p1)=N(p).
```

At least one child has count below `2^(m-k-1)`. Choose such a child and continue. After `m` steps the completion capacity is one, so the maintained strict inequality gives `N(y)=0`. Thus `y` is outside the image.

A single count uses

```text
O(m A(b)^2 poly(n,m))
```

time on a supplied width-`b` branch decomposition. Recomputing for the `m` prefix decisions gives

```text
O(m^2 A(b)^2 poly(n,m))
```

time. This is a constructive bounded-branchwidth algorithm for arbitrary Boolean gates of fan-in at most three. It is not an unrestricted `NC0_3-Avoid` algorithm because the decomposition is supplied and `b` may grow with the instance.

## 5. A width-dependent bicriteria price bound

Let `C_B` be the minimum projected residual cost among orders whose frontier never exceeds `B`. In a prefix-feasible system, every nonterminal layer contains at least one residual. Therefore

```text
m <= G*_proj <= C_B <= m A(B),
```

and consequently

```text
C_B / G*_proj <= A(B).
```

This is a rigorous but coarse width-dependent bound. It is not a rank-only constant: bounded gate arity does not bound support frontier width.

## 6. A bounded-treewidth family with exact growing `G*_proj`

Let the primal graph be the path on variables `x_0,...,x_m`. Gate `i` is binary OR on `(x_i,x_{i+1})`, and select output one. Its positive fiber is

```text
{01,10,11} = {01,10} disjoint-union {11},
```

an affine XOR line plus a singleton.

**Theorem.** For `m>=2`, this family has primal treewidth one and

```text
G*_proj = 3m-3.
```

**Upper bound.** Process edges from one endpoint. The residual-layer profile is

```text
1, 2, 3, 3, ..., 3,
```

whose sum is `3m-3`.

**Lower bound.** Every one-edge proper subset has two residuals. Consider a proper processed subset containing at least two edges. If a processed path component has length at least two, explicit choices of XOR-line and singleton cells give at least three distinct residuals on an exposed endpoint: unconstrained, fixed zero, and fixed one. Otherwise there are at least two isolated processed edges; each contributes two residual alternatives and component factorisation gives at least four global residuals. Hence every later proper prefix has at least three residuals. Every order therefore costs at least

```text
1 + 2 + 3(m-2) = 3m-3.
```

This answers the V74 bounded-treewidth search with a nontrivial exact linear-growth family. It is not a superpolynomial lower bound and does not imply a lower bound in a standard branching-program or proof-system model.

## 7. Scientific boundary

The new result proves avoidance only when a branch decomposition of bounded support boundary is supplied. It does not provide a polynomial algorithm for finding an optimum decomposition, a uniform polynomial bound for unrestricted rank-three support hypergraphs, an all-orders superpolynomial lower bound, a size-preserving standard-model simulation, or a P-versus-NP consequence.
