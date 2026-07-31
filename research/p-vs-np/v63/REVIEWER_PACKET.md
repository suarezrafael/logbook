# Reviewer packet — affine fibers, bijunctive barriers and orientation depth

## Purpose

This packet isolates the claims for which specialist correction is most useful. It does not assert priority. The integrated narrative remains in `../v62/INTEGRATED_MANUSCRIPT.md`; the three V63 appendices are intended to make proof review possible without reconstructing the laboratory history.

## Reading order

1. `APPENDIX_A_AFFINE_FIBERS.md`
2. `APPENDIX_B_BIJUNCTIVE_BLOCKS.md`
3. `APPENDIX_C_ORIENTATION_DEPTH.md`
4. `../v62/SOURCE_TO_CLAIM.json`
5. `CI_PROMOTION_RECORD.md`

## Central positive claim

For `m>n`, if one selected fiber of every output coordinate has an efficiently computable affine description over `GF(2)`, a missing output can be constructed in deterministic polynomial time.

The proof has two branches:

- a minimal inconsistent subsystem produces a conjunction certificate;
- a consistent family becomes a collection of row-space blocks, and one block is contained in the sum of at most `n` other blocks.

### Questions

- Is this exact complete-block statement already standard in affine CSP, database dependencies, coding theory or matroid language?
- Is there a canonical theorem name that should replace “consistency-or-redundancy”?
- Is the `n+1` certificate-size bound immediate from a known circuit or Helly-type theorem?

## Central negative claim

Five ternary gate-fiber blocks from the NPN orbit of `0x07` on four variables are jointly satisfiable with unique model `0000`, but none of the five complete blocks is implied by the other four. Direct sums give an infinite stretch-one family.

The collapsed formula is a six-clause clause-irredundant 2-CNF. General 2-CNF irredundancy is not claimed as new. The constrained object is the partition into constant-size local gate blocks from one NPN orbit.

### Questions

- Is block or group irredundancy under 2-CNF entailment standard terminology?
- Is this five-block pattern equivalent to a known IES construction?
- Does the same-orbit and minimum-positive-stretch restriction appear in prior work?

## Parameterized localization claim

For circuits whose selected fibers are 2-CNF, orientation depth is the Hamming distance from a baseline image word to the internal boundary of the image. If the depth is at most `d`, exhaustive search over the radius-`d` Hamming ball plus 2-SAT entailment gives an `m^{O(d)} poly(n+m)` deterministic algorithm.

### Questions

- Does this parameter coincide with a known solution-graph, reconfiguration or frozen-variable parameter?
- Is there a stronger algorithm than Hamming-ball enumeration?
- Are constant-depth or logarithmic-depth bounds known for the orbit `0x07`?

## Explicit nonclaims

This packet does not claim:

- a deterministic algorithm for general `NC0_3-Avoid`;
- universal constant orientation depth;
- novelty of CNF or 2-CNF irredundancy;
- novelty of randomized output sampling;
- a circuit lower bound;
- progress toward resolving P versus NP.

## Reproducibility status

The cumulative quick and full verifiers pass in clean GitHub Actions. V22 remains a justified skip because its original serialized certificate dataset was not committed.
