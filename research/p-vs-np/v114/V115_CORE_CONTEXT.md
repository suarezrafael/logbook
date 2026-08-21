# V115 frozen core context — conflict-conditioned excess overlap

## Inherited barrier

V113 completely decides target compatibility on the minimum-overlap face for every fixed opposite-phase MUX first pair.

V114 proves that a generic attempt to leave that face by guessing one arbitrary extra shared non-dominator gate and solving unrestricted completion is not a viable polynomial oracle in general.  ONE-EXTRA-OPPOSITE-COMPATIBLE-RETURN is NP-complete already at exactly one shared gate.

The V114 reduction deliberately has a compatible zero-overlap bypass.  Therefore it does **not** prove `Delta=1` hardness.

## V115 primary question

Can the fact that V113 rejected the **entire optimum face** force enough structure to make small positive `Delta` tractable?

The target remains

```text
Given a fixed first pair whose V113 optimum-face DP rejects,
decide target-compatible overlap <= minOverlap + k
in f(k) poly(N) time.
```

V115 must exploit a rejection certificate; arbitrary waypoint selection is frozen out by V114.

## Track A — minimal dominator-interval phase conflict

Instrument the V113 four-state DP so a rejection returns a smallest interval/state conflict rather than only `None`.

For each rejected transition record:

```text
previous common gate/state,
next common gate/state or final root,
first-gate phase pairs attempted,
minimum two-flow cuts blocking each compatible phase pair.
```

Question: does every `Delta=1` repair have to share a gate crossing one of a bounded number of these minimum conflict cuts?

A useful theorem would be a constant or parameter-bounded candidate set `S` satisfying

```text
any compatible +1-overlap repair shares some g in S.
```

This would evade V114 because its reduction has no V113 rejection.

## Track B — SCC localization of the hard interval

Compress each rejected dominator interval by strongly connected components after removing the common gates.

Directed two-linkage hardness requires cyclic interaction.  Test whether a rejection interval whose relevant SCC condensation has one of the following restrictions admits a polynomial repair algorithm:

- every cyclic SCC intersects only one side of the conflict cut;
- bounded number of cyclic SCCs;
- bounded directed feedback vertex set;
- the extra shared gate lies in an acyclic region.

Do not claim a DAG theorem without proving that gate-resource simplicity and target phase constraints survive the compression.

## Track C — strengthen the barrier to actual positive Delta

Try to compose the V114 reduction with a signed-MUX phase gadget such that:

1. every minimum-overlap pair is target-incompatible;
2. a compatible pair exists with one extra shared gate iff the source `2-DDP` instance is yes; and
3. exact positive stretch and essential ternary MUX semantics are preserved.

If successful, this would prove `Delta=1` NP-hardness and would close parameterization by `Delta` alone unless `P=NP`.

The current V114 bypass explicitly prevents this conclusion; it may not be silently removed without replacing the minimum-overlap analysis.

## Track D — finite discovery only

For small signed-MUX circuits where V113 rejects but a compatible higher-overlap pair exists, record:

```text
Delta,
rejected DP interval/state,
minimum conflict cuts,
location of every extra shared gate,
SCC membership,
whether the repair gate lies on a minimum route.
```

Use this census only to propose a structural lemma.  Larger tables alone are not promotable.

## Strict promotion rule

V115 is promotable only with at least one of:

- an FPT algorithm parameterized by `Delta`/budget `k` that explicitly uses V113 rejection structure and is not contradicted by V114;
- a polynomial theorem for all V113-rejected instances with `Delta<=1` under a clearly stated nontrivial structural class plus an infinite separation family;
- a correct reduction proving `Delta=1` NP-hardness on exact-stretch signed-MUX instances;
- a different externally recognized barrier that closes the conflict-conditioned route.

## Global boundary

Even a positive conflict-conditioned theorem does not solve all MUX `0x1b` unless its structural condition is shown universal.  Unrestricted `NC0_3-Avoid`, general circuit lower bounds, and P versus NP remain open.
