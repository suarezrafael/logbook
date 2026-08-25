# V119 frozen core context — multiple clone types after V118

## Inherited facts

V117 blocks generic FPT compression of a supplied feedback interface at the graph-resource level unless `FPT=W[1]`.

V118 identifies a signed-MUX exception: if each non-common dominator stage is a DAG after deleting one exact MUX-clone class, then `Delta<=1` is polynomial-time decidable even when the raw feedback-gate number is unbounded. The loop-erasure proof bounds a normalized route to at most two clones per segment because one exact clone class has only two branch types.

V118 also gives an exact-stretch family with `m=n+1`, `Delta=1`, and feedback-gate number `width -> infinity`.

## New parameter

Let `c` be the minimum number of exact signed-MUX clone classes whose deletion makes a non-common dominator stage acyclic.

The direct V118 normalization extends only to an XP bound: each route segment uses at most two representatives from each class, so naive enumeration gives `N^{O(c)}` behavior.

## Track A — FPT in clone-type count

Seek an `f(c) poly(N)` algorithm by compressing clone identities before the DAG linkage step. Candidate tools:

- representative families for interchangeable gate resources;
- color coding / perfect hash families for the `O(c)` special traversals;
- a type-level automaton carrying only branch and phase signatures;
- important-separator style compression of the residual DAG contacts.

Promotion target: a rigorous FPT algorithm parameterized by `c` with a scalable family separating it from raw feedback-gate number.

## Track B — hardness at small clone-type count

Attempt to realize the V117 two-chain barrier with two or three exact MUX clone classes. A successful parameter-preserving reduction for constant `c` would close Track A much more strongly than generic feedback hardness.

Promotion target: NP-hardness for a fixed constant `c`, or W[1]-hardness parameterized by `c`, under the actual signed-MUX phase/dominator constraints.

## Track C — stronger loop-erasure invariant

Test whether exact equality is unnecessarily strong. Candidate equivalence relations:

- same selector, branch destinations and branch source phases;
- same signed branch interface but different output flip compensated by target state;
- module-equivalent banks with the same two boundary transfer functions.

Any relaxation must preserve the shared-boundary target argument; same selector alone is not sufficient.

## Track D — finite discovery only

Enumerate small V118-rejected but repairable circuits and classify the minimum number of clone/interface types needed after dominator decomposition. Use this only to propose lemmas; finite census alone is not promotable.

## Strict promotion rule

V119 is promotable with at least one of:

- FPT in clone-type count `c`;
- hardness for fixed/small `c` under signed-MUX constraints;
- a polynomial theorem for a strictly larger phase-interface equivalence than exact cloning, with an infinite separation family;
- another structural barrier that decisively narrows the post-V118 frontier.

## Global boundary

No V119 result should be described as resolving unrestricted `NC0_3-Avoid` or P versus NP without an explicit, externally validated bridge.
