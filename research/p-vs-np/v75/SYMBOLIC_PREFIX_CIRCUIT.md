# Symbolic paired-variable prefix circuit

## Status

The statements in Sections 1–5 are internally verified by the primary and independent V75 checkers. They remain unreviewed research results. The literature observations in Section 7 are context, not novelty claims.

## 1. Paired generating polynomial theorem

Let `C:{0,1}^n -> {0,1}^m` be represented by fan-in-at-most-three Boolean output gates. Introduce two formal variables for every output coordinate:

```text
z_{i,0}=u_i,  z_{i,1}=v_i.
```

Define

```text
P_C(u,v) = sum_x product_i z_{i,C_i(x)}.
```

### Theorem — exact paired generating polynomial

For every output word `y`, the coefficient of

```text
product_i z_{i,y_i}
```

in `P_C` is exactly `|C^{-1}(y)|`.

For a prefix `p` of length `k`, assign

```text
z_{i,p_i}=1 and z_{i,1-p_i}=0       for i<k,
z_{i,0}=z_{i,1}=1                   for i>=k.
```

The evaluated value is the exact prefix count `N(p)`.

The coefficient statement follows directly because each input contributes one monomial encoding its complete output. The prefix statement follows because the substitution retains exactly the monomials whose first `k` output bits equal `p`.

## 2. Monotone residual-circuit translation

Use the exact pairwise-disjoint affine-cell decompositions of both gate fibers from V74. For a branch-tree node `t`, let `B_t` be its support boundary. For every nonempty projected affine residual `A` on `B_t`, construct an arithmetic expression `Q_t(A)`.

### Leaf recurrence

For output leaf `i`, bit `c`, and affine cell `F` in the exact fiber `C_i^{-1}(c)`, let `A` be the projection of `F` to the leaf boundary. Add

```text
2^(dim(F)-dim(A)) * z_{i,c}
```

to `Q_i(A)`.

### Join recurrence

For children `u,v`, combine each compatible residual pair `A in R_u`, `B in R_v`. Let `J=A intersect B` and let `P(J)` be its projection to the parent boundary. Add

```text
Q_u(A) * Q_v(B) * 2^(dim(J)-dim(P(J)))
```

to `Q_t(P(J))`.

At the root, multiply the empty-boundary expression by `2^r`, where `r` is the number of input variables unused by every output gate.

### Proof invariant

For every node `t`, residual `A`, subtree output word `y_t`, and boundary assignment satisfying `A`, the coefficient of the monomial selected by `y_t` in `Q_t(A)` is the number of compatible assignments to variables internal to `t` per such boundary assignment.

At a leaf, affine projection has a uniform fiber of size `2^(dim(F)-dim(A))`. Exact fiber cells are disjoint, so additions do not double count. At a join, child internal choices are independent after conditioning on compatible shared-boundary assignments; intersection enforces consistency and the projection factor counts eliminated assignments uniformly. Induction proves the invariant. The root has an empty boundary, so its coefficients are exact global preimage counts.

Only nonnegative integer constants, addition, and multiplication are used. The result is therefore a monotone arithmetic circuit. Its `2^m` coefficients are never expanded.

## 3. Arithmetic size

Let `A(b)` be the number of nonempty affine subspaces of `GF(2)^b`. If every branch node has boundary size at most `b`, then it has at most `A(b)` residual keys. Every join examines at most `A(b)^2` child pairs. A binary tree with `m` leaves has `O(m)` nodes, and each accepted pair creates only constantly many multiplication/addition operations. Therefore

```text
S = O(m A(b)^2)
```

apart from the polynomial cost of canonical affine intersection and projection.

This is a size bound for the repository-local monotone arithmetic DAG. V75 does not claim an equivalent arithmetic branching program, tensor network, OBDD, FBDD, resolution, or Res-Lin representation.

## 4. Incremental prefix evaluation

Store each arithmetic gate value and reverse edges from children to parents. Initially set every paired variable to one; the root equals `2^n`.

At output coordinate `i`, temporarily change `v_i` from one to zero. The new root is `N(p0)`. Exact fiber partition gives

```text
N(p1)=N(p)-N(p0).
```

Choose a child whose count is smaller than its remaining output-completion capacity. If bit one is selected, restore `v_i=1` and set `u_i=0` in one batch. Retain the selected assignment and continue.

Let `D_T(i)` be the number of arithmetic operation nodes reachable from either paired variable of output `i`. Each coordinate causes at most two dependency-cone reevaluations. Including the initial full evaluation, a complete search path costs

```text
O(S + sum_i D_T(i))
```

arithmetic reevaluations.

Only arithmetic nodes created at the leaf and its ancestors can depend on that leaf's paired variables. Each ancestor contributes at most `O(A(b)^2)` operations. Hence

```text
D_T(i)=O(A(b)^2 depth_T(i)).
```

and the total bound is

```text
O(A(b)^2 (m + sum_i depth_T(i)) poly(n,m)).
```

## 5. Balanced supplied decomposition corollary

If the supplied branch tree has height `h`, then

```text
sum_i depth_T(i) <= m h.
```

Thus the prefix-search runtime is

```text
O(m h A(b)^2 poly(n,m)).
```

For `h=O(log m)`, this becomes

```text
O(m log(m) A(b)^2 poly(n,m)).
```

which improves the V74 repeated-DP bound by a factor of approximately `m/log m` at the level of the parameterized asymptotic expression.

The qualification is essential. A caterpillar tree can have height `m-1` and external path length `Theta(m^2)`. For 64 leaves, the verified balanced tree has height `6` and external path length `384`, while the verified caterpillar has height `63` and external path length `2,079`. Therefore V75 does not remove the depth obstruction for an arbitrary supplied width-`b` decomposition.

## 6. Computational evidence

The primary verifier constructs one arithmetic DAG per circuit and checks all coefficients and prefixes against direct Boolean enumeration. It also compares every incremental update against a fresh topological evaluation.

The independent verifier does not import the arithmetic builder, affine residual code, or primary generator. It reconstructs gate semantics directly from support, truth mask, and output polarity; enumerates all inputs; repeats the prefix pigeonhole search; regenerates the seeded circuit family; and verifies the balanced/caterpillar depth identities.

The frozen totals are documented in `EXHAUSTIVE_RESULTS.md` and `RESULTS.json`.

## 7. Literature boundary and next structural question

Korhonen and Oum's 2026 result gives an FPT algorithm for finding width-`k` branch decompositions of general oracle connectivity functions. Applied to the support-boundary connectivity function, it materially weakens the earlier decomposition-construction obstruction in the parameterized setting. It does not by itself guarantee a logarithmic-depth decomposition, so it does not remove the depth obstruction proved visible by V75.

Bodlaender's logarithmic-depth transformation for graph tree decompositions permits width inflation to `3k+2`. V75 does not prove that this graph-tree-decomposition result transfers to the gate branch decomposition needed by the symbolic residual circuit with a controlled support-boundary width. Establishing such a transfer, or proving a direct balanced branch-decomposition theorem for the support connectivity function, is the primary V76 target.

References used only for scope:

- H. L. Bodlaender, *NC-Algorithms for Graphs with Small Treewidth*, WG 1988/1989.
- T. Korhonen and S.-i. Oum, *Branch-width of connectivity functions is fixed-parameter tractable*, arXiv:2601.04756, 2026.

## 8. Nonclaims

V75 does not establish automatic width-preserving balancing, unrestricted `NC0_3-Avoid`, a polynomial algorithm for arbitrary instances, a superpolynomial lower bound, a standard-model simulation, novelty, priority, peer review, or any consequence for P versus NP.
