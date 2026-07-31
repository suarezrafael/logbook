# Cumulative scientific state

**Current laboratory:** V63  
**Updated:** 2026-07-30  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP route active:** no  
**External review:** requested, replies pending  
**External contact:** sent  
**Promotion model:** one laboratory per PR, CI, then merge to `main`

## One-paragraph state

The repository contains an integrated manuscript centered on a positive/negative dichotomy. V56 gives deterministic consistency-or-redundancy avoidance for efficiently represented affine output fibers at `m>n`. V57 proves that the analogous complete-block redundancy principle fails for bijunctive fibers through five orbit-`0x07` gates on four variables and an infinite direct-sum family. V58 introduces orientation depth and an `m^{O(d)} poly(n+m)` localization algorithm; V59 supplies boundary geometry and flat-potential barriers; V60 separates deterministic localization from elementary randomized avoidance. V61 repaired historical reproducibility, V62 integrated the paper and requested external review, and V63 records clean quick/full CI, prepares reviewer-facing appendices and changes repository governance to one merged PR per laboratory.

## Main manuscript chain

1. **Affine positive result — V56.** Efficient affine-fiber mixtures are deterministically avoidable in polynomial time for `m>n`.
2. **Bijunctive negative result — V57.** Joint consistency does not force a redundant complete 2-CNF gate block.
3. **Orbit-constrained obstruction.** Five `0x07`-orbit gates on four variables form a completely block-irredundant stretch-one instance.
4. **Infinite obstruction.** Direct sums give `n=4+3k`, `m=n+1` for every `k>=0`.
5. **Localization parameter — V58.** Orientation depth `d` yields an `m^{O(d)} poly(n+m)` algorithm.
6. **Geometry and barriers — V59.** Boundary points are abundant, but natural strict-improvement potentials may be flat.
7. **Regime separation — V60.** Polynomial-time image membership gives a Las Vegas algorithm with at most two expected tests.

## V63 promotion evidence

Legacy PR `#1` was merged into `main` as `968ac5d1b1b480484db1f4f22425e680f4204de9`. The clean GitHub Actions run `30595354956` passed both jobs after commit `233745d3f6a0613bc1d27fcfe9725ecb4a20d628`:

- quick: 22 executed, 4 justified skips, 0 failures;
- full: 24 executed, 2 justified skips, 0 failures;
- V56 index passed in full mode;
- V58 exact passed after 126,607 DFS nodes;
- V60 primary passed 285 checks after its historical-state repair;
- V62 primary and independent verifiers passed.

The earlier failure was editorial coupling in `v60/verify.py`, not a theorem failure. V60 had required the current cumulative ledger to remain at `external_contact.status == not_sent`. The repair checks historical non-contact in `v60/EXTERNAL_CONTACT_STATUS.md` while allowing the live ledger to evolve.

## V63 reviewer appendices

- `v63/APPENDIX_A_AFFINE_FIBERS.md` isolates the V56 assumptions, algorithm, certificate and barrier.
- `v63/APPENDIX_B_BIJUNCTIVE_BLOCKS.md` gives the V57 clauses, unique model and explicit irredundancy witnesses.
- `v63/APPENDIX_C_ORIENTATION_DEPTH.md` gives the V58 definitions, algorithm and finite evidence.
- `v63/REVIEWER_PACKET.md` states the exact questions for external review.
- `v63/CI_PROMOTION_RECORD.md` preserves the clean-CI evidence and justified skips.

## External requests

On 2026-07-30, prior-art questions were sent to Karthik Gajulapalli, Jayalal Sarma, Neha Kuntewar and Paolo Liberatore. Gmail was checked twice during V63 using the two original subjects and recipient names. No replies were found. No follow-up was sent because the interval is too short. The status remains `sent_awaiting_reply`.

No response, silence or negative search is evidence of novelty.

## Historical reproducibility corrections

**V22 reproducibility correction:** the original `full_certificate_cases.json` was never committed. The theorem remains a proof candidate, while its finite certificate evidence is not repository-reproduced and the cumulative row remains a justified `SKIP`.

## Known background and overlap

1. Range Avoidance and lower-bound connections are prior work.
2. `NC0_2-Avoid` algorithms are prior work.
3. Monotone `NC0_3-Avoid` at `m>n` is prior work.
4. CNF/2-CNF redundancy and IES are prior work.
5. UCP-irredundance is prior work.
6. Cube isoperimetry is classical.
7. Uniform randomized output sampling is elementary background.

## Contributions with unresolved novelty

- the exact grouped affine-fiber formulation of V56;
- the orbit-constrained V57 gadget and direct-sum family;
- orientation depth in the output-image setting;
- the specific boundary/flat-potential combination;
- the low-degree V54 separator as distinct from the known monotone algorithm.

None is declared novel pending specialist review.

## Current nonclaims

The project does not establish:

- deterministic polynomial-time general `NC0_3-Avoid`;
- universally bounded orientation depth;
- a universal monotone localization potential;
- completion of the `n=9` classification;
- novelty of general 2-CNF irredundancy;
- novelty of randomized sampling;
- unrestricted circuit lower bounds;
- `P != NP`.

## Promotion policy at V63

Every laboratory starts from current `main`, uses a dedicated branch, opens a non-draft PR, runs quick and full CI, and is squash-merged into `main` after success. A later correction is a separate corrective commit or laboratory; published historical evidence is not rewritten silently.

## Repository entry points

- `README.md` — orientation and version map.
- `STATE.md` — cumulative state.
- `LEDGER.json` — machine-readable scientific and promotion record.
- `verify_all.sh` — cumulative runner.
- `v62/INTEGRATED_MANUSCRIPT.md` — integrated manuscript.
- `v63/REVIEWER_PACKET.md` — reviewer-facing entry point.
- `v63/CI_PROMOTION_RECORD.md` — clean-CI evidence.
- `v63/V64_CORE_CONTEXT.md` — next-session context.

V22 remains a justified skip because the original certificate dataset is absent.
