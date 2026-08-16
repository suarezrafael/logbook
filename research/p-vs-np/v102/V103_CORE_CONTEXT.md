# V103 core context — beyond logarithmic affine backdoors

## Starting point

V102 defines the strong affine backdoor number `beta(C)` and gives deterministic

```text
O(2^beta poly(N))
```

avoidance, with FPT backdoor detection for locality at most three. It handles both exact V101 residual orbits under one parameter and gives an exact-stretch pure-MUX family with `beta=1` while V97/V101 remain at `n`.

## The real remaining gap

Nothing in V102 prevents

```text
beta(C)=Theta(n).
```

A new version must attack this high-beta regime rather than refine the finite local classification.

## Track A — hybrid V101 + V102 compression

Allow some outputs to be handled by V101 functional anchors and condition only a small affine backdoor for the remaining cyclic/residual subsystem. Seek a combined parameter strictly below both `mu` and `beta` on an infinite family.

## Track B — residual high-beta obstruction

Construct explicit connected `0x17/0x1b` families with

```text
lambda=Theta(n),
mu=Theta(n),
beta=Theta(n)
```

at linear stretch. Then inspect their implication, switching, cycle-space, or separator structure for a fourth parameter that provably shrinks.

## Track C — approximate/backdoor-cover consequence

For residual gates, `0x1b` imposes selector-or-both-data constraints and `0x17` imposes two-of-three constraints on a backdoor. Determine whether positive surplus `m>n` forces a useful approximation, kernel, crown, or density decomposition for this mixed covering problem that can be converted into avoidance rather than merely finding `beta`.

## Stop rule

Do not promote V103 for a larger exhaustive search alone. Require one of:

- a hybrid parameter theorem with strict infinite-family separation;
- a scalable high-beta obstruction plus a rigorously smaller new invariant;
- a structural bound on `beta` for a nontrivial residual class that yields a new polynomial or subexponential avoidance regime.
