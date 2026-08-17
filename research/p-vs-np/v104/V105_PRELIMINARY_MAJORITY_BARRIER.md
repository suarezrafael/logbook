# V105 preliminary barrier — switching-unbalanced cyclic signed majority

This is a handoff result, not an official V105 candidate.

## Family

For every `n>=4`, let the inputs be `x_0,...,x_(n-1)`. Put one all-positive
majority gate on every cyclic length-three support

```text
E_i = {i,i+1,i+2} mod n.
```

On `E_0={0,1,2}`, add one extra signed-majority output in the same NPN orbit but
negate exactly the literal on `x_0`. This gives exact stretch `m=n+1` without
changing the support hypergraph.

The support is connected and every input belongs to at least three outputs.
All gates are essential signed-majority (`0x17` orbit) gates.

## Not switching-equivalent to the monotone case

V98 characterizes switching-balanced unate components by incidence equations

```text
d(e,v) = r_v XOR q_e,
```

where `d(e,v)` records whether gate `e` is decreasing in variable `v`.

For the all-positive gate on `E_0`, these equations force

```text
r_0 = r_1 = r_2 = q_base.
```

For the extra gate, whose `x_0` literal alone is negated, they force

```text
r_0 = 1 XOR q_extra,
r_1 = r_2 = q_extra,
```

and therefore `r_0 != r_1`. The two copies of the same support impose
contradictory switching requirements. Hence the component is **not**
switching-balanced and cannot be reduced to the published monotone case by the
V98 input/output coordinate flips.

This correction is essential: a globally switched all-positive majority cycle
would already be polynomial-time tractable through V98 and would not be a useful
residual barrier.

## Barrier theorem for V101 + V103 primitives

Every output fiber of every signed-majority gate is a balanced non-affine
four-point set. Its affine hull is the full cube `GF(2)^3`, so no target choice
contributes an affine-hull equation. V101's exact classification also shows that
the entire `0x17` NPN orbit has no functional anchor for either target value.

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

This is invariant under output ordering, head ordering, target polarity, and the
choice of affine block basis. Reordering the existing primitives cannot
penetrate this switching-unbalanced signed-majority family.

## Exact V102 strong-backdoor size

For any signed-majority gate, V102 proved that a strong affine backdoor must
condition at least two of its three support variables, and any two suffice. The
extra signed gate duplicates support `E_0`, so it does not change the support
condition. A global backdoor `B` therefore satisfies

```text
|B intersect E_i| >= 2
```

for every cyclic triple. Let `U=V\B`. Equivalently,

```text
|U intersect E_i| <= 1
```

for every `i`.

Any two vertices of `U` must have cyclic distance at least three. The disjoint
length-three arcs beginning at vertices of `U` give

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

A finite brute-force regression independently confirmed the formula for
`4<=n<=12` before this handoff was recorded.

## Previous parameters on the same family

Because the support is connected, all gates are essential, and every input has
degree at least three, V97 performs no unused/leaf/unary peel:

```text
lambda=n.
```

`0x17` is a V100 residual hard orbit, so V100 performs zero graph-fiber peels.
Because the full orbit is functional-anchor-free,

```text
mu=n.
```

Because both fibers of every signed-majority gate have full affine hull,

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

The family also explicitly fails the V98 switching-balanced test, so this
linear-parameter obstruction is not merely a disguised monotone instance.

## Consequence for V105

The next advance needs a genuinely new operation for switching-unbalanced signed
majority. A tempting idea is to condition a one-hit support set, because fixing
one input reduces a majority gate to a binary AND/OR-type function with a proper
restricted canonical hull. However independently solving each conditioned branch
does **not** construct a word missing from the union of all branches. The branch
composition theorem is the missing mathematical step.

V105 should therefore either:

1. construct one globally fixed missing output using branch-conditioned affine
   information;
2. prove a hardness barrier for that branch-composition primitive; or
3. introduce a non-affine majority-native certificate.

No P-versus-NP consequence follows from this barrier alone.
