# Affine-cell branching model

For every selected non-affine gate fiber, choose a disjoint partition

```text
F_i = A_i^0 dot-union A_i^1,
```

where both cells are nonempty affine subsets of the input cube.

A partial branch fixes cells for some gates. Its feasible set is the intersection of the chosen cells.

## Leaf rules

1. **Inconsistency leaf.** The feasible set is empty. This is an affine inconsistency certificate.
2. **Affine completion leaf.** All gates are fixed and the feasible set is nonempty. The chosen cells form a consistent affine system, so V56 supplies a complete-block redundancy certificate because `m>n` in the target stretch-one experiments.
3. **Internal state.** At least one gate is unassigned and the feasible set is nonempty.

## Recorded finite parameters

`L_aff` is the leaf count of a tree minimizing, lexicographically, leaf count, internal-node count, and depth.

`D_aff` is the maximum root-to-leaf depth of that selected tree.

`G_aff` is the number of distinct residual states `(feasible input set, remaining gate indices)` reached by that same policy. It is not separately minimized over all DAG representations.

## Exact state compression

For complete `n=3` enumeration, a partial system is represented by its nonempty signature groups: inputs inducing the same cell-choice word. Future transitions depend only on those groups. Therefore merging histories with identical signature groups is exact, not heuristic.

## Boundary

A small leaf count on a finite cube does not prove an asymptotic polynomial bound. Conversely, a large syntactic branch space does not prove hardness because inconsistency and state merging may collapse it. V66 records both phenomena without choosing a general conjecture.
