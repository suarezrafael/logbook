# Laboratory V75 — symbolic prefix counting

## Status

Active draft laboratory. The statements below are proof targets and implementation specifications until the primary and independent verifiers are complete.

## Starting point

V74 counts the preimages of one full output or one output prefix by running a weighted affine-residual dynamic program on a supplied branch decomposition. Repeating the full dynamic program at every prefix step gives the current

```text
O(m^2 A(b)^2 poly(n,m))
```

target-search bound.

## Primary V75 direction

Build one monotone arithmetic circuit for the paired output generating polynomial

```text
P_C(u_1,v_1,...,u_m,v_m)
  = sum_{x in {0,1}^n} product_i z_{i,C_i(x)},
```

where `z_{i,0}=u_i` and `z_{i,1}=v_i`.

The intended properties are:

1. the coefficient of `product_i z_{i,y_i}` is exactly `|C^{-1}(y)|`;
2. a prefix count is obtained by assigning the selected variable to one, its opposite to zero, and both variables of every unfixed coordinate to one;
3. the weighted branch-residual recurrence constructs the arithmetic circuit without expanding its `2^m` coefficients;
4. the circuit has `O(m A(b)^2)` arithmetic size for a supplied width-`b` decomposition, apart from polynomial-time affine-basis operations;
5. dynamic reevaluation touches only the dependency cone above the changed output leaf.

## Candidate incremental bound

For a rooted supplied decomposition `T`, let `depth_T(i)` be the depth of output leaf `i`. The current proof target is

```text
O(A(b)^2 * (m + sum_i depth_T(i)) * poly(n,m)).
```

Therefore a balanced height-`O(log m)` decomposition would give

```text
O(m log(m) A(b)^2 poly(n,m)).
```

This is not yet an unconditional improvement: a supplied width-`b` decomposition may have linear height, and V75 has not yet proved that it can always be balanced without an unacceptable width increase.

## Parallel questions

- Can bounded-width branch decompositions be constructed or balanced with guarantees sufficient for the symbolic algorithm?
- Is the `A(B)` bicriteria price bound tight, or can the reachable residual catalogue replace the full affine-subspace catalogue?
- Can an exact arbitrary-fiber, bounded-treewidth family force superlinear `G*_proj` beyond the V74 OR-path value `3m-3`?
- Can the symbolic residual circuit be translated size-preservingly to an arithmetic branching program, tensor network, or junction-tree representation?

## Scientific boundary

V75 has not proved an unrestricted avoidance algorithm, a decomposition-construction theorem, a superpolynomial lower bound, a standard-model simulation, novelty, peer review, or any consequence for P versus NP.

Promotion requires quick, full, and LaTeX CI on the same final SHA, followed by a final-diff Copilot review with no unresolved actionable finding.
