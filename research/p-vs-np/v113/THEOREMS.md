# V113 theorem ledger — common-dominator optimum-flow DP

## Setting

Fix two distinct signed MUX outputs `g0,g1` with the same selector `v` and choose first branches with opposite source phases. Let their branch destinations be `d0,d1`. Remove every output whose selector is `v` from the return graph. Split every remaining output gate `h` into a gate resource so that using `h` is the event counted as route overlap.

A return route starts at `di`, follows selected MUX branches, and ends at `v`.

## Definition 1 — common gate dominator

A return gate `h` is a **common gate dominator** for `(d0,d1;v)` when every `d0 -> v` return route and every `d1 -> v` return route uses `h`.

Equivalently, deleting `h` disconnects both `d0` and `d1` from `v`.

Let

```text
H = {h_1,...,h_d}.
```

The implementation detects these gates by repeated reachability. A standard dominator algorithm could replace this polynomial reference implementation.

## Lemma 2 — common dominators form one chain

Add a super-source `s` with arcs to `d0,d1`. A gate lies in `H` exactly when its gate-node dominates the sink `v` in this single flow graph. Dominators of a fixed vertex are the ancestors of that vertex in the dominator tree, hence are linearly ordered.

Therefore the common gates can be written in source-to-sink order

```text
h_1 < h_2 < ... < h_d.
```

V113 verifies the order constructively by reachability after deleting common gates and rejects if the expected nesting relation is not obtained.

## Lemma 3 — minimum overlap equals the number of common dominators

For the fixed first-branch pair,

```text
minimum number of return gates shared by the two routes = d = |H|.
```

### Lower bound

Every return route from either source uses every gate in `H`. Hence every pair of routes shares all `d` common dominators.

### Upper bound

Give each common gate capacity two and every other return gate capacity one. Variable vertices and ordinary transition arcs have capacity two. Add a super-source with one unit-capacity arc to each of `d0,d1`.

Suppose the maximum flow to `v` had value below two. By max-flow/min-cut there would be a cut of capacity at most one. A common gate cannot be such a cut because it has capacity two. A single source arc cannot disconnect the other source. Therefore a capacity-one cut would have to be a noncommon gate resource whose deletion disconnects every super-source-to-`v` route. That gate would be used by every route from both `d0` and `d1`, contradicting that it is noncommon.

Thus a two-flow exists. Integrality decomposes it into two return routes. Every noncommon gate has capacity one, so the routes share no noncommon gate. They share exactly the `d` common dominators.

Combining the bounds proves equality.

## Corollary 4 — optimum routes decompose into dominator intervals

Every minimum-overlap pair shares exactly `H` and no other return gate. Cutting the two routes at consecutive common dominators yields independent intervals in which the two local route pieces are gate-disjoint.

Conversely, choosing gate-disjoint local route pieces in every interval and choosing one branch for each route at each common gate stitches into a global minimum-overlap pair.

This is the structural reason the optimum-flow face can be searched without enumerating complete paths.

## Lemma 5 — four-state MUX phase transfer

At a common gate `h_j`, the only shared local choice is the pair of branch bits

```text
(b_0,b_1) in {0,1}^2.
```

Hence there are four states.

For a fixed current state and a fixed next state, target compatibility at `h_j` is determined by the source phases of the first selected output gates in the next interval. V113 enumerates those first output/branch choices for the two routes. After fixing them, the remaining question is only whether their tails can be completed gate-disjointly to the next dominator selector. That question is a two-unit integral max-flow with capacity one on noncommon gate resources.

If the next boundary is reached immediately, the required arrival phase is the next common-gate branch phase. At the final interval, it is the complement of the initial source phase, closing the contradiction cycle.

The enumeration is polynomial because there are at most `O(m^2)` pairs of first local gate/branch choices and only four current and four next states.

## Theorem 6 — complete polynomial algorithm for compatible optimum return pairs

For a fixed pair of opposite-phase initial MUX branches, V113 decides in deterministic polynomial time whether **some minimum-overlap pair of return routes is target-compatible on all shared gates**. If so, it constructs such routes and a full missing output word.

### Soundness

