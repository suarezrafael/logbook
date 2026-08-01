# Bicriteria residual ordering and branch multiplicities

## 1. Budgeted projected-residual objective

For every processed gate set `S`, let:

```text
w(S)      = number of distinct nonempty projected affine residuals,
lambda(S) = support-frontier size.
```

For an order with prefix sets

```text
P_0 = empty, P_1, ..., P_m = E,
```

the repository convention is

```text
G_proj = sum_{i=0}^{m-1} w(P_i).
```

Fix a frontier budget `B`. Let `C_B(S)` be the minimum accumulated cost of an order of `S` whose every visited prefix has frontier at most `B`.

## 2. Exact bicriteria recurrence

```text
C_B(empty) = 0,
C_B(S) = min_{e in S} [ C_B(S-{e}) + w(S-{e}) ],
```

where a transition is permitted only when `lambda(S)<=B` and the predecessor is feasible.

### Correctness

Take an optimum feasible order of `S` and let `e` be its last gate. Removing `e` leaves a feasible order of `S-{e}`. The last transition contributes the layer `w(S-{e})`, so the optimum is at least the recurrence. Conversely, append `e` to an order attaining the predecessor optimum. The frontier condition on `S` makes the extension feasible and gives the matching upper bound.

After the exact tables `w(S)` and `lambda(S)` are available, the optimization uses `O(m 2^m)` transitions and `O(2^m)` stored costs. Computing the residual table remains exponential and is an audit algorithm, not an unrestricted polynomial algorithm.

## 3. Exact branch multiplicities

Let a binary tree have one gate at each leaf. At a node `t`, let `E_t` be its leaf set and let

```text
partial(t) = V(E_t) intersect V(E-E_t).
```

For each canonical residual `A` on `partial(t)`, store an integer `mu_t(A)` equal to the number of complete cell selections inside `E_t` whose conjunction is consistent and projects to `A`.

At a leaf, project each cell and add one to its residual. At a join with children `u,v`, inspect residual pairs. If `A intersect B` is consistent and projects to `R` on the parent boundary, add

```text
mu_u(A) * mu_v(B)
```

to `mu_t(R)`.

### Exactness

Each complete cell selection at an internal node splits uniquely into one selection in each child. Each child selection has exactly one canonical projected residual. Multiplication counts the Cartesian product of child selections; summation combines disjoint selections that project to the same parent residual. Induction on the tree proves exactness.

The state bound remains `A(b)` residuals at boundary size `b`. Counts may be exponentially large but require only `O(m)` bits when there are `m` binary cell choices.

## 4. What the DP can certify about avoidance

Suppose a target output word `y` is supplied and, for every gate `i`, the selected fiber

```text
f_i^{-1}(y_i)
```

is represented as an exact disjoint union of affine cells. A complete cell selection is consistent exactly when some input maps to `y`. Therefore:

```text
root multiplicity = 0  iff  y is outside the circuit image.
```

In that situation the already supplied `y` is an explicit avoidance witness. This is certification of a supplied target, not a search over target words.

## 5. Barrier in the current normalized schema

The V66–V72 normalized gate compiler represents the three-point positive fiber by two cells. For each partition type, cell zero contains the all-zero local assignment. Consequently the global all-zero input belongs to cell zero of every gate, for every normalized system.

Hence:

```text
root multiplicity >= 1
```

for every current normalized instance. The present schema therefore cannot itself return an avoided target and does not contain enough information to search over target output polarities. A constructive avoidance laboratory must encode both output fibers, their polarity, and exact affine decompositions or another exact representation.

## 6. Private-vertex binary-tree compression

Orient every tree edge from parent `p` to child `c`, introduce a private vertex `z`, and use the partition-zero gate on `(p,c,z)`:

```text
cell 0: p=0, c=0, z=0,
cell 1: p=0, c xor z=1.
```

Process edges in rooted postorder. Before an incoming edge is processed, every completed child subtree projects to the single condition that its top vertex is zero. Processing the incoming edge eliminates the private vertex and the completed child, leaving only the condition that the parent is zero. Thus every projected layer contains exactly one residual.

There are `m` nonterminal layers and every nonempty layer has at least one residual, so

```text
G*_proj = m.
```

V72 proved that the same support family has primal treewidth at most two and unbounded support linear width. Therefore support-width hardness does not lower-bound projected residual cost on this family.

For the tree-aligned branch decomposition, a bare edge to an unfinished internal child can have two residuals. Once joined with the completed child subtree, the residual collapses to the single parent-zero condition. Every internal branch node therefore has exactly one residual and every gate leaf has at most two.

## 7. Scope

These results do not prove an all-orders lower bound, unrestricted Range Avoidance, a simulation to OBDD/FBDD/resolution/Res-Lin, novelty, peer review, or a consequence for P versus NP.
