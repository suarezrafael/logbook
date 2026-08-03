# V88 theorem packet — the fourteen-output barrier for three rows

## Setup

Use the exact three-row reduction from `COLLISION_NORMAL_FORM.md`. Every
nonconstant target column labels its simple ternary support by one of three
colors. A vertex coloring is valid when a support may be monochromatic only in
its own label.

For a labeled support `(S,c)`, let `B(S,c)` be the set of vertex three-colorings
that violate it. Thus a coloring lies in `B(S,c)` exactly when `S` is
monochromatic in one of the two colors different from `c`.

A three-row target matrix is uncoverable precisely when its bad sets cover all
`3^n` vertex colorings.

## Lemma 1 — one bad cylinder

For every ternary support,

```text
|B(S,c)| = 2 * 3^(n-3).
```

Choose one of the two forbidden monochromatic colors on the three support
vertices and color all remaining vertices freely.

Consequently, thirteen active target columns cannot be uncoverable, because

```text
13 * 2/27 < 1.
```

The first unresolved counting case is fourteen columns.

## Lemma 2 — intersections of distinct bad cylinders

Let `S` and `T` be distinct ternary supports.

- If `S` and `T` are disjoint, then

  ```text
  |B(S,c) intersect B(T,d)| = 4 * 3^(n-6).
  ```

- If they intersect, their monochromatic colors must agree on every shared
  vertex. The number of common forbidden colors is two when `c=d` and one
  when `c!=d`. Hence, with `r=|S intersect T|`,

  ```text
  |B(S,c) intersect B(T,d)|
    = (2 if c=d else 1) * 3^(n-(6-r)).
  ```

In every case,

```text
|B(S,c) intersect B(T,d)| >= 3^(n-5).
```

The minimum occurs when the supports meet in one vertex and have different
labels.

## Theorem 3 — fourteen active columns are still coverable

Every three-row target list on a simple 3-uniform support family with at most
fourteen nonconstant output columns is coverable.

### Proof

The cases with at most thirteen active columns follow from Lemma 1 and the
union bound. Assume that fourteen bad sets cover all colorings.

For a coloring `z`, let `r(z)` be the number of bad sets containing it. Since
the bad sets cover,

```text
r(z) >= 1.
```

The total incidence excess above a single cover is

```text
sum_z (r(z)-1)
 = 14 * 2 * 3^(n-3) - 3^n
 = 3^(n-3).
```

On the other hand, summing pair intersections gives

```text
sum_z binom(r(z),2).
```

Lemma 2 supplies the lower bound

```text
sum_z binom(r(z),2)
 >= binom(14,2) * 3^(n-5)
 = 91 * 3^(n-5).
```

Because `1 <= r(z) <= 14`,

```text
binom(r(z),2) <= 7 * (r(z)-1).
```

Therefore the same quantity is at most

```text
7 * 3^(n-3)
 = 63 * 3^(n-5),
```

contradicting `91 > 63`. `QED`

## Corollary 4 — first possible three-row obstruction size

Any uncoverable three-row target matrix on simple ternary supports needs at
least fifteen active output columns.

This is a structural lower bound on the number of target columns, not merely a
small-instance census.

## Corollary 5 — target-stretch finite scales

At

```text
m = n + ceil(n^(2/3)),
```

the theorem covers every simple ternary instance for `5 <= n <= 9`, where the
corresponding output counts are `8, 10, 11, 12, 14`.

The result is not asymptotic: for `n >= 10`, the target output count is already
at least fifteen.

## Property-B control

If the underlying support hypergraph is two-colorable, every three-row target
matrix is coverable: use two of the three active colors in a proper support
coloring. Every support is then nonmonochromatic, independently of its label.

Thus a three-row obstruction requires more than an arbitrary label assignment;
it must also live on a non-two-colorable support family.

The committed Fano-plane control checks all `3^7=2,187` labelings of its seven
supports. Every labeling is satisfiable. The number of satisfying vertex
colorings ranges from `1,238` to `1,317`.

## Constructive interpretation

When at most fourteen columns are active, only the variables contained in
those supports matter, so at most forty-two variables are relevant. Exhaustive
search over their three colors recovers a cover witness in

```text
O(3^(3m) * poly(n,m))
```

time. This is fixed-parameter constructive in the active output count, though
not intended as the asymptotic `Eval_H` algorithm sought by V88.

## Strategic consequence

The V88 search should no longer spend effort on two-row constructions, and a
three-row constructor must generate at least fifteen active columns. The next
useful questions are:

1. whether a fifteen-column labeled simple ternary obstruction exists;
2. whether additional intersection moments raise the lower bound;
3. whether four-row target matrices yield a cleaner target-stretch
   construction;
4. whether a restricted constructor model can be ruled out using this bad-set
   geometry.

## Nonclaims

This theorem does not construct the asymptotic support-only list, settle the
existence of a fifteen-column obstruction, solve unrestricted `NC0_3-Avoid`,
derandomize V87, produce rigid matrices, prove a circuit lower bound, establish
novelty or peer review, or resolve `P` versus `NP`.