Accepted interval transitions use gate-disjoint noncommon gates. The global routes therefore share exactly the common dominators. At every common gate the DP explicitly requires equal target bits for both traversals. The V111 arbitrary-overlap composition lemma then gives a contradictory fixed-output 2-CNF, so the constructed output word is outside the circuit range.

### Completeness over the optimum face

Let an arbitrary target-compatible minimum-overlap pair exist. By Lemma 3 it shares exactly `H`. Its branch pair at every common dominator is one of the four DP states. In each interval, its first local branches witness one of the enumerated choices, and its remaining gate-disjoint tails witness the corresponding max-flow feasibility. Therefore every state transition of that optimum pair is present in the DP, so V113 accepts.

Thus V113 does not merely test one deterministic min-cost decomposition: it decides existence over the entire minimum-overlap face for the fixed first-branch pair.

## Corollary 7 — polynomial recognizer over all repeated selectors

Scanning all pairs of outputs sharing a selector and all four branch pairs is polynomial. Therefore V113 constructs a missing word whenever any such fixed pair admits a target-compatible minimum-overlap return pair.

The number of candidate first pairs is polynomial in the number of outputs; each candidate invokes only reachability, constant-state dynamic programming, and ordinary max-flow.

## Theorem 8 — nonserial strict family

For every `d>=1`, `strict_nonserial_optimum_family(d)` has

```text
n = 7(d+1),
m = n+1.
```

It uses two three-variable lobes per layer and `d` shared hub MUX gates. The support is not the `k=2` serial template recognized by V112.

For the distinguished first pair:

```text
minimum overlap = d.
```

The `d` shared hub gates are exactly the common dominators. Explicit route pairs show that the optimum face contains both:

- a target-compatible pair sharing exactly those `d` gates;
- a target-incompatible pair with the same overlap `d`.

Therefore ordinary overlap optimality still does not determine phase compatibility, but V113 searches the optimum face and finds the compatible pair.

The primary verifier checks the V113 constructor through depth 30 and the current V111 reference implementation as a finite rejection control through depth 20. The implementation-specific V111 rejection is not promoted to an all-depth theorem.

## Theorem 9 — exact V102 backdoor on the k=3 strict family

For the depth-`d` family,

```text
beta_V102 = 5(d+1) = 5n/7.
```

### Proof

Consider one three-variable lobe with variables `x0,x1,x2` and exit hub `z`. Its local V102 MUX conditions are cyclically

```text
xi in B OR (x_{i+1} in B AND z in B).
```

If `z` is selected, these reduce to the vertex-cover constraints of a triangle, requiring at least two of the three lobe variables; two suffice. If `z` is not selected, every selector `xi` is forced, so all three lobe variables are required.

Each layer has two lobes. Hence the two lobes cost at least four selected variables when the layer exit hub is selected and at least six otherwise. Including the hub itself gives layer cost at least five in the first case and six in the second. Summing over the `d+1` layer exit hubs gives

```text
beta >= 5(d+1).
```

Select every layer exit hub and any two variables from each three-variable lobe. All lobe constraints are then satisfied, while the central/shared hub MUX gates are satisfied by their selected selector hubs. This gives the matching upper bound.

Thus equality holds.

## Verification boundary

The primary verifier cross-checks V113 against exhaustive gate-simple path enumeration on random small signed-MUX instances. The independent verifier does not import V113; it independently enumerates paths, recomputes common dominators by deletion, reconstructs the strict family, and checks the produced good targets with an independent 2-SAT SCC engine.

Finite enumeration is a falsification layer, not the proof of the general theorem.

## Boundary

V113 solves compatibility **within the minimum-overlap face** for a fixed initial pair and scans all such pairs polynomially. It does not prove that some minimum-overlap compatible pair must exist in every MUX circuit. A circuit may require a target-compatible pair whose overlap exceeds the unconstrained minimum.

Define the next residual parameter

```text
Delta = minimum_target_compatible_overlap - minimum_overlap.
```

V113 settles the `Delta=0` case for every fixed opposite-phase first pair. The `Delta>0` case remains open.

Consequently V113 does not prove all essential MUX/bijunctive `0x1b` circuits are in P, does not solve unrestricted `NC0_3-Avoid`, does not establish a general circuit lower bound, and does not resolve P versus NP.
