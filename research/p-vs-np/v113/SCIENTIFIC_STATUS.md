# V113 scientific status

## What is proved in this candidate

1. For a fixed opposite-phase repeated-selector first pair, the minimum number of shared return output gates equals the number of common gate dominators.
2. Those common dominators form a source-to-sink chain after adding a super-source for the two return origins.
3. Every minimum-overlap pair shares exactly those common dominators and decomposes into gate-disjoint intervals between consecutive dominators.
4. A four-state dynamic program over the branch pair at each common dominator decides whether any minimum-overlap pair is target-compatible.
5. An accepted DP witness constructs a missing output word by the arbitrary-compatible-overlap lemma inherited from V111.
6. Scanning every repeated-selector output pair and opposite-phase first-branch choice remains polynomial.
7. The nonserial `k=3` strict family has `n=7(d+1)`, `m=n+1`, minimum overlap `d`, mixed compatible/incompatible optima, and exact V102 backdoor `beta=5(d+1)=5n/7`.

## What is independently checked

The independent verifier imports no V113 implementation. It separately:

- enumerates gate-simple return paths on small random signed-MUX instances;
- computes common dominators by gate deletion;
- checks `minimum overlap = number of common dominators` on the enumerated cases;
- reconstructs the nonserial strict family;
- checks explicit compatible and incompatible optimum pairs;
- verifies the compatible target with its own signed-MUX 2-SAT SCC solver through depth 100;
- checks Hall matching controls through depth 30;
- checks the exact depth-one V102 backdoor value.

These computations are falsification controls; the general theorem rests on the dominator/max-flow proof, not on finite enumeration.

## Prior-art discipline

Dominators and their efficient computation are classical graph-algorithm material. Two-unit gate-disjoint feasibility via node splitting and max-flow is also standard. V113 makes no novelty claim for those ingredients.

The project-specific claim is the composition: common-dominator decomposition of the minimum-overlap MUX return-flow face plus a four-state target-phase DP that is complete over all optimum decompositions for a fixed first pair.

A targeted search performed in August 2026 did not identify an explicit published statement of this exact range-avoidance theorem. Absence from that search is not evidence of novelty; expert review is still required.

## Remaining barrier

V113 solves only the `Delta=0` regime,

```text
Delta = minimum_target_compatible_overlap - minimum_overlap.
```

If every minimum-overlap pair is target-incompatible but a compatible pair exists after deliberately sharing additional non-dominator gates, V113 can reject even though a valid double-cycle certificate exists.

The next laboratory must attack `Delta>0` directly or prove a structural reason that a compatible optimum always exists in a broad residual class.

## Global status

- all essential MUX/bijunctive `0x1b` circuits in P: **not proved**;
- unrestricted `NC0_3-Avoid` in P: **not proved**;
- new general circuit lower bound: **not proved**;
- P versus NP: **unresolved**;
- novelty confirmed: **no**;
- peer reviewed: **no**.
