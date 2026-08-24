# V114 scientific status

## Classification

**Barrier.**

V114 does not add a new positive algorithm for the `Delta>0` regime.  It proves that one natural continuation of V113 — guess a small set of extra shared gates and solve arbitrary completion by generic flow — already contains a classical NP-complete directed-linkage problem at one extra shared gate.

## Proved internally

For a fixed opposite-phase signed-MUX first pair, the decision problem asking for a target-compatible pair of gate-simple return routes with exactly one shared return gate and opposite branch bits at that gate is NP-complete.

The reduction:

- is polynomial in the directed `2-DDP` input size;
- uses valid essential ternary MUX gates;
- forces exact positive stretch `m=n+1`;
- preserves the existing V109--V113 target construction semantics; and
- includes a disjoint compatible bypass, proving the hard shared gate is extra non-dominator overlap rather than a common dominator.

## Why the result is a barrier rather than `Delta` hardness

Every reduction instance has a compatible zero-overlap pair.  Therefore its V113 parameter satisfies

```text
Delta = 0.
```

The theorem concerns the difficulty of selecting an **additional** compatible one-gate overlap, not the difficulty of repairing an instance whose entire optimum face is incompatible.

Accordingly, V114 does not establish NP-hardness for `Delta=1`, para-NP-hardness in `Delta`, W-hardness, or the failure of all possible FPT approaches.

## Redirected program

The generic arbitrary-waypoint branch oracle is closed.  The next positive attempt must use information absent from the reduction, especially the structure of a V113 rejection certificate over the minimum-overlap dominator-chain DP.

Promising next parameters are conflict locality, the number or structure of cyclic SCCs inside the rejected dominator interval, directed feedback-set size, or a bounded candidate set forced by a minimum phase conflict.

A separate negative route remains to strengthen V114 by inserting a phase-conflict gadget so the reduction itself has `Delta>0`.  That stronger hardness statement is not currently proved.

## External validation

The source hardness theorem is classical directed `2-DDP` NP-completeness due to Fortune, Hopcroft, and Wyllie.  The MUX-specific reduction and its exact-stretch padding have not received external mathematical review.

## Global boundary

V114 does not prove all MUX `0x1b` circuits are in P, does not solve unrestricted `NC0_3-Avoid`, does not establish a general circuit lower bound, and does not resolve P versus NP.
