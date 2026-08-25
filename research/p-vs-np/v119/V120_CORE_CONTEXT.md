# V120 frozen core context — branch-image number after V119

## Inherited facts

V117 blocks generic FPT compression of the supplied-feedback two-chain graph-resource residual problem unless `FPT=W[1]`; this is not signed-MUX hardness.

V118 gives a signed-MUX exception for one exact clone bank per non-common V113 dominator stage.

V119 strictly enlarges that exception.  If a stage becomes acyclic after deleting the full bank

`B_D = { g : data0(g),data1(g) in D }`

for `|D|<=d`, destination loop erasure normalizes every private segment to at most `d` bank traversals.  With one extra shared gate, at most `4d+4` residual DAG requests remain.  Therefore fixed `d` gives an `N^{O(d)}` algorithm; in particular `d=2` is in P.

V119 also gives an exact-stretch `Delta=1` family with feedback-gate number tending to infinity and no single exact-clone deletion class exposing a DAG.

## New parameter

Let `d` be the minimum branch-image size needed so that, in every non-common stage, deleting `B_D` exposes a DAG.

The direct V119 algorithm is XP in `d`.  The frontier is whether signed-MUX structure compresses the `N^{O(d)}` representative choices to FPT, or whether hardness survives at bounded/small `d`.

## Track A — FPT in branch-image number

Seek `f(d) poly(N)` by replacing concrete bank-gate enumeration with a compressed interface.  Candidate tools:

- representative families over `(selector,destination,source-phase)` contacts;
- color coding / perfect hash families for the `O(d)` special traversals;
- important-separator or reachability-profile compression in the residual DAG;
- a type-level automaton that records only boundary phase and used destination states.

Promotion target: a rigorous FPT algorithm parameterized by `d`, with a scalable family separating the result from raw feedback-gate number.

## Track B — hardness at fixed small d

Attempt to realize the V117 generic two-chain barrier as an actual signed-MUX stage with branch-image size 3 or another fixed constant.

A valid reduction must preserve:

1. the V113 dominator decomposition;
2. opposite-phase repeated-selector first pair;
3. exact target compatibility semantics;
4. the budget-one overlap interpretation;
5. a fixed bound on branch-image size.

Promotion target: NP-hardness for a fixed constant `d`, or a parameterized hardness theorem for `d` under genuine signed-MUX constraints.

## Track C — several small branch-image banks

Let `c` be the minimum number of banks, each with image size at most two, whose union deletion makes the stage acyclic.

Test whether destination loop erasure plus a bank-level DP gives polynomial/FPT behavior for `c=2`, or whether interaction between banks recreates the V117 barrier.

Promotion target: a polynomial theorem for a nontrivial multi-bank class with an infinite separation family, or hardness already at a fixed small `c`.

## Track D — module/interface relaxation

Replace literal destination sets by a bounded number of equivalent boundary transfer states.  Candidate invariant: the number of distinct `(arrival-variable, source-phase)` states reachable after one cyclic module traversal.

Any relaxation must preserve the shared-boundary target argument; finite census alone is not promotable.

## Strict promotion rule

V120 is promotable with at least one of:

- FPT in branch-image number `d`;
- hardness for fixed/small `d` under signed-MUX constraints;
- a polynomial theorem for multiple bounded-image banks with an infinite strict separation family;
- a strictly larger module/interface theorem with proof and scalable separation;
- another structural barrier that decisively narrows the post-V119 frontier.

## Global boundary

No V120 result should be described as resolving unrestricted `0x1b`, `NC0_3-Avoid`, or P versus NP without a new explicit and externally validated bridge.
