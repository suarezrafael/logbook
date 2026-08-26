# V119 scientific status

**Classification:** frontier_progress

## Promotable statement

For every fixed constant branch-image bound `d`, the fixed opposite-phase signed-MUX `Delta<=1` problem is decidable in deterministic time `N^{O(d)}` when every non-common V113 dominator stage becomes acyclic after deleting a bank `B_D` whose two branch destinations lie in one set `D`, `|D|<=d`.

In particular, the complete promised class with `d=2` is polynomial-time decidable.

## Structural advance over V118

V118 required one exact signed-MUX clone class per cyclic stage.  V119 needs no equality of selector, data polarities, or output flip inside the deleted bank.  The route normalization depends only on repeated **arrival destinations**: returning to a previously reached `v in D` permits loop erasure while preserving the first traversal after the shared boundary.

The strict family has unbounded feedback-gate number, exact stretch, `Delta=1`, multiple exact MUX signatures on both sides of the feedback bank, and therefore lies outside the V118 promise for every width at least two.

## Verification evidence

Primary verification covers widths 2 through 8 and depths 0,1,3,7, 32 private-sign variants, the smallest full-image/range control, exact feedback-number checks through width 4, and structural rejection by V118.

Independent verification imports no V119 implementation.  It reconstructs the family, brute-forces widths 2 and 3, checks the feedback number, verifies that no exact-clone class breaks the cyclic stage, identifies the two-destination deletion banks, and audits destination loop erasure on 138 gate-simple cyclic routes.

These checks validate the implementation and intended examples.  They are not the proof of the asymptotic theorem.

The implementation reuses the per-stage branch-image set/bank already found during stage partitioning and prunes special plans that repeat a private bank gate within one route or share a private bank gate across the two routes before invoking the residual realizer.  These are sound implementation-level pruning steps only; they do not strengthen the stated `N^{O(d)}` runtime bound or any scientific claim.

## Open boundary

The exponent of the direct algorithm grows with `d`.  V119 does not decide whether branch-image number admits an FPT algorithm `f(d) poly(N)`, nor whether the generic V117 W[1]-hard barrier can be realized under bounded branch-image structure.

## Global nonclaims

- `Delta=1` unrestricted remains open.
- all signed-MUX `0x1b` remains open.
- unrestricted `NC0_3-Avoid` remains open.
- P versus NP is not resolved.
- novelty is not confirmed and the result is not peer reviewed.
