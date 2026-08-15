# V101 core context — five residual ternary NPN orbits

## Starting point

V100 literal-substitution peeling removes every essential ternary gate whose
some fiber forces a constant literal or a copy/negation relation between two
inputs. Exactly 144 of 218 essential ternary truth tables are removed.

The residual NPN universe is only

```text
0x16   16 tables
0x17    8 tables   signed MAJ_3
0x1b   24 tables
0x1e   24 tables
0x69    2 tables   parity / complement
```

plus arbitrary outputs of locality at most two.

## Priority 1 — exploit stronger solvable relations without locality blowup

The V100 rule substitutes one variable by a unary literal of another variable.
For the residual orbits, inspect whether a selected fiber determines one input
by a two-input function. Such substitution normally raises a disjoint ternary
neighbor to locality four, so promotion requires an explicit structural
condition preventing that blowup or a controlled parameter measuring it.

`0x69` is the clean affine control: a parity fiber solves one input as XOR of
the other two. The obstacle is not solving the fiber; it is propagation into
neighboring ternary gates.

## Priority 2 — combine with V99 signed-majority obstruction

For `0x17`, V99 proves that a simple signed-majority X is useless in all three
nonzero switching classes because its edge map is surjective. V101 should seek
larger Turan structures or a way to localize switching defects before applying
the balanced V98 algorithm.

## Priority 3 — classify 0x16/0x1b/0x1e symbolically

Do not enumerate only finite circuits. Determine a reusable local relation,
transfer semigroup, polymorphism, or obstruction for at least one orbit.

## Stop rule

Promotion requires an infinite-family theorem: a safe elimination rule, a
polynomial/FPT constructor with a meaningful parameter, or an asymptotic
obstruction that closes a specified route. A truth-table census alone is not
enough.
