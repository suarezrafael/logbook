# V89/V90 — exact obstructions to the 3-core peeling bridge

The eight-row affine construction requires a labeling of every variable by a
nonzero vector of `F_2^3` such that every ternary support receives a basis.
V90 briefly considered deriving this labeling from an empty 3-core. That
universal implication is false.

## Why the route looked plausible

For the binomial random 3-uniform hypergraph `H_3(n,d/n^2)`, the 3-core
threshold is

```text
d_3,3 = inf_{lambda>0} 2 lambda / Pr[Po(lambda)>=2]^2
      = 9.316979... .
```

Since the expected edge density is `d/6`, the corresponding threshold is

```text
m/n = 1.552829940... .
```

The V87 density tends to one, so its 3-core is empty with high probability.
However, an empty 3-core gives only a removal order in which every removed
vertex belongs to at most two active supports. It does not guarantee that the
two already colored vertices in each support have distinct labels, so reverse
extension can fail.

## Eight-vertex obstruction

Use vertices `0,...,7` and supports

```text
013  014  126  157  234
257  346  357  457  567
```

The committed peel certificate removes every vertex at active degree at most
two, so the 3-core is empty.

Assume a basis coloring exists. The five supports containing the pair `57`
force the labels of vertices `1,2,3,4,6` into the four-point affine coset outside
`span(label(5),label(7))`. Inside this coset, a triple is a basis exactly when
its three labels are distinct.

Write

```text
a=label(1), b=label(2), c=label(3), d=label(4), e=label(6).
```

The supports `126`, `234`, and `346` imply respectively

```text
(a,b,e), (b,c,d), (c,d,e) are pairwise distinct triples.
```

Thus `c,d` use two coset labels; `b,e` must be the other two labels and are
distinct; therefore `a`, being distinct from `b,e`, equals either `c` or `d`.
If `a=c`, support `013` repeats a label. If `a=d`, support `014` repeats a
label. Both alternatives contradict basis validity.

The executable audit independently normalizes `013` to labels `1,2,4` and
checks all

```text
7^5 = 16,807
```

remaining assignments, finding zero satisfying colorings. Every one-edge
deletion is colorable.

## Exact vertex minimality

Every empty-3-core hypergraph has a peeling order. Relabel that order as
`0,...,n-1`; each edge is then owned by its earliest vertex, and every owner has
load at most two. Colorability is inherited by deleting edges, so it suffices
to enumerate maximal load-two instances.

For seven vertices the final edge is always `456`. After normalizing it to the
standard basis, only `7^4=2,401` assignments remain. Bitset intersection over
all maximal owner choices checks exactly

```text
212,625
```

hypergraphs. All are basis-colorable. Hence the eight-vertex obstruction is
vertex-minimal in the empty-3-core class.

## Linear obstruction

The stronger hope that pair-codegree one might repair peeling is also false.
The following 12-vertex, 14-edge hypergraph is linear, has empty 3-core, and is
not basis-colorable:

```text
0,8,11   1,4,7    1,5,9    2,4,9    2,6,11
3,4,10   3,9,11   4,5,11   4,6,8    5,6,7
5,8,10   6,9,10   7,8,9    7,10,11
```

The exact CSP solver verifies unsatisfiability and colorability after deleting
any one edge. Pair-codegree is exactly one.

## Consequence for V90

The 3-core threshold remains relevant random-model information, but it cannot
be promoted into the eight-row theorem through a universal reverse-peeling
lemma, even under linearity. Any successful asymptotic bridge must use
additional random structure, a genuine seven-state second-moment argument, or
the strong-four Birkhoff inequality.

The fixed obstructions themselves occur with vanishing probability in the
sparse V87 model, so they do not prove that the random model is uncolorable.
They close only the unsupported universal peeling shortcut.
