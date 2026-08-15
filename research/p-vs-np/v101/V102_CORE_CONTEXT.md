# V102 core context — majority, mux, and cyclic functional dependencies

## Starting point

V100 locally removes five NPN orbits. V101 globally relaxes selected functional
fibers into an acyclic dependency DAG and reaches 186 of the 218 essential
ternary truth tables.

Only two essential ternary NPN orbits have **no functional anchor at all**:

```text
0x17    8 tables   signed MAJ_3,
0x1b   24 tables   mux/bijunctive selector.
```

## Track A — mux target selection

Canonical `0x1b` can be written

```text
(x0 AND NOT x2) OR (NOT x0 AND NOT x1),
```

so `x0` selects between two signed data bits. Both output fibers are 2-CNF and
produce two implication paths through the selector. Seek a polynomial target
constructor forcing a contradictory strongly connected component, or a
parameterized implication-cycle theorem with an explicit strict family.

## Track B — signed majority beyond simple X

V99 proves that the simple Kuntewar--Sarma `X_{2 ell}` is surjective in every
nonzero signed-majority switching class. Therefore V102 must use a larger
substructure, localize switching defects, or combine multiple X certificates;
changing only the edge target coloring cannot work.

## Track C — functional cycles

V101 requires an acyclic selected dependency system. For affine functional
relations such as XOR, cycles can instead be solved by Gaussian elimination.
Seek a hybrid semiring/constraint system that permits selected cycles for a
broader class of two-input functions without reverting to locality-four
composition.

## Stop rule

Promotion requires an infinite-family symbolic result: a missing-word
constructor, a meaningful FPT parameter with strict asymptotic separation, or a
scalable obstruction for one of these tracks. No local census alone.
