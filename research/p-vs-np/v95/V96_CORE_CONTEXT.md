# V96 core context — comparison-free range avoidance

## Starting point

V95 closes the exact V92 canonical-halving route as a plausible generic
polynomial strategy: a fixed seven-type locality-three compiler at exact stretch
`M=N+1` has a genuinely canonical next bit encoding a PP-complete comparison.

The closure is policy-specific. It does not make the total search problem
`NC0_3-Avoid` PP-hard, because a solver may output any absent word.

## Mandatory front

V96 must construct or characterize a **different avoided-output policy** that
does not reproduce exact canonical child comparisons.

Allowed information primitives include:

```text
one-sided zero/nonzero tests,
structural certificates that force an empty fiber,
coarse multiplicative or additive estimates,
modular/parity information,
a polynomial-size target list with a guaranteed missing member,
local component decompositions that certify absence without global comparison.
```

Exact `N(p0)<=N(p1)` evaluation as the main engine is forbidden by the V95 stop
rule.

## Track A — certificate-triggered empty child

V93 preserved efficient zero detection on structured prefixes. Try to build a
policy that searches only for a **certified empty child**, rather than the
smaller child.

First theorem target:

> Find a structural condition, checkable without exact counting, under which a
> polynomially generated set of prefixes is guaranteed to contain one prefix
> with an empty child before depth `N+1`.

A finite census is not sufficient; the guarantee must scale asymptotically.

## Track B — polynomial target list

Instead of one canonical word, construct a list

```text
L(C) subset {0,1}^{N+1}
```

of polynomial size such that at least one member is absent from the range and
such that absence of a listed candidate is efficiently certifiable or the list
can be searched without exact child comparisons.

The list must be constructive. V88/V90 support-only existential lists do not
satisfy this requirement.

## Track C — coarse imbalance

Test whether exact child comparison can be replaced by a robust threshold:
choose a child only when a structural or approximate method certifies a
constant-factor imbalance, and branch/list on the remaining near-ties.

Promotion requires an end-to-end bound on the number of unresolved branches.
A local approximation result without a global avoidance guarantee is not
material progress.

## Runtime benchmark

Any algorithmic candidate must be compared with the published Huang-Li-Zhong
stretch-one bound

```text
O(N * 2^(N/2))
```

for `k=3`. A claimed improvement must include every branch/list/enumeration cost.

## First concrete lemma target

Prove or refute the following list-halving statement:

> There exists a polynomial-time rule that maintains at most `poly(N)` prefixes
> and, using only zero tests plus structural local information, advances them so
> that after `N+1` outputs at least one maintained prefix is empty.

Start with exact small-instance adversarial search only to discover invariants;
do not promote a finite pattern without a symbolic proof.

## Stop rule

If polynomial-size list halving requires exact comparison or grows
superpolynomially under an explicit family, record the obstruction and switch to
a structurally restricted branch where zero detection is composable. Do not
return to exact canonical-word evaluation.
