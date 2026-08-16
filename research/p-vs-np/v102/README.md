# Laboratory V102 — strong affine backdoors for the residual frontier

## Status

Candidate theorem package. Internally proved and checked by primary and independent verifiers. Not peer reviewed. Novelty and priority are not established. V102 does not solve unrestricted `NC0_3-Avoid`, does not improve the Huang--Li--Zhong all-instance worst-case exponent, and does not resolve P versus NP.

## Main theorem

Let

```text
C : {0,1}^n -> {0,1}^m,  m>n,
```

with output locality at most three. A set `B` of input variables is a **strong affine backdoor** when, for every assignment `sigma` to `B`, every restricted output gate is affine over `GF(2)` in the remaining variables.

Write

```text
beta(C) = minimum size of a strong affine backdoor.
```

Given a backdoor of size `beta`, V102 constructs an avoided output deterministically in

```text
O(2^beta poly(N)).
```

For locality at most three, a backdoor of size at most `k` can itself be found by a bounded search tree in

```text
O(3^k poly(N)).
```

Consequently `beta=O(log N)` is a deterministic polynomial-time range-avoidance regime.

## Why prefix counting becomes easy

For a prefix `p`, define

```text
M(p) = |{x : C(x) begins with p}|.
```

Fix one assignment `sigma` to the backdoor. Every restricted output is affine, so the condition that the first `|p|` output bits equal `p` is a linear system over `GF(2)`. Gaussian elimination gives the exact number of extensions in polynomial time. Summing over the `2^beta` assignments to `B` gives `M(p)` exactly.

Starting with the empty prefix, choose at each output coordinate the child with smaller preimage count:

```text
M(p b) <= M(p)/2.
```

Since `M(empty)=2^n` and `m>n`, after `m` choices

```text
M(y) <= 2^(n-m) < 1.
```

The count is integral, hence `M(y)=0` and `y` is outside the range.

## Exact residual-orbit rules

V101 left only two essential ternary NPN orbits without functional anchors.

### MUX / bijunctive orbit `0x1b`

Each of the 24 masks has a unique selector coordinate. Conditioning that selector makes both branches unary literals, hence affine. If the selector is not conditioned, both data coordinates must be conditioned to obtain a strong affine restriction.

Thus a pure `0x1b` circuit has an immediate backdoor consisting of its distinct selector variables.

### Signed majority orbit `0x17`

For each of the 8 masks, conditioning fewer than two support variables leaves a non-affine majority/AND/OR restriction for some branch. Conditioning any two support variables leaves at most a unary function.

Thus its exact local rule is

```text
|B intersect support(g)| >= 2.
```

V102 therefore gives one parameterized framework for both exact residual orbits.

## Strict separation family

For every `n>=5`, use variables

```text
x0, x1, ..., x_(n-1)
```

and let every output be canonical `0x1b` with selector `x0`. On the data vertices `x1,...,x_(n-1)`, take a cycle and add two distinct chords. Use one gate on each corresponding support

```text
(x0, xa, xb).
```

Then

```text
m=n+1,
beta=1.
```

The support component is connected and every input has degree at least two, so V97 performs no unused/leaf reduction and `lambda=n`. Every gate is a V100 residual hard `0x1b` gate, so V100 performs zero local graph peels. The orbit is functional-anchor-free, so V101 selects zero anchors and has `mu=n`.

Hence on this infinite exact-stretch family:

```text
V97:  2^n scale through lambda=n
V101: 2^n scale through mu=n
V102: 2^1 affine branches
```

This is a strict asymptotic parameter separation, not just a finite truth-table census.

## Validation

Primary verifier:

- all 24 `0x1b` masks checked for the exact selector/backdoor rule;
- all 8 `0x17` masks checked for the exact two-of-three rule;
- 600 seeded random pure-MUX circuits with exact prefix counts cross-checked against brute force;
- strict family checked through `n=10`;
- signed-majority control families checked through `n=9`.

Independent verifier:

- recomputes local affine degree using an ANF/Mobius transform;
- uses direct branch enumeration instead of Gaussian elimination;
- checks 240 fresh random MUX circuits;
- rechecks the strict family through `n=9`.

Both gates pass with zero failures.

## Literature boundary

The **backdoor-set paradigm is classical** in SAT/CSP: small strong backdoors into tractable classes are a standard parameterized method. V102 does not claim novelty for that concept. The range-avoidance step is the specialization that combines a strong affine backdoor with exact prefix preimage counting and the pigeonhole halving invariant.

Current range-avoidance literature still treats unrestricted `NC0_3-Avoid` as nontrivial; published algorithms include general high-stretch/local algorithms and special linear-stretch monotone algorithms. No source located in the V102 search explicitly states this `beta`-parameterized residual `0x17/0x1b` theorem, but absence from a targeted search is not evidence of novelty.

## Next frontier

V102 does **not** bound `beta(C)` in the worst case. The next version should attack one of:

1. prove a structural upper bound or approximation for `beta` on the residual `0x17/0x1b` mixtures;
2. combine V101 functional anchors with V102 affine backdoors so cyclic/non-affine dependencies can be compressed jointly;
3. build an explicit residual family with `lambda=mu=beta=Theta(n)` and identify a new invariant that shrinks it.
