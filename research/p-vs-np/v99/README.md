# Laboratory V99 — unbalanced singleton cores and signed-majority X dichotomy

V99 advances the V98 label frontier in both a constructive and a negative
direction.

## Constructive result

The 16 essential ternary truth tables in the singleton NPN orbit (AND/OR type
with arbitrary literal and output orientations) are now an unconditional
polynomial-time range-avoidance class for `m>n`.

Orient each local gate so that it has one satisfying assignment. If two gates
sharing a variable demand opposite values on that variable, target both oriented
outputs by one: no input can realize the target. If no conflict exists, every
variable has one globally consistent demanded polarity and input switching
turns the component into a positive-AND monotone circuit. The published
Kuntewar--Sarma monotone `NC0_3` algorithm then applies.

An exact-stretch connected family with cyclic triple supports plus one
conflicting duplicate has V97 `lambda=N`, minimum input degree at least three,
and fails the V98 switching-balance test, yet V99 produces an immediate missing
word. Thus this is a strict extension of the V98 tractable raw-label regime.

## Signed-majority X classification

For a simple Kuntewar--Sarma `X_{2 ell}` whose gates are majority of three
literals, the signed incidence graph has cycle rank two, so there are four
input/output switching classes.

V99 proves the exact dichotomy for every length:

```text
balanced class        -> exactly two missing edge words;
three nonzero classes -> the X edge map is surjective.
```

After switching the balanced case to all-positive MAJ, the two missing words
are the two alternating edge colorings used by the published majority argument.

The proof is constant-state rather than a finite cycle census. Private majority
edges reduce to two Boolean 2x2 transfer matrices; any nonalternating path
collapses to the universal endpoint relation, while an even alternating path
has only one forbidden endpoint pair. The whole X reduces to five boundary
variables and an exact constant table.

Therefore the simple loose-X/majority certificate cannot be extended to
unbalanced signed-majority labels merely by choosing a different edge coloring:
in the three nonzero switching classes every edge coloring is induced.

## Unate frontier after V99

The 72 essential ternary unate tables split into NPN orbit sizes

```text
16  singleton core       -- solved by V99,
48  x AND (y OR z) core  -- open,
 8  MAJ_3 core           -- balanced solved by V98; simple-X signed classes
                            exactly classified by V99.
```

The next laboratory should attack the 48-table middle orbit, preferably through
an implication-graph/transfer theorem rather than raw truth-table enumeration.

## Nonclaims

No all-unate `NC0_3-Avoid` algorithm, no unrestricted `NC0_3-Avoid` algorithm,
no improvement of the Huang--Li--Zhong worst-case exponent, no novelty or peer
review claim, and no P-versus-NP resolution.
