# V114 theorem ledger — one-extra opposite-branch overlap barrier

## Problem definition

Fix a signed-MUX circuit, a root selector `r`, two distinct root outputs `g0,g1`, and first branches whose source phases are opposite.  Delete root-selector outputs from the return graph exactly as in V109--V113.

A **one-extra opposite-compatible return certificate** is a pair of gate-simple return routes from the two first destinations back to `r` such that:

1. exactly one return output gate is used by both routes;
2. the two routes use opposite branch bits at that shared MUX gate; and
3. the target bit required by the two implication cycles is identical on the shared gate.

Because no other output is shared, condition 3 is exactly the target-compatibility condition needed by the V111 arbitrary-overlap composition lemma.

Call the decision problem **ONE-EXTRA-OPPOSITE-COMPATIBLE-RETURN**.

## Theorem 1 — NP membership

ONE-EXTRA-OPPOSITE-COMPATIBLE-RETURN is in NP.

A certificate contains the two return routes.  Gate simplicity bounds each route length by the number of outputs.  In polynomial time one checks route continuity, return to the fixed root, exact one-gate overlap, opposite branch bits at the shared gate, and equality of the induced target requirement.  The full target word is then constructed by the same local implication rule used since V109.

## Theorem 2 — exact-stretch reduction from two directed disjoint paths

There is a polynomial-time many-one reduction from the classical two directed vertex-disjoint paths problem (`2-DDP`) to ONE-EXTRA-OPPOSITE-COMPATIBLE-RETURN.

Input to `2-DDP` is a digraph `D=(V,A)` with four distinct terminals

```text
(s1,t1), (s2,t2).
```

The output is an essential signed-MUX circuit with

```text
m = n + 1
```

and one fixed opposite-phase first pair.

### Construction

Create a fresh logical waypoint `w`.  For every original graph vertex `v`, create a variable `x_v`, a private choice variable `c_v` unless `v=t2`, and one mandatory vertex-resource MUX

```text
Q_v : x_v -> c_v | dead
```

with branch `0` the only branch that can remain in the return graph.  For `t2`, branch `0` goes directly to the root.

For every graph arc `(u,v)` with `u != t2`, create

```text
A_uv : c_u -> x_v | dead.
```

Add one unique connector

```text
A_t1w : c_t1 -> x_w | dead.
```

The fresh waypoint MUX is

```text
W : x_w -> x_s2 | private_after.
```

Both branches of `W` can return to the root.  Branch `0` enters the encoded `s2` suffix; branch `1` enters a private one-gate suffix.

The first pair at root has destinations `route0_start` and `route1_start`.  Their selected first branches have source phases `0` and `1`.  Route 0 has a private entry into `x_s1`; route 1 has a private entry into `x_w`.

Finally add a private route-0 bypass from `route0_start` to the root.  This bypass is disjoint from the route-1 scaffold and proves minimum overlap zero independently of the `2-DDP` instance.

All wrong branches lead to a trap component.  If the raw construction has too few outputs, duplicate essential MUX outputs entirely inside that trap.  If it has too many outputs relative to variables, add isolated unused variables.  In either case the final instance has exactly `m=n+1` and the padding creates no return path.

The construction has size `O(|V|+|A|)`.

## Lemma 3 — graph paths lift to one-extra compatible MUX routes

Suppose `D` has vertex-disjoint directed paths

```text
P1 : s1 -> t1,
P2 : s2 -> t2.
```

Route 0 takes its graph entry, follows the mandatory vertex and arc MUX gates encoding `P1`, uses the unique `t1 -> w` connector, traverses waypoint `W` on branch `0`, follows the encoded `P2`, and reaches the root through `Q_t2`.

Route 1 follows its private prefix to `W`, uses branch `1`, and follows its private suffix to the root.

The two return routes share exactly `W`.  Vertex-disjointness of `P1,P2` prevents repeated mandatory vertex gates inside route 0.  All graph-resource gates are private to route 0 and all scaffold gates are private to route 1.

