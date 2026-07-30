# Translating V57 into standard 2-CNF irredundancy terminology

## 1. Standard clause redundancy

For a CNF formula `F` regarded as a set of clauses, a clause `c in F` is redundant when

```text
F \ {c} entails c.
```

Equivalently, deleting `c` leaves the same model set. A CNF is clause-irredundant when none of its clauses is redundant. An irredundant equivalent subset (IES) of `F` is an equivalent subset that is clause-irredundant.

These notions are established prior art. In particular, Liberatore studies redundancy and IESs for general CNF and specifically for 2-CNF.

## 2. Block redundancy used in V57

The Range-Avoidance instance supplies one local fiber per output gate. Each fiber is represented by a constant-size 2-CNF block `B_i`. V57 calls block `i` redundant when

```text
conjunction_{j != i} B_j entails B_i.
```

This is grouped-clause redundancy: the removable unit is a complete gate block, not an arbitrary individual clause.

A family is completely block-irredundant when deleting any complete `B_i` strictly enlarges the model set.

## 3. Explicit gadget

The five blocks are

```text
B1 = ¬x0 ∧ (¬x1 ∨  x2)
B2 = ¬x0 ∧ ( x1 ∨ ¬x2)
B3 = ¬x0 ∧ (¬x1 ∨  x3)
B4 = ¬x0 ∧ ( x1 ∨ ¬x3)
B5 = ¬x0 ∧ (¬x2 ∨ ¬x3).
```

Every block contains the common unit clause `¬x0`. After duplicate clauses are collapsed, the conjunction is the six-clause 2-CNF

```text
F = {
  ¬x0,
  ¬x1 ∨  x2,
   x1 ∨ ¬x2,
  ¬x1 ∨  x3,
   x1 ∨ ¬x3,
  ¬x2 ∨ ¬x3
}.
```

Its unique model is `0000`.

## 4. Clause-level statement

The six-clause set `F` is clause-irredundant:

- deleting `¬x0` permits the assignment `1000`;
- deleting any binary clause permits an assignment that violates exactly that binary clause while satisfying the other five unique clauses.

Thus `F` is itself an IES of its own theory.

## 5. Block-level statement

Deleting a complete block leaves four copies of `¬x0`, so the common unit remains enforced. The only logically new loss is the block's binary clause. Since each of the five binary clauses is essential relative to the other clauses and `¬x0`, every complete block is essential.

Therefore the V57 gadget is simultaneously:

1. a clause-irredundant 2-CNF after duplicate removal;
2. a completely irredundant partition into five gate-fiber blocks;
3. an orbit-constrained circuit-image construction.

## 6. What is special and what is not

Not special to V57:

- clause redundancy;
- IES terminology;
- implication-graph entailment checks;
- the existence of irredundant 2-CNF formulas.

The repository-specific structure is:

- each block is a selected three-point fiber of an essential ternary gate;
- all gates belong to the same NPN orbit, represented by `0x07`;
- the instance has `n=4`, `m=5`, the minimum positive stretch;
- exhaustive normalized search gives 12 families forming one variable-isomorphism class;
- no corresponding `n=3,m=4` instance exists in the searched universe;
- direct sums give an infinite stretch-one family.

The exact prior-art status of this constrained construction remains unresolved.

## 7. Recommended manuscript language

Use:

> We give a completely block-irredundant family of five 2-CNF gate fibers from one ternary NPN orbit. After duplicate clauses are removed, the conjunction is a clause-irredundant 2-CNF; the contribution claimed here is the circuit-image and orbit constraint, not the general notion of 2-CNF irredundancy.

Do not use:

> We introduce irredundant 2-CNF formulas.
