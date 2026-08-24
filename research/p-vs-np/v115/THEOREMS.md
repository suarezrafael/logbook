# V115 theorem ledger — all-DAG-stage excess overlap one

## Setup

Fix a valid essential signed-MUX circuit and a prescribed pair of distinct first outputs at a common selector `r`. Fix branches whose selector source phases are opposite. Delete all outputs selected by `r` from the return graph, as in V109--V114.

Apply the V113 common gate-dominator decomposition to the two first destinations. Let

```text
H = (h_1,...,h_d)
```

be the ordered common gate dominators. V113 proves that every pair of return routes shares all gates of `H` and that the minimum possible return-gate overlap is exactly

```text
d = |H|.
```

The non-common return gates are partitioned into the `d+1` dominator stages between the first destinations, successive common dominators and the root selector.

For a stage, its **branch graph** has the stage variables as vertices and, for every allowed stage gate, the two directed selector-to-data branch arcs induced by that gate. The V115 structural class consists of fixed pairs for which every non-common stage branch graph is acyclic.

## Lemma 1 — unique-extra localization

If a pair of return routes has overlap at most `d+1`, then besides the mandatory common dominators it shares at most one non-common gate. Such a gate belongs to exactly one dominator stage.

This follows directly from the V113 stage partition and `minimum_overlap=d`.

## Lemma 2 — DAG prefix/suffix separation

Consider one acyclic stage and two gate-simple route segments that share exactly one stage gate `g`. Split each segment immediately before and immediately after its traversal of `g`.

No stage gate used by either prefix can be used by either suffix.

### Proof

Suppose a stage gate `q` were used before `g` by one route and after `g` by either route. The prefix gives a directed branch walk from the data destination reached after `q` onward to the selector of `g`; together with the arc through `q`, this yields directed reachability from `selector(q)` to `selector(g)`. The suffix begins with a branch of `g` and later reaches `selector(q)`, giving directed reachability from `selector(g)` back to `selector(q)`. Their concatenation contains a directed cycle in the stage branch graph, contradicting acyclicity. The same argument covers either choice of prefix route and suffix route. Therefore the prefix and suffix gate sets are disjoint except for the explicitly inserted gate `g`. QED.

## Lemma 3 — fixed extra-gate completion is polynomial in a DAG stage

Fix an acyclic stage, a candidate extra shared gate `g`, and the two branch choices used at `g`.

The existence of the required two prefixes from the stage starts to `selector(g)` is a two-unit integral flow problem with capacity one on every output gate other than `g`. The existence of the two suffixes from the chosen data destinations of `g` to the stage sink is another such flow problem. Both are solvable in polynomial time by vertex/gate splitting and ordinary max flow.

The local target requirement at the preceding common gate is checked from the source phase of each first prefix gate. The target requirement at `g` is checked from the source phase of each first suffix gate (or the next common gate / final closing phase when a suffix is empty). If the two requirements at each shared gate agree, the two flows may be concatenated. By Lemma 2 no hidden cross-prefix/suffix gate reuse can occur.

Thus a fixed `g` and fixed branch pair can be tested in polynomial time. Scanning all stage gates and four branch pairs remains polynomial.

## Lemma 4 — phase information remains finite-state

For a common dominator `h_j`, target compatibility depends only on the two chosen branches of `h_j` and the source phases of the first gates in the following segment, exactly as in the V113 segment transition.

When a unique extra gate is used inside a stage, its target compatibility is fully checked inside that stage by Lemma 3. No identity or phase information from that non-common gate is needed by later stages.

Therefore a dynamic program needs only:

```text
(branch of route 0 at the current common gate,
 branch of route 1 at the current common gate,
 whether the extra-overlap budget has been used)
```

plus witness paths for reconstruction. The state space is constant up to witness storage.

## Theorem 5 — polynomial budget-one decision on all-DAG stages

For every fixed opposite-phase first pair whose non-common dominator stages are all acyclic, there is a polynomial-time algorithm deciding whether a target-compatible return pair exists with

```text
overlap <= minimum_overlap + 1.
```

### Proof

Use V113 to compute `H`, the stage map and `d=|H|`. Process stages in dominator order. Ordinary transitions use the V113 gate-disjoint two-flow segment test. If the extra-overlap budget has not yet been used, additionally scan every candidate stage gate and its four branch pairs using Lemma 3. Keep the finite phase state of Lemma 4 and one budget bit. Lemma 1 proves that every feasible pair within budget is represented by either an ordinary transition in every stage or exactly one extra-gate transition in one stage. Lemma 2 proves that the latter transition is soundly composed from its independent prefix and suffix flows. Hence the DP is sound and complete for the stated class and runs in polynomial time. QED.

The implementation stores the chosen extra gate as witness metadata, but this does not enlarge the mathematical state needed for future transitions.

## Theorem 6 — exact-stretch infinite separation from V113

For every integer `t>=0`, `strict_dag_delta_one_family(t)` has

```text
n = 8+t,
m = 9+t = n+1.
```

For the designated opposite-phase first pair:

1. the unique common non-root gate dominator is `c`, so `minimum_overlap=1`;
2. every minimum-overlap route pair must leave `c` on opposite left/right continuations, whose immediate source phases force contradictory target bits at `c`, so the complete minimum-overlap face is target-incompatible;
3. a pair taking the left branch of `c` on both routes shares one additional gate `g`, then separates through two distinct exits; its target requirements agree at both `c` and `g`, so `minimum_target_compatible_overlap<=2`;
4. item 2 gives the matching lower bound, hence `minimum_target_compatible_overlap=2` and `Delta=1`;
5. subdividing the private route-0 prefix by `t` fresh selector variables adds one variable and one essential MUX per subdivision, preserves the overlap/phase argument, and keeps every non-common stage acyclic.

Thus V115 strictly extends the V113 optimum-face regime on an infinite exact-positive-stretch family.

## Literature boundary

The graph-level tractability of two disjoint directed paths on DAGs is prior art; in particular Tholey (2012) gives a linear-time algorithm for the DAG 2-disjoint-paths problem. General directed disjoint-path problems already exhibit NP-completeness at two terminal pairs through Fortune--Hopcroft--Wyllie (1980). V115 does not claim either graph result.

The internally proved contribution is the transfer of the all-DAG-stage condition through the V113 common-dominator/phase machinery with one excess-overlap budget and the exact-stretch signed-MUX separation family. Novelty relative to all circuit/range-avoidance literature remains unconfirmed.

## Nonclaims

V115 does **not** prove:

- tractability when a relevant non-common stage is cyclic;
- an FPT theorem parameterized only by unrestricted `Delta`;
- NP-hardness of `Delta=1`;
- all signed-MUX / bijunctive `0x1b` avoidance in P;
- unrestricted `NC0_3-Avoid` in P;
- a general circuit lower bound; or
- P versus NP.
