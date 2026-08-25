# V119 theorem ledger

All statements below concern one fixed opposite-phase signed-MUX first pair after the V113 common-dominator decomposition.

## Definition — bounded branch-image bank

For one non-common stage with allowed output gates `A` and a set of variables `D`, let

`B_D = { g in A : data0(g) in D and data1(g) in D }`.

The stage is **d-image-reducible** when there exists `D` with `|D| <= d` such that deleting every gate in `B_D` leaves a DAG.

No equality of selectors, polarities, output flips, or exact MUX signatures is required inside `B_D`.

## Lemma 1 — destination loop erasure

Let `P` be a gate-simple route segment whose interior contains no gate shared with the other return route.  Suppose two bank traversals `e_i,e_j in B_D`, with `i<j`, both arrive at the same variable `v in D`.

Delete the subwalk strictly after the first arrival at `v` through and including `e_j`.  The suffix after `e_j` begins at the same variable `v`, so it can be attached directly after `e_i`.  The resulting route segment:

1. has the same endpoints;
2. remains gate-simple;
3. preserves the first traversal of the segment;
4. therefore preserves the source phase seen by the preceding shared boundary;
5. changes target requirements only on private gates removed or retained inside the segment.

Repeating the operation gives a normalized segment with at most one bank arrival per variable of `D`, hence at most `|D|` bank gates.

## Lemma 2 — budget-one interface bound

If a return-pair witness has at most one extra shared gate `q` beyond the V113 common dominators, then `q` partitions each route in the containing stage into at most two private segments.

After Lemma 1, each route uses at most `2d` bank gates plus `q`.  Removing `B_D` and `q` leaves at most

`4d + 4`

source-target connector requests in the residual DAG.

Only the first traversal after a shared boundary can constrain the target bit of that shared gate.  Thus phase constraints are carried by the concrete enumerated bank/extra traversals and by the first traversal of the corresponding residual DAG request.

## Lemma 3 — fixed-d stage decision

For fixed `d`, a d-image-reducible stage can be solved in `N^{O(d)}` time:

1. enumerate `D` with `|D|<=d` and retain a set whose full bank deletion exposes a DAG;
2. enumerate whether the budget-one extra gate lies in this stage, its two branches, and the normalized bank traversals, with at most `d` arrivals per private segment;
3. delete the bank and optional extra gate;
4. solve the resulting at-most-`4d+4` gate-disjoint requests by the fixed-dimensional product-state DAG linkage DP;
5. enforce actual signed-MUX source phases at the preceding common gate and optional extra gate.

The enumeration is polynomial for every fixed `d`; its degree is allowed to depend on `d`.

## Theorem — bounded branch-image budget-one tractability

For every fixed constant `d`, if every non-common V113 dominator stage is d-image-reducible, then the existence of a target-compatible return pair with

`overlap <= minimumOverlap + 1`

for the fixed opposite-phase first pair is decidable in deterministic time `N^{O(d)}`.

The proof composes Lemma 3 across the common-dominator chain using the V113 state `(common-branch-pair, extra-budget-used)`.

### Important special case

For `d=2`, the entire promised class is in P.

## Theorem — strict exact-stretch separation family

For every `depth>=0` and `width>=2`, `strict_branch_image_delta_one_family(depth,width)` has

- `m=n+1`;
- `minimumOverlap=1`;
- `minimumCompatibleOverlap=2` and therefore `Delta=1`;
- feedback-gate number exactly `width`;
- a cyclic stage that becomes acyclic after deleting a branch-image bank with `|D|=2`;
- no exact-clone deletion class that makes that stage acyclic.

The last item holds because both the forward and backward sides contain at least two exact signed-MUX signatures, while every directed 2-cycle chooses one forward and one backward resource.  Deleting any single exact-signature class leaves at least one resource on both sides.

Minimum overlap one is forced by the unique common dominator.  An overlap-one pair must take opposite common branches and receives incompatible target requirements there.  A compatible overlap-two witness takes the same common branch and shares the repair gate, then uses distinct forward/backward resources whose selector phases are fixed while their private data signs may differ.

## Classification

`frontier_progress` — polynomial theorem for a strictly larger signed-MUX phase-interface class than V118, with an infinite exact-stretch `Delta=1` separation family.

## Explicit nonclaims

- No FPT theorem parameterized by `d`.
- No polynomial theorem for unbounded `d`.
- No hardness theorem for signed-MUX branch-image number.
- No solution of all `Delta=1` signed-MUX instances.
- No solution of unrestricted `0x1b`, `NC0_3-Avoid`, or P versus NP.
- Novelty and peer review are not externally established.
