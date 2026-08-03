# V88 theorem packet — collision normal form for repeated-table `Eval_H`

## Setup

Fix supports

```text
H=(S_1,...,S_m),  S_i subseteq [n],  |S_i|<=3,
```

and a list of target rows

```text
Y=(y^0,...,y^(k-1)) in ({0,1}^m)^k.
```

The list is **coverable** when there are witnesses `x^0,...,x^(k-1)` and local
truth tables `f_i` such that

```text
f_i(x^a restricted to S_i)=y^a_i
```

for every row `a` and output `i`. Equivalently, `Y` lies in the range of the
repeated-table evaluation map `Eval_H` from V85.

## Theorem 1 — collision normal form

Normalize the first witness to zero by replacing every witness `x^a` with
`x^a xor x^0`. For each input variable `v`, record the column pattern

```text
p_v=(x^1_v,...,x^(k-1)_v) in {0,1}^{k-1}.
```

Then `Y` is coverable if and only if there are patterns `p_1,...,p_n` such
that, for every output `i` and pair of rows `a<b`,

```text
y^a_i != y^b_i
```

implies that some variable `v in S_i` has different bits in rows `a` and `b`.

### Proof

If two rows have the same local address on `S_i`, a single truth table cannot
assign them different values. Therefore every differing target pair must be
separated on that support.

Conversely, assume all differing target pairs are separated. For a fixed
output `i`, assign the requested target bit to every local address observed
among the `k` witnesses. The separation condition guarantees that repeated
addresses never receive conflicting values. Extend this partial assignment
arbitrarily to the unobserved addresses. The outputs are independent, so these
extensions define all local truth tables. `QED`

## Corollary 2 — exact CSP formulation

For fixed `k`, coverability is a local CSP with:

```text
n variables;
alphabet size 2^(k-1);
at most m*binom(k,2) separation constraints;
each constraint reading at most three CSP variables.
```

This formulation exposes the repeated truth-table coordinates. Treating
`Eval_H` merely as an arbitrary `NC0_11` map discards this collision geometry.

## Corollary 3 — two rows never suffice

Every two-row target list is coverable.

Let `D` be the union of the supports on which the two target rows differ. Use
witness zero for the first row and the indicator of `D` for the second row.
Every differing output sees a nonzero local projection, so its two requested
values may be assigned independently. Equal outputs impose no conflict.

Thus an uncovered support-only list cannot be certified by a single target
pair. Any constructive obstruction must use consistency interactions among at
least three rows.

## Theorem 4 — three rows are a labeled hypergraph-coloring problem

For three rows, a variable pattern is one of

```text
00, 01, 10, 11.
```

The all-zero pattern never helps a separation constraint and may be replaced
by any nonzero pattern without destroying a previously satisfied constraint.
Hence three active colors suffice:

```text
color 0 = rows (0,1) equal;
color 1 = rows (0,2) equal;
color 2 = rows (1,2) equal.
```

Every nonconstant target column has a unique equal pair and therefore labels
its support by one of these three colors. A coloring covers the target list if
and only if no labeled support is monochromatic in a color different from its
label. Constant target columns impose no constraint.

This is an exact equivalence, not a relaxation.

## Theorem 5 — three rows need at least fifteen active outputs

For simple 3-uniform supports, every three-row target list with at most
fourteen nonconstant columns is coverable.

The full proof is in `THREE_ROW_BARRIER.md`. In bad-set language, one labeled
support excludes exactly a `2/27` fraction of all vertex three-colorings, and
any two distinct bad cylinders intersect in at least a `1/243` fraction. At
fourteen columns, a hypothetical cover would force the sum of pair
intersections to be simultaneously at least

```text
91 * 3^(n-5)
```

and at most

```text
63 * 3^(n-5),
```

a contradiction.

Therefore the first possible three-row obstruction has at least fifteen active
output columns.

## Theorem 6 — Property B rules out every three-row obstruction

If the support hypergraph is properly two-colorable, embed its two colors into
any two of the three active colors above. Every support remains
nonmonochromatic, so every three-row labeling is satisfiable.

`PROPERTY_B_BOUNDARY.md` combines this observation with the random-hypergraph
two-colorability theorem used there. The V87 target-stretch random model has
Property B with high probability, while its Hall, simplicity, and linear-width
events have the probabilities established in V86/V87. Consequently one family
simultaneously defeats the three earlier certificate mechanisms and still
covers every target list of at most three rows.

Thus, in the exact constructor model of ordered target lists depending only on
the supports,

```text
minimum universal list size >= 4.
```

## Finite censuses

The collision census enumerates all `15` nonempty simple ternary support
families on four variables and every target matrix with one, two, or three
rows. It checks `7,264` instances in total.

Two independent implementations compare:

1. direct extension of observed local truth-table addresses;
2. the normalized collision-pattern CSP;
3. for three rows, the labeled three-color formulation.

There are zero mismatches. Every target list in this smallest complete census
is coverable.

The extended audits check `1,710` labeled pairs of distinct supports on six
variables, all five moment-certificate scales from `n=5` through `n=9`, all
`2,187` labelings of the Fano support control, the three V80 support controls,
and eight deterministic V87 samples.

## Strategic consequence

The direct constructive question is now genuinely four-row:

```text
construct, from H alone, a four-or-more-row target matrix whose induced
separation CSP is unsatisfiable at m=n+ceil(n^(2/3));
```

or raise the lower bound for a precisely specified constructor class.

The Hall, syndrome, and width barriers do not imply even a three-row missing
output. Future work must use four-row collision geometry or support properties
that force failure of Property B while preserving the target stretch.

## Nonclaims

This normal form and its lower bounds do not construct the V85 counting list,
produce a four-row obstruction, derandomize the V87 family, solve unrestricted
`NC0_3-Avoid`, establish a circuit lower bound, or resolve `P` versus `NP`.
Novelty and peer-review status remain unconfirmed.
