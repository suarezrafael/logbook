# V99 core context — signed-majority cohomology and the remaining unate orbit

## Starting point

V98 proves a polynomial subclass inside the V97 large-kernel regime.

For an essential unate gate, record one incidence bit `d(e,v)` indicating
increasing/decreasing orientation. If

```text
d(e,v)=r_v XOR q_e
```

globally, input/output switching turns the component into monotone `NC0_3`, so
the Kuntewar--Sarma `m>n` algorithm applies.

V98 also proves that loose-X support alone is insufficient for arbitrary labels:
a parity-labeled loose X is surjective, even when embedded into an exact-stretch
V97-irreducible host.

## V99 discovery pretest

The 72 essential ternary unate truth tables split into exactly three NPN orbits:

```text
singleton core (AND/OR type):       16 tables,
three-satisfying core x&(y|z):       48 tables,
majority core MAJ_3:                  8 tables.
```

Two symbolic targets emerged before opening V99.

### Target A — singleton-core completion

Orient each singleton-core gate by an output complement so that it has exactly
one satisfying local assignment. Then it is a conjunction of three literals.
If two such gates sharing an input demand opposite values on that input, setting
both oriented target outputs to one gives an immediate missing word. If no such
conflict exists, every input has one globally consistent demanded polarity;
input switching makes every gate a positive AND, and the published monotone
`NC0_3` algorithm applies.

V99 should formalize the resulting candidate theorem:

> Every positive-surplus component whose essential ternary gates lie in the
> singleton NPN orbit admits deterministic polynomial-time range avoidance,
> whether or not its V98 incidence-sign cochain is balanced.

A strict irreducible family is available from cyclic triple supports plus a
duplicate support whose singleton demand disagrees on one shared input. It has
`lambda=N`, minimum input degree at least three, and is not V98-switching-balanced.

### Target B — exact signed-MAJ loose-X dichotomy

For a simple `X_{2 ell}` labeled by majority-of-three literals, input/output
switching acts exactly as switching of a signed incidence graph. Its incidence
graph has cycle rank two, hence four switching classes.

A constant-state 2-SAT/transfer reduction gives the following candidate
all-length classification:

```text
trivial/balanced class: exactly two missing edge words,
                         the two alternating words after output switching;
each nonzero class:      the edge map is surjective.
```

The asymptotic step is not a length census. Private majority edges reduce to
2-by-2 Boolean path matrices

```text
R0 = [[1,1],[1,0]],
R1 = [[0,1],[1,1]].
```

Any equal adjacent target bits make the path relation universal; a strictly
alternating even path has only one forbidden endpoint pair. The whole `X`
therefore collapses to two path relations and five boundary variables. The
remaining constant boundary table has two failures only in the balanced class
and none in the three nonzero switching classes.

This would exactly explain why the Kuntewar--Sarma alternating coloring works
for ordinary MAJ labels and why an unbalanced signed-MAJ loose X can fail as a
local avoidance certificate as strongly as possible.

## Residual unate frontier after Targets A/B

If both targets survive independent verification, the only essential ternary
unate NPN orbit not structurally classified by the laboratory is the 48-table
orbit represented by

```text
x AND (y OR z)
```

up to NPN equivalence. Each fixed output fiber of this gate is bijunctive, which
suggests an implication-graph/transfer formulation, but fixed-target 2-SAT
membership alone is not a missing-word constructor.

## Genuinely non-unate ternary labels

There are 218 essential ternary tables in total, so 146 are non-unate. Future
work should operate modulo NPN equivalence rather than raw truth tables and seek
symbolic transfer recurrences or scalable obstructions, not finite censuses.

Parity/XOR remains an algebraically easy control and should not be mistaken for
a hardness example.

## External-calibration rule

Signed-graph switching and the characterization of balanced signatures as those
switching to all-positive are classical (Harary/Zaslavsky territory). V99 must
not claim that language as new. The potentially research-specific object is the
exact interaction between those switching classes and the range of the
Kuntewar--Sarma `X_{2 ell}` majority map.

The 12 August 2026 Brakensiek reply also weakens novelty expectations for generic
polynomial linear-dependence arguments by connecting them to CSP sparsification
folklore. Do not return to that route without a consequence not already
explained by linear algebra/sparsification.

## Stop rule

No finite census may be promoted. V99 requires at least one symbolic theorem
valid for an infinite family. The preferred promotion package is:

- singleton-core unbalanced-unate polynomial avoidance; and
- the all-length signed-MAJ `X_{2 ell}` switching-class dichotomy.

The unrestricted Huang--Li--Zhong benchmark remains unchanged.
