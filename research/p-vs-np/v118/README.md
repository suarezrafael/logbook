# V118 — signed-MUX clone-bank loop erasure

V118 isolates a signed-MUX invariant that is absent from the generic W[1]-hard two-chain abstraction of V117.

## Main theorem

Fix an opposite-phase repeated-selector MUX first pair and its V113 chain of common return-gate dominators. Assume that every non-common dominator stage is either a DAG or becomes a DAG after deleting one class of **exact MUX clones**: outputs with identical selector, data inputs, input polarities and output flip.

Then the existence of a target-compatible gate-simple return pair with

`overlap <= minimum_overlap + 1`

is decidable in deterministic polynomial time.

The size of the clone class is unrestricted. In particular, the theorem is not parameterized by the raw feedback-gate number.

## Why the V117 hardness transfer does not survive this promise

Cut each route at the possible unique extra shared gate `q`. Inside either side of the cut, if one route uses two clone outputs with the same branch, the subwalk between the two equal branch endpoints is a closed loop. Erasing that loop keeps the route valid, deletes gates rather than adding overlap, and preserves the first signed phase seen from the adjacent shared boundary.

Therefore a normalized route uses at most one clone of branch 0 and at most one clone of branch 1 on each side of `q`: at most four clone outputs per route. Removing the whole clone bank and `q` leaves a DAG, so the remaining problem is a constant-cardinality gate-disjoint linkage problem. At most four first traversals are phase-sensitive; they are enumerated explicitly before the residual DAG product-state DP.

The V113 dominator DP then composes the stages with only `(common-branch-pair, extra-used)` as cross-stage state.

## Exact-stretch separation family

`strict_clone_bank_delta_one_family(depth, width)` is defined for `depth >= 0`, `width >= 2` and satisfies

- `n = 7 + depth + 2*width`;
- `m = 8 + depth + 2*width = n+1`;
- minimum overlap = 1;
- minimum target-compatible overlap = 2, hence `Delta=1`;
- the relevant post-dominator stage has feedback-gate number exactly `width`;
- deleting the `width` exact forward clones exposes a DAG.

Thus the feedback-gate number is unbounded while the normalized signed interface remains constant. For `width >= 2` this family lies outside the V116 `tau<=1` theorem.

## Verification

- `verify.py` checks the strict family over several widths/depths, exact small feedback numbers, one full-image missing target, and 96 randomized signed width-two cross-checks against exhaustive gate-simple return enumeration.
- `verify_independent.py` does not import the V118 solver. It independently rebuilds the family, brute-forces widths 2 and 3, exhaustively verifies feedback number 2–4, and audits loop erasure on the width-three route census.

## Boundary

V118 does **not** prove FPT for arbitrary feedback-gate number, does not refute V117, and does not solve unrestricted signed-MUX `Delta<=1`. Exact-clone structure is essential to the proof. No claim is made about unrestricted `NC0_3-Avoid`, circuit lower bounds, or P versus NP.