The first gate after `W` on the graph branch is `Q_s2` branch `0`, whose source phase is zero.  The first gate after `W` on the private branch is also fixed to source phase zero.  With zero data polarities on `W`, both traversals therefore require the same target bit on `W`.

Thus the two cycles are target-compatible and construct a missing output.

## Lemma 4 — any exact-one opposite certificate extracts a `2-DDP` witness

Consider any valid one-extra opposite-compatible return certificate in a reduction instance.

Route 1 starts at a private variable with only one root-reaching choice: its private prefix into waypoint selector `x_w`.  Hence every route-1 return uses `W`.

Every ordinary graph vertex-resource gate and every graph arc gate has only branch `0` on any root-reaching return.  A pair sharing one of those gates cannot use opposite branch bits.  Therefore the unique shared gate of any valid certificate must be `W`.

The routes consequently use opposite branches of `W`.

To reach `W`, route 0 cannot take its private bypass.  The reduction structure forces it to alternate mandatory vertex gates and graph-arc gates from `s1`, and the only graph entry into `x_w` is the unique `t1 -> w` connector.  Its prefix therefore encodes a directed `s1 -> t1` path `P1`.

Whichever route takes branch `0` of `W` must then alternate mandatory vertex gates and graph-arc gates from `s2` until `Q_t2` reaches the root.  This gives a directed `s2 -> t2` path `P2`.

If the same return route contains both `P1` and `P2`, gate simplicity prevents reuse of any mandatory `Q_v`, so the graph paths are vertex-disjoint.  If the two graph portions lie on different return routes, exact one-gate overlap prevents them from sharing any mandatory `Q_v`.  Again `P1` and `P2` are vertex-disjoint.

Thus every accepting MUX certificate yields a `2-DDP` witness.

## Corollary 5 — NP-completeness

By Theorem 1 and Lemmas 3--4,

```text
ONE-EXTRA-OPPOSITE-COMPATIBLE-RETURN is NP-complete.
```

This holds on essential signed-MUX circuits with exact positive stretch `m=n+1`.

## Lemma 6 — the hard shared gate is extra, not a common dominator

The reduction includes a private route-0 bypass and a route-1 scaffold whose return-gate sets are disjoint.  They are target-compatible because they share no output gate.

Therefore

```text
minimum return-gate overlap = 0.
```

In particular, the waypoint `W` is not a common gate dominator.  The NP-hard selection asks whether the same first pair additionally admits a compatible pair using exactly one non-dominator shared gate with opposite branch bits.

## Corollary 7 — barrier to the generic guessed-X oracle

A generic V114 Track-A strategy of the form

```text
guess one extra shared non-dominator gate and its local branch state;
solve arbitrary completion in polynomial time
```

cannot be valid on unrestricted MUX return graphs unless `P=NP`: the residual completion already contains the NP-complete problem above at one extra shared gate.

The barrier applies to a generic branch oracle, not to every possible `Delta`-parameterized algorithm.  A successful FPT method may still exploit structural information available only after V113 proves that the complete optimum face is target-incompatible.

## Verification boundary

The proof of NP-hardness is the explicit reduction, not the finite census.  The primary verifier executes the reduction and compares seeded small instances to direct `2-DDP` enumeration.  The independent verifier reimplements the encoder, return enumeration, target compatibility, and circuit semantics without importing V114.

## Nonclaims

V114 does **not** prove:

- NP-hardness of deciding `Delta=1`;
- NP-hardness of unrestricted existence of any compatible return pair;
- impossibility of a conflict-conditioned FPT algorithm;
- all-MUX `0x1b` avoidance in P or outside P;
- unrestricted `NC0_3-Avoid`;
- a new general circuit lower bound; or
- P versus NP.

The reduction instances deliberately have `Delta=0` because of the private compatible bypass.  This is essential to the stated scope of the barrier.
