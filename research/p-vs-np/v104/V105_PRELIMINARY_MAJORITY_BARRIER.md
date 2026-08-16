# V105 preliminary barrier — cyclic signed majority

This is a handoff result, not an official V105 candidate.

## Family

For every `n>=4`, let the inputs be `x_0,...,x_(n-1)`. Put a canonical `0x17`
majority gate on every cyclic length-three support

```text
E_i = {i,i+1,i+2} mod n
```

and duplicate one output to obtain exact stretch `m=n+1`.

The support hypergraph is connected and every input belongs to at least three
output supports.

## Barrier theorem for V101 + V103 primitives

Both output fibers of signed majority are balanced non-affine four-point sets.
Their affine hull is the full cube `GF(2)^3`, so no target choice contributes an
affine-hull equation. V101's exact classification also shows that `0x17` has no
functional anchor for either target value.

Therefore for **every** hybrid certificate using only:

- V101 total functional-graph relaxations, and
- V103 affine-hull equations,

we necessarily have

```text
f=0,
R=0,
eta_* = n.
```

In particular the V104 canonical affine-first parameter satisfies

```text
eta_AF=n.
```

This is invariant under output ordering, head-ordering, target polarity, and the
choice of affine block basis. Reordering the existing primitives cannot
penetrate pure signed majority.

## Exact V102 strong-backdoor size

For a majority gate, V102 proved that a strong affine backdoor must condition at
least two of its three support variables, and any two suffice. Hence a global
backdoor `B` for the cyclic family satisfies

```text
|B intersect E_i| >= 2
```

for every cyclic triple. Let `U=V\B`. Equivalently,

```text
|U intersect E_i| <= 1
```

for every `i`.

Any two vertices of `U` must therefore have cyclic distance at least three.
Partitioning the cycle into the arcs beginning at vertices of `U` gives

```text
3|U| <= n,
```

so `|U|<=floor(n/3)`. The bound is attained by

```text
U={0,3,6,...,3(floor(n/3)-1)}.
```

Thus

```text
beta = n-floor(n/3) = ceil(2n/3).
```

A finite brute-force regression independently confirmed this formula for
`4<=n<=12` before the handoff was recorded.

## Previous parameters on the same family

Because the support is connected, all gates are essential, and every input has
degree at least three, V97 performs no unused/leaf/unary peel:

```text
lambda=n.
```

`0x17` is a V100 residual hard orbit, so V100 performs zero graph-fiber peels.
Because it is functional-anchor-free,

```text
mu=n.
```

Because both canonical fibers have full affine hull,

```text
nu=n.
```

Together:

```text
V97:  lambda = n,
V101: mu     = n,
V102: beta   = ceil(2n/3),
V103: nu     = n,
V104: eta_AF = n.
```

## Consequence for V105

The next advance needs a genuinely new operation for signed majority. A tempting
idea is to condition a one-hit support set, because fixing one input reduces a
majority gate to a binary AND/OR-type function with a proper restricted
canonical hull. However independently solving each conditioned branch does
**not** construct a word missing from the union of all branches. The branch
composition theorem is the missing mathematical step.

V105 should therefore either:

1. construct one globally fixed missing output using branch-conditioned affine
   information;
2. prove a hardness barrier for that branch-composition primitive; or
3. introduce a non-affine majority-native certificate.

No P-versus-NP consequence follows from this barrier alone.
