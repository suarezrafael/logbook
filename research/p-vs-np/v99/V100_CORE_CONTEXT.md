# V100 core context — the 48-table middle unate orbit

## Starting point

V99 would leave exactly one essential ternary unate NPN orbit structurally open:

```text
canonical representative: x AND (y OR z)
orbit size:               48 truth tables.
```

The singleton orbit (16 tables) has a polynomial avoidance theorem even outside
V98 switching balance. The majority orbit (8 tables) has V98's balanced
polynomial theorem and V99's exact simple-X switching obstruction.

## Key algebraic/logic feature

After local NPN normalization, a gate is

```text
f = a AND (b OR c)
```

on literals `a,b,c`. Both fixed output fibers are bijunctive:

```text
f=1:  a  AND (b OR c),
f=0:  (NOT a OR NOT b) AND (NOT a OR NOT c).
```

Thus for any *fixed* target word, range membership reduces to 2-SAT. This is
useful but not sufficient: a polynomial membership test does not automatically
construct one missing word among exponentially many targets.

## Preferred V100 track

Encode each target bit as a local switch between two constant-size implication
gadgets. Seek a structural theorem saying that positive support surplus forces a
target-selectable contradictory implication cycle.

Promotable outcomes include:

1. a polynomial constructor for the whole 48-table orbit;
2. an FPT constructor parameterized by a symbolic implication-defect parameter
   that is `o(lambda)` on an explicit irreducible family;
3. an all-length transfer obstruction proving that simple loose-X structures
   cannot solve a precisely specified subfamily.

## Stop rule

Do not promote fixed-target 2-SAT membership, a raw implication-graph census, or
small-cycle enumeration. The target bits themselves must be constructed or an
infinite-family obstruction proved.
