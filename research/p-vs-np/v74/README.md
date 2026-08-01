# Laboratory V74 — exact two-fiber avoidance

V74 replaces the normalized one-fiber schema with an explicit Boolean gate model containing a truth table, output polarity, and exact disjoint affine decompositions of both output fibers.

## Main results

1. Every ternary fiber is a disjoint union of at most three affine cells, and seven-point fibers require three.
2. A weighted branch-residual DP computes the exact preimage count of a supplied output word.
3. Prefix counting constructs an avoided output for positive-stretch circuits in `O(m^2 A(b)^2 poly(n,m))` time when a width-`b` branch decomposition is supplied.
4. Exhaustive verification covers all 4,096 two-input/three-output binary-gate circuits and all 32,768 target words.
5. The OR=1 path family has primal treewidth one and exact `G*_proj=3m-3` for `m>=2`.
6. For prefix-feasible systems, the bicriteria price satisfies `C_B/G*_proj <= A(B)`.

## Files

- `two_fiber_model.py` — exact gate fibers, weighted target counting, and constructive prefix search.
- `or_path_family.py` — exact bounded-treewidth residual family.
- `v74_two_fiber_avoidance.py` — deterministic result generator.
- `verify.py` — primary repository verifier.
- `verify_independent.py` — independent truth-table and all-order audit.
- `TWO_FIBER_AVOIDANCE.md` — definitions and proofs.
- `V74_TWO_FIBER_AVOIDANCE_THEOREM.tex` — formal module.
- `RESULTS.json` — deterministic snapshot.
- `V75_CORE_CONTEXT.md` — frozen next-step constraints.

## Nonclaims

V74 does not solve unrestricted `NC0_3-Avoid`, does not find a bounded-width decomposition in polynomial time, does not prove a superpolynomial projected-residual lower bound, and does not resolve P versus NP.
