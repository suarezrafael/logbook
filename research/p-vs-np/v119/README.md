# V119 — bounded branch-image feedback banks

V119 strictly enlarges the V118 signed-MUX tractable class for the fixed opposite-phase repeated-selector pair.

## Main result

For a non-common V113 dominator stage and a variable set `D`, define

`B_D = { g : data0(g) in D and data1(g) in D }`.

The stage is **d-image-reducible** if, for some `|D| <= d`, deleting all gates in `B_D` makes the stage acyclic.

For every fixed constant `d`, V119 decides whether a target-compatible return pair exists with

`overlap <= minimumOverlap + 1`

in time `N^{O(d)}`.  In particular, the full `d=2` class is polynomial-time decidable.

## Why exact clones are unnecessary

Consider one route segment between shared boundaries.  If two traversed bank gates both arrive at the same variable `v in D`, keep the first arrival and delete the entire excursion through the later bank gate that returns to `v`.  The resulting gate sequence is still valid and gate-simple.  The first traversal of the segment is unchanged, so the source phase seen by the preceding shared gate is unchanged as well.

Repeating this operation leaves at most one bank arrival per destination in `D`.  Thus a normalized segment uses at most `d` bank gates even when the raw feedback-gate number and the number of distinct signed MUX signatures are unbounded.

With at most one extra shared gate `q`, each route has at most two such segments.  After deleting the bank and `q`, the remaining connectors form at most `4d+4` fixed gate-disjoint requests in a DAG.  V119 enumerates the bounded bank interface, enforces the first-traversal phase constraints, solves the residual DAG linkage, and composes the stages with the V113 branch/budget DP.

## Strict separation from V118

`strict_branch_image_delta_one_family(depth, width)` preserves exact stretch `m=n+1`, has

- `minimumOverlap = 1`,
- `minimumCompatibleOverlap = 2`, hence `Delta = 1`,
- feedback-gate number exactly `width`,
- no single exact-MUX-clone class whose deletion breaks the cyclic stage for `width >= 2`,
- a two-destination branch-image bank whose deletion does break the cyclic stage.

The forward and backward banks deliberately vary private data polarities/output flips while preserving the selector phases needed by the explicit `Delta=1` witness.

## Verification

- `verify.py`: solver/family checks through width 8 and depth 7, exact feedback-number controls, V118 structural rejection, 32 private-sign variants, and a full range check on the smallest family member.
- `verify_independent.py`: reconstructs the family without importing V119, brute-forces widths 2 and 3, independently checks feedback number and branch-image deletion, checks that no exact-clone class suffices, and audits destination loop-erasure on 138 cyclic routes.

Finite verification supports the implementation; the polynomial theorem rests on the loop-erasure and fixed-request DAG-linkage proof.

## Nonclaims

V119 does not prove FPT parameterized by `d`, does not solve unbounded branch-image size, does not prove signed-MUX hardness for `d`, and does not solve unrestricted `0x1b`, `NC0_3-Avoid`, or P versus NP.
