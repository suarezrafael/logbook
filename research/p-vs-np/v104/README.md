# Laboratory V104 — hybrid functional-root rank compression

## Status

Experimental theorem package. The symbolic theorem and strict family are
recorded on an isolated branch while V102/V103 proceed through repository
promotion in order. V104 is not the official candidate. Novelty, priority, and
peer review are not established.

## Main result

V104 composes the two safe relaxations that survived the previous laboratories
without substituting nonlinear functions into neighboring gates:

1. V101-style functional target fibers are relaxed to total graph relations and
   organized as a distinct-head DAG.
2. After the DAG is fixed, selected V103-style affine-hull equations are allowed
   only when they involve the remaining DAG roots.

If the functional set has `f` heads and the independent affine root equations
have rank `R`, define

```text
eta = n - f - R.
```

Given such a hybrid certificate, V104 deterministically constructs a word
outside the range in

```text
O(2^eta poly(N)).
```

The certificate itself is polynomially checkable. Finding an optimal certificate
for an arbitrary circuit is explicitly left open.

## Why the counting is exact

The functional DAG leaves `n-f` root variables, and every root assignment has a
unique total-graph extension. The affine system has rank `R` entirely on those
roots, so exactly `2^(n-f-R)=2^eta` root assignments survive. Each retained
affine output block increases rank, so at most `R` affine output coordinates are
consumed. Since `m>n`, more than `eta` output coordinates remain. Enumerating the
hybrid relaxed domain and choosing a missing residual output therefore gives a
missing full output after restoring selected target bits.

## Strict exact-stretch family

For each `k>=1`, take `n=8k` inputs and `m=n+1` outputs.

The first `4k` variables carry a cyclic `0x1e` graph-of-OR block. Selecting
`4k-2` functional outputs leaves two roots. The second `4k` variables carry the
V103 `0x16` parity-hull block of rank `4k-1`. Add one majority output inside the
second block and one majority output crossing the blocks to make the support
connected and the stretch exactly one.

The explicit hybrid certificate has

```text
f   = 4k-2,
R   = 4k-1,
eta = 3.
```

Thus the relaxed domain always has eight assignments and four residual output
bits.

On this same family the preceding parameters remain large:

```text
lambda(V97) = 8k,
mu(V101)     = k+3,
beta(V102)   = Theta(k) with beta >= 3k,
nu(V103)     = 4k+1,
eta(V104)    = 3.
```

This is the intended material advance: a constant hybrid exponent on a connected
infinite family where each previous structural exponent is linear.

## Current verification state

The theorem was independently sanity-checked before registration on the first
two exact family instances:

- `k=1`: `n=8,m=9`, eight relaxed assignments, candidate checked against the
  complete original range;
- `k=2`: `n=16,m=17`, eight relaxed assignments, candidate checked against the
  complete original range;
- structural rank/connectivity identities checked through `k=20`.

The branch also contains primary and independent verifier programs with larger
randomized and structural gates. Those programs must pass repository CI before
V104 can become a candidate.

## Literature boundary

Current primary range-avoidance literature includes polynomial algorithms for
`NC0_2`, special monotone `NC0_3` regimes, general/local exponential algorithms,
and reductions connecting avoidance to explicit constructions and circuit lower
bounds. The targeted search performed for V103/V104 did not locate this exact
functional-DAG-plus-root-affine-rank certificate theorem. That is not evidence of
novelty, and no novelty claim is made.

## Nonclaims

V104 does not find the best hybrid certificate in polynomial time, does not put
unrestricted `NC0_3-Avoid` in P, does not improve the published unrestricted
worst-case exponent, and does not resolve P versus NP.
