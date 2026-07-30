# Cumulative scientific state

**Current laboratory:** V61  
**Updated:** 2026-07-30  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP route active:** no  
**External review:** pending  
**External contact:** not sent

## One-paragraph state

The coherent manuscript is now centered on a positive/negative dichotomy. V56 gives a deterministic polynomial-time consistency-or-redundancy algorithm for efficiently represented affine output fibers at minimum positive stretch `m>n`. V57 shows that the analogous block-redundancy argument fails for bijunctive fibers, through an explicit five-block orbit-`0x07` construction and an infinite direct-sum family. V58 introduces orientation depth and an `m^{O(d)} poly(n+m)` deterministic algorithm; V59 proves boundary abundance and barriers to several strict-improvement potentials; V60 records that polynomial-time image membership makes positive-stretch Avoid Las Vegas-easy in at most two expected trials. V61 repairs the historical V22 reproducibility status and narrows novelty claims against primary literature.

## Main manuscript chain

1. **Affine positive result — V56.** Efficient affine-fiber mixtures are deterministically avoidable in polynomial time for `m>n`.
2. **Bijunctive negative result — V57.** Joint consistency does not force a redundant 2-CNF block, even with five orbit-`0x07` gates on four variables.
3. **Infinite obstruction.** The V57 construction extends to `n=4+3k`, `m=n+1`.
4. **Localization parameter — V58.** Orientation depth `d` gives an `m^{O(d)} poly(n+m)` algorithm.
5. **Geometry and barriers — V59.** The internal boundary is globally abundant, but forced-count, unit-propagation count and fiber size can all be flat at the first step.
6. **Regime separation — V60.** If image membership is in P, uniform output sampling succeeds with probability at least `1-2^(n-m)` and expected trials at most two.

## Historical and supplementary results

- V20–V22 contain proof candidates on effective dimension and zero-set polynomial dependencies.
- V22's aggregate `RESULTS.json` survives, but the original `full_certificate_cases.json` containing 125 serialized cases was never committed. Its verifier is therefore not repository-executable.
- V25's complete four-input NPN classification is a valid finite result but is supplementary to the V54–V60 paper narrative.
- V53 preserves the union-free substitution lemma and two finite computations; its girth implication and derived logarithmic claim remain retracted.

## Prior-art audit at V61

### Known background or direct overlap

1. General CNF redundancy and irredundant equivalent subsets were studied by Liberatore before this project.
2. The 2-CNF-specific redundancy and irredundant-equivalent-subset problem was studied explicitly by Liberatore.
3. UCP-irredundance is an established, distinct notion; V59's unit-propagation plateau must not be marketed as inventing that subject.
4. The randomized output-sampling observation for Avoid is elementary and part of the standard problem framing.
5. Range Avoidance connections to explicit constructions and lower bounds are established in the Korten, Ren–Santhanam–Wang and Guruswami–Lyu–Wang lines.
6. A 2025 result gives deterministic polynomial-time `MONOTONE-NC0_3-Avoid` for `m>n`. Any claim around V54 for monotone ternary circuits must state this overlap.

### Contributions whose exact prior-art status remains unresolved

7. The exact V56 block-system formulation for arbitrary mixtures of efficiently represented affine output fibers.
8. The smallest same-orbit circuit-image instance underlying V57, including the complete `n=4,m=5` classification.
9. The V57 infinite direct-sum family under the local-gate restrictions.
10. Orientation depth and its exact Range-Avoidance formulation.
11. The combination of boundary geometry with the explicit flat-potential family.

These are not declared novel until specialist review.

## Corrections, retractions and reproducibility debt

1. **V53 retraction:** incidence girth greater than `4t` does not imply `t`-union-freeness.
2. **V53 retraction:** the derived stretch-one `AND3` syndrome-degree `Omega(log n)` family is unsupported.
3. **V22 reproducibility correction:** the verifier requires an absent directory artifact and cannot reproduce the recorded 125 cases from `RESULTS.json`.
4. The V22 runner row is `SKIP`, not `PASS`.
5. No incomplete `n=9` search is evidence of a theorem.
6. Random experiments are diagnostics only.

## Current nonclaims

The project does not establish:

- a deterministic polynomial-time algorithm for general `NC0_3-Avoid`;
- a universal bounded orientation depth;
- a universal monotone potential for walking to the boundary;
- completion of the `n=9` exact classification;
- novelty of the general notions of CNF or 2-CNF irredundancy;
- novelty of randomized output sampling for Avoid;
- circuit lower bounds for unrestricted circuits;
- `P != NP` or any equivalent consequence.

## Current open questions

1. Is the V56 affine-block theorem already explicit in coding, CSP or Range-Avoidance literature?
2. Is the V57 orbit-constrained minimal example new after translating it into standard IES terminology?
3. Does orientation depth coincide with an existing parameter in CSP reconfiguration, solution-graph geometry or proof complexity?
4. Can deterministic avoidance be proved for a meaningful non-affine subclass not already covered by monotone `NC0_3` algorithms?
5. Which external reviewer can independently audit both the affine proof and the bijunctive construction?

## Program decision at V61

The active objective is manuscript readiness and external validation. The main narrative excludes the V25 four-input classification except as optional supplementary material. Exact `n=9` search remains available only for falsification, regression and reviewer-requested checks. No new score measuring progress toward P versus NP may be introduced.

## Repository entry points

- `README.md` — orientation and version map.
- `STATE.md` — this compact state.
- `LEDGER.json` — machine-readable claims, corrections and prior-art status.
- `verify_all.sh` — curated verifier runner with explicit skips.
- `v61/PRIOR_ART_AUDIT.md` — source-by-source audit.
- `v61/MANUSCRIPT_ABSTRACT.md` — refocused abstract.
- `v61/V62_CORE_CONTEXT.md` — next-session context.
