# Symbolic paired-variable prefix circuit

## 1. Exact generating polynomial

For a Boolean circuit `C:{0,1}^n -> {0,1}^m`, introduce two formal variables for every output coordinate:

```text
z_{i,0}=u_i,  z_{i,1}=v_i.
```

Define

```text
P_C(u,v) = sum_x product_i z_{i,C_i(x)}.
```

Every input contributes exactly one multilinear monomial. Consequently, for every output word `y`, the coefficient of

```text
product_i z_{i,y_i}
```

is exactly the preimage count `|C^{-1}(y)|`.

For a prefix `p` of length `k`, assign

```text
z_{i,p_i}=1 and z_{i,1-p_i}=0       for i<k,
z_{i,0}=z_{i,1}=1                   for i>=k.
```

The resulting value is the exact prefix count `N(p)`.

## 2. Weighted residual translation

Use the same exact disjoint affine-cell decompositions as V74.

At output leaf `i`, for each bit `c`, each affine cell in the exact fiber `C_i^{-1}(c)`, and each projected boundary residual `A`, create the contribution

```text
2^(dim(cell)-dim(A)) * z_{i,c}.
```

Contributions with the same projected residual are added.

At a join, combine every compatible child-residual pair. If the intersection residual projects to `A`, create

```text
left_expression * right_expression * 2^(dim(intersection)-dim(A)).
```

Again add expressions producing the same projected residual. At the root, multiply the empty-boundary expression by the explicit free-unused-input factor.

The recurrence uses only nonnegative integer constants, addition, and multiplication. It therefore constructs a monotone arithmetic circuit. Expanding this circuit gives `P_C`, but expansion is neither required nor permitted by the intended algorithm.

## 3. Size target

At a decomposition node with boundary width at most `b`, there are at most `A(b)` nonempty affine residual keys. A join examines at most `A(b)^2` compatible candidate pairs. Since the decomposition has `O(m)` nodes, the arithmetic circuit target size is

```text
S = O(m A(b)^2)
```

apart from the polynomial cost of canonical affine intersection and projection.

This is intended as a size-preserving translation of the V74 weighted residual object to a monotone arithmetic circuit. No translation to arithmetic branching programs, tensor networks, or junction trees is claimed yet.

## 4. Incremental evaluation

Store the current value of every arithmetic gate and reverse dependency edges from children to parents. Initially set all `u_i=v_i=1`, so the root value is `2^n`.

To test prefix child `p0`, change only `v_i` from one to zero and propagate recomputation through its reverse dependency cone. The other child count is

```text
N(p1)=N(p)-N(p0),
```

because the two exact fibers partition the parent prefix. If bit one is selected, restore `v_i=1`, set `u_i=0`, and propagate those changes. The selected assignment is then retained for the next step.

Let `D_T(i)` be the number of arithmetic gates reachable from the paired variables of leaf `i`. A complete target-search path uses

```text
O(S + sum_i D_T(i))
```

arithmetic reevaluations. The branch recurrence gives the coarse bound

```text
D_T(i)=O(A(b)^2 depth_T(i)).
```

Hence the candidate total is

```text
O(A(b)^2 (m + sum_i depth_T(i)) poly(n,m)).
```

For height `h`, this is `O(m h A(b)^2 poly(n,m))`. A balanced supplied tree gives `h=O(log m)` and improves the V74 repeated-DP bound to `O(m log m A(b)^2 poly(n,m))`.

## 5. Current obstruction

The result is depth-sensitive. A caterpillar decomposition can have total leaf depth `Theta(m^2)`, so local incremental reevaluation alone does not improve the worst-case V74 asymptotic bound. V75 must either:

1. prove a balancing transformation with controlled boundary-width inflation;
2. find a more global evaluation schedule whose cost is independent of external path length; or
3. state the improvement only for balanced or low-external-path-length supplied decompositions.

## 6. Required verification

- compare every symbolic coefficient against brute-force output counts on exhaustive small circuits;
- compare every prefix evaluation against V74 `prefix_count`;
- verify dynamic updates against full fresh arithmetic-circuit evaluation after every changed variable;
- count arithmetic gates and affected dependency cones;
- exercise balanced and caterpillar decompositions separately;
- implement an independent semantic verifier that does not import the primary arithmetic-circuit builder.

## 7. Nonclaims

This document is an active proof design, not a promoted theorem. It does not establish unrestricted `NC0_3-Avoid`, automatic bounded-width decomposition construction, a general balancing theorem, a standard proof-system simulation, novelty, or a P-versus-NP consequence.
