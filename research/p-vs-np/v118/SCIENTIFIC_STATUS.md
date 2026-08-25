# V118 scientific status

## Promotable claim

**Internal theorem candidate.** For a fixed opposite-phase repeated-selector signed-MUX first pair, if every non-common V113 dominator stage is a DAG or becomes a DAG after deleting one exact MUX-clone class, then `Delta<=1` is decidable in deterministic polynomial time.

The proof uses an internal loop-erasure lemma plus fixed-dimensional DAG linkage; it does not import a new external algorithmic theorem beyond the already-promoted V113/V116 machinery.

## Material separation from V116

V116 requires feedback-gate number at most one in every non-common stage. V118's strict family has feedback-gate number exactly `width`, for arbitrary `width>=2`, while still satisfying the clone-bank promise and exact stretch `m=n+1`.

Thus V118 is not merely a rephrasing of `tau<=1`.

## Relation to V117

V117 proves a W[1]-hard barrier for generic supplied-feedback two-chain gate linkage. V118 does not contradict it: exact MUX cloning creates a route-normalization rule absent from arbitrary gate-resource instances. The hard V117 family is not asserted to satisfy the clone-bank promise.

## Finite evidence

The primary verifier includes exhaustive return-pair comparisons for 96 randomized signings of the width-two topology. The independent verifier reconstructs the family without importing the solver, brute-forces widths two and three, verifies feedback number two through four, and audits route loop erasure.

These finite checks support implementation correctness only. The polynomial-time claim rests on the proof in `THEOREMS.md` and the formal LaTeX note.

## Critical nonclaims

- no algorithm for arbitrary feedback-gate number without the exact-clone promise;
- no FPT theorem for an arbitrary number of clone classes;
- no hardness theorem for signed-MUX feedback number;
- no solution of unrestricted signed-MUX `Delta<=1`;
- no solution of unrestricted `NC0_3-Avoid`;
- no circuit lower bound or P-versus-NP resolution;
- novelty is not externally confirmed and the result is not peer reviewed.
