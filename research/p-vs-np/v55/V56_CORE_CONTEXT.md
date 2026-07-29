# Historical core context for Laboratory V56

> **Outcome recorded after V56.** The V55 conjectured improvement was achieved: arbitrary mixtures of affine-fiber gates are avoidable at minimum positive stretch `m>n`. The original `m>n+1` threshold below is therefore superseded, not retracted.

## Stable facts inherited from V55

1. The V53 girth implication and `Omega(log n)` family remain retracted.
2. V54 gives a degree-at-most-four separator for pure `AND3` positive stretch.
3. The 256 ternary functions form 14 NPN classes.
4. Eight classes have an affine output orientation.
5. Four affine classes are essential: `01`, `06`, `18`, `69`.
6. V55 proved mixed affine-fiber avoidance for `m>n+1` by augmented block-subspace redundancy.
7. V55 proved the antipodal-pair orbit `18` at stretch one.
8. The parity orbit `69` was already handled at stretch one by affine output rank.
9. The six essential non-affine classes are `07`, `16`, `17`, `19`, `1b`, and `1e`.
10. General stretch-one `NC0_3-Avoid` remains open.
11. Novelty and prior art for the block theorem are not externally confirmed.

## V56 outcome

V56 introduced a consistency-or-redundancy dichotomy:

- if all chosen active affine fibers are inconsistent, a minimal inconsistent subsystem directly gives an absent output;
- if they are consistent, translation by a common solution removes all affine right-hand sides and places the gate blocks in an `n`-dimensional coefficient space.

Consequences:

```text
all affine-fiber mixtures: m>n
0x06 distance-two orbit: m>n
arbitrary singleton polarities: m>n
separator degree: at most n+1
```

V56 also established that every fiber of the six remaining classes is the disjoint union of exactly two affine cells. Projection preserves affineness, so a single hidden-variable affine extension cannot represent those non-affine fibers.

## Frozen next direction

The classes `0x07`, `0x17`, and `0x1b` have bijunctive fibers on both sides. V57 therefore moves from affine equation blocks to implication-graph/2-CNF blocks, prioritizing `0x17` and its connection to signed-MAJ3 motifs.
