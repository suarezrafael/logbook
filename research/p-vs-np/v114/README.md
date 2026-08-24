# V114 — one-extra MUX overlap selection barrier

V114 attacks the `Delta>0` handoff left by V113.  The first generic idea in the frozen V114 context was to guess a small set `X` of extra shared non-dominator gates and then solve the resulting return-flow problem by a polynomial residual oracle.

V114 proves a barrier to that generic oracle.

## Main result

Define **ONE-EXTRA-OPPOSITE-COMPATIBLE-RETURN** for a fixed opposite-phase repeated-selector MUX first pair.  The question is whether there are two gate-simple return routes such that

- exactly one return gate is shared;
- the two routes use opposite MUX branches at that shared gate; and
- the two induced cycle target assignments agree on every shared output, hence construct a missing output by the inherited V111 arbitrary-overlap composition lemma.

V114 proves this problem NP-complete even on valid essential signed-MUX circuits with exact positive stretch

```text
m = n + 1,
```

and even though the same distinguished first pair has an explicit target-compatible **zero-overlap** return pair.

The reduction is from the classical two directed vertex-disjoint paths problem (`2-DDP`) of Fortune, Hopcroft, and Wyllie.

## Reduction idea

Given terminal pairs `(s1,t1)` and `(s2,t2)`, each logical graph vertex receives one mandatory MUX resource gate.  Every graph arc is represented by a selector-choice MUX whose only root-reaching branch is branch `0`.  A fresh waypoint gate `w` has two root-reaching branches:

```text
branch 0 -> encoded s2 suffix,
branch 1 -> private scaffold.
```

Route 0 can reach the waypoint only through an encoded `s1 -> t1` path and a unique `t1 -> w` connector.  Route 1 reaches the waypoint through a private prefix.

An exact-one shared pair using opposite branches must therefore share the waypoint and no graph resource.  Whichever route takes branch `0` supplies an encoded `s2 -> t2` suffix.  Gate simplicity or cross-route exact-one overlap forces the two encoded graph paths to be vertex-disjoint.  Conversely, two directed vertex-disjoint paths lift directly to a target-compatible exact-one shared MUX pair.

The waypoint signing is chosen so both opposite-branch traversals demand the same target bit.  All padding used to force `m=n+1` lies in a dead trap component and cannot create return routes.

## Why this matters for the V114 Track A plan

The reduction does **not** say that `Delta=1` is NP-hard.  In fact every reduction instance deliberately contains a private zero-overlap compatible bypass, so its unconstrained optimum is already compatible.

What it does prove is that the proposed generic branch oracle

```text
guess one extra shared gate / phase state
-> solve arbitrary completion by flow
```

cannot be justified in general.  Exact-one opposite-branch completion already contains directed two-disjoint paths.  Any successful `Delta`-FPT algorithm must exploit additional structure produced by **V113 optimum-face rejection**, rather than treating a guessed extra gate as an arbitrary waypoint.

## Verification

The primary verifier:

- executes the actual reduction;
- compares `96` seeded four-vertex reductions against direct `2-DDP` path enumeration;
- checks exact `m=n+1` padding and valid ternary MUX inputs;
- checks the explicit zero-overlap bypass;
- constructs a yes-certificate from two disjoint paths; and
- checks one generated missing target against the complete original circuit image.

The independent verifier imports no V114 code.  It separately implements the encoder, route census, target compatibility, and direct circuit semantics, and checks `128` seeded reductions plus four adversarial controls.

## Boundary

V114 is a **barrier**, not a polynomial avoidance theorem and not a `Delta`-hardness theorem.  It does not prove that the full fixed-pair compatible-overlap problem is NP-hard, that `Delta=1` is NP-hard, or that a conflict-conditioned FPT algorithm is impossible.

All-MUX `0x1b`, unrestricted `NC0_3-Avoid`, general circuit lower bounds, and P versus NP remain open.  No novelty, priority, or peer-review claim is made.
