# Cumulative scientific state

**Current laboratory:** V60  
**Updated:** 2026-07-30  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP route active:** no  
**External review:** pending  
**External contact:** not sent

## One-paragraph state

The repository now supports a coherent research article about range avoidance for local Boolean circuits. The strongest positive result is the V56 deterministic polynomial-time algorithm for arbitrary mixtures of efficiently represented affine output fibers at minimum positive stretch `m>n`. V57 shows that the analogous fixed-orientation redundancy principle fails for bijunctive fibers, V58 introduces orientation depth and an `m^{O(d)} poly(n+m)` algorithm, and V59 proves global boundary abundance while preserving a direct-sum family that defeats several natural strict-improvement potentials. V60 records that, whenever image membership is polynomial-time and `m>n`, uniform output sampling already gives a Las Vegas range-avoidance algorithm with at most two expected trials. The remaining deterministic questions are legitimate but are no longer described as an active route to P versus NP.

## Stable results

### Local classifications and algebraic certificates

1. V16 gives a finite signed-MAJ3 obstruction classification.
2. V20–V22 develop effective-dimension and zero-set-polynomial dependency candidates.
3. V25 classifies all 65,536 four-input Boolean functions into 222 NPN classes.
4. V25 finds 215 of 222 four-input NPN classes representable by zero sets of degree at most two over `GF(5)` after optional output complementation.
5. V27 gives affine-parity certificates for the seven cubic four-input classes.
6. V55 classifies all 256 ternary truth tables into 14 NPN classes.

### Affine-fiber positive results

7. V54 constructs a degree-at-most-`k+1` range separator for positive-stretch pure `AND_k` circuits.
8. V56 proves a consistency-or-redundancy dichotomy for affine output fibers.
9. For `C:{0,1}^n -> {0,1}^m`, `m>n`, arbitrary mixtures of efficiently represented affine fibers are avoidable deterministically in polynomial time.
10. The affine ternary classes include canonical representatives `0x01`, `0x06`, `0x18`, and `0x69`.

### Bijunctive frontier

11. V57 gives five `0x07`-orbit gates on four variables whose chosen 2-CNF fibers are jointly consistent and completely irredundant.
12. The V57 construction extends by direct sum to `n=4+3k`, `m=n+1` for every `k>=0`.
13. A boundary edge of the image is equivalent to a context that forces one output bit.
14. V58 defines orientation depth as distance from a baseline image point to the internal boundary.
15. For bijunctive fibers, depth `d` yields an `m^{O(d)} poly(n+m)` deterministic algorithm.
16. The exact one-flip search is complete through `n=8`; `n=9` remains open.
17. The 12 finite V57 families form one variable-isomorphism class and have depth one.

### Geometry and randomization

18. V59 applies the vertex-isoperimetric profile of the cube: for nonempty `S` with `|S|<=2^(m-1)`,

```text
|internal_boundary(S)| / |S|
  >= binom(m,floor(m/2)) / 2^(m-1)
   = Theta(1/sqrt(m)).
```

19. The V57 direct-sum family has a unique interior point, while exact forced-variable count, unit-propagation count, and fiber size are flat from that point to every neighbor.
20. Therefore no universal walking proof can require strict improvement of any one of those three potentials on its first step.
21. V60 records the elementary easy-membership theorem: if image membership is decidable in polynomial time and `m>n`, sampling `y` uniformly from `{0,1}^m` succeeds with probability at least `1-2^(n-m)`.
22. The expected number of trials is at most `1/(1-2^(n-m))`, hence at most two.
23. At stretch one, equality in the two-trial upper bound is possible when the circuit is injective.

## Corrections and retractions

1. **V53 retraction:** incidence girth greater than `4t` does not imply `t`-union-freeness.
2. **V53 retraction:** the derived stretch-one `AND3` syndrome-degree `Omega(log n)` family is unsupported.
3. **Preserved from V53:** the union-free substitution lemma and finite UF2/UF3 computations.
4. Acyclic nested-cover examples remain permanent regression tests.
5. No incomplete `n=9` search is evidence of a theorem.
6. Random experiments are diagnostics only.

## Current nonclaims

The project does not establish:

- a deterministic polynomial-time algorithm for general `NC0_3-Avoid`;
- a universal bounded orientation depth;
- a universal monotone potential for walking to the boundary;
- completion of the `n=9` exact classification;
- circuit lower bounds for unrestricted circuits;
- `P != NP` or any equivalent consequence;
- novelty or priority without external literature review.

## Current open questions

1. Can deterministic avoidance for non-affine local fibers be proved without solving general image membership?
2. Is orientation depth bounded or efficiently navigable for a meaningful nontrivial subclass beyond the affine case?
3. Can the direct-sum plateau be crossed by a rigorously analyzed nonmonotone or memory-based rule?
4. Is there a useful deterministic sampler or hitting set for the complements of these circuit images?
5. Which results are already implicit in the 2-CNF irredundancy, CSP, proof-complexity, and range-avoidance literature?
6. Does the `n=9` finite case reveal any structural obstruction worth retaining after manuscript review?

## Program decision at V60

The active objective is now **manuscript readiness and external validation**, not further narrowing toward a finite `n=9` computation. Exact search remains available for falsification, regression and reviewer-requested checks. A separate future lower-bounds program would need to leave the easy-membership regime and define a new connection to explicit constructions; it must not be presented as a continuation automatically justified by the current results.

## Repository entry points

- `README.md` — orientation and version map.
- `STATE.md` — this compact cumulative state.
- `LEDGER.json` — machine-readable claims and versions.
- `SCIENTIFIC_METHOD.md` — promotion and retraction policy.
- `verify_all.sh` — curated verifier runner.
- `v60/MANUSCRIPT_PLAN.md` — proposed paper structure.
- `v60/V61_CORE_CONTEXT.md` — next-session context.

## Verification

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Default mode avoids intentionally expensive exact search. `--full` includes exact verifiers where present. A missing historical verifier is `SKIP`, not `PASS`.
