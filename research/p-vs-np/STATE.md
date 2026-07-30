# Cumulative scientific state

**Current laboratory:** V62  
**Updated:** 2026-07-30  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP route active:** no  
**External review:** requested, replies pending  
**External contact:** sent

## One-paragraph state

The repository now contains an integrated manuscript centered on a positive/negative dichotomy. V56 gives a deterministic consistency-or-redundancy algorithm for efficiently represented affine output fibers at `m>n`. V57 proves that the analogous complete-block redundancy principle fails for bijunctive fibers, using five orbit-`0x07` gates on four variables and an infinite direct-sum family. V58 introduces orientation depth and an `m^{O(d)} poly(n+m)` algorithm; V59 proves boundary abundance while exhibiting flat first-step potentials; V60 separates deterministic localization from an elementary Las Vegas algorithm. V61 repaired V22 reproducibility and narrowed novelty claims. V62 integrates the paper, translates V57 into standard IES terminology, compares V54 with Kuntewar–Sarma, creates a source-to-claim matrix, and sends two external prior-art requests.

## Main manuscript chain

1. **Affine positive result — V56.** Efficient affine-fiber mixtures are deterministically avoidable in polynomial time for `m>n`.
2. **Bijunctive negative result — V57.** Joint consistency does not force a redundant complete 2-CNF gate block.
3. **Orbit-constrained obstruction.** Five `0x07`-orbit gates on four variables give the smallest example in the searched universe.
4. **Infinite obstruction.** Direct sums give `n=4+3k`, `m=n+1` for every `k>=0`.
5. **Localization parameter — V58.** Orientation depth `d` yields an `m^{O(d)} poly(n+m)` algorithm.
6. **Geometry and barriers — V59.** Boundary points are abundant, but several natural strict-improvement potentials are flat.
7. **Regime separation — V60.** Easy image membership gives a Las Vegas algorithm using at most two expected tests.

## V62 clarifications

### V57 and IES terminology

After duplicate copies of the common unit clause are removed, the V57 gadget is a six-clause clause-irredundant 2-CNF. General CNF and 2-CNF irredundancy are prior art. The repository-specific statement concerns a partition into five essential local gate-fiber blocks, all from one ternary NPN orbit, at minimum positive stretch.

### V54 and monotone prior work

Kuntewar–Sarma 2025 proves deterministic `MONOTONE-NC0_3-Avoid` for `m>n`. This subsumes the algorithmic conclusion of V54 for pure `AND3`. V54 is retained only for its direct 2-core witness and degree-at-most-four separator, plus the pure `AND_k` degree-at-most-`k+1` statement. Certificate equivalence remains unresolved.

### Orientation-depth search

The V62 search found nearby literature on Boolean CSP solution graphs, connectivity, reconfiguration and frozen variables, but no exact output-image boundary-distance parameter with the same FPT use. This is a negative search result, not confirmation of novelty.

## External requests

On 2026-07-30, prior-art questions were sent to:

- Karthik Gajulapalli, Jayalal Sarma and Neha Kuntewar;
- Paolo Liberatore.

The status is `sent_awaiting_reply`. No response is presumed. A response changes the scientific record only after it is read, preserved accurately and evaluated against the proofs.

## Historical and supplementary results

- V20–V22 remain proof candidates.
- **V22 reproducibility correction:** the original `full_certificate_cases.json` was never committed; its row is `SKIP`, not `PASS`.
- V25 is a valid finite four-input classification but supplementary to the main paper.
- V53 preserves its union-free substitution lemma and finite computations; two derived claims remain retracted.

## Known background and overlap

1. Range Avoidance and its lower-bound connections are prior work.
2. `NC0_2-Avoid` algorithms are prior work.
3. Monotone `NC0_3-Avoid` at `m>n` is prior work.
4. CNF/2-CNF redundancy and IES are prior work.
5. UCP-irredundance is prior work.
6. Cube isoperimetry is classical.
7. Randomized output sampling is elementary background.

## Contributions with unresolved novelty

- the exact grouped affine-fiber theorem of V56;
- the orbit-constrained V57 gadget, finite classification and direct sums;
- orientation depth in the Range-Avoidance output-image setting;
- the specific combination of boundary geometry and flat-potential examples;
- the degree-bounded V54 separator as distinct from the monotone algorithmic theorem.

None is declared novel pending specialist review.

## Current nonclaims

The project does not establish:

- a deterministic polynomial-time algorithm for general `NC0_3-Avoid`;
- a universal bounded orientation depth;
- a universal monotone potential for boundary localization;
- completion of the `n=9` classification;
- novelty of general 2-CNF irredundancy;
- novelty of randomized output sampling;
- an unrestricted circuit lower bound;
- `P != NP` or any equivalent consequence.

## Current open questions

1. Is V56 already explicit in affine CSP, coding or grouped-linear-constraint language?
2. Is the orbit-constrained V57 construction a known grouped IES pattern?
3. Does orientation depth coincide with an existing solution-graph parameter after translation?
4. Is V54's low-degree separator implicit in Kuntewar–Sarma?
5. What corrections or references will the contacted specialists provide?
6. Can the full repository runner pass in clean CI, with V22 as a justified skip?

## Program decision at V62

The active objective is external correction and manuscript revision. Every future laboratory is committed as one coherent commit. Exact `n=9` work remains optional falsification/regression. No progress score toward P versus NP may be introduced.

## Repository entry points

- `README.md` — orientation and version map.
- `STATE.md` — this compact state.
- `LEDGER.json` — machine-readable claims, corrections and outreach.
- `verify_all.sh` — cumulative runner.
- `v62/INTEGRATED_MANUSCRIPT.md` — integrated draft.
- `v62/SOURCE_TO_CLAIM.json` — automated citation/claim matrix.
- `v62/EXTERNAL_CONTACT_STATUS.md` — sent/awaiting-reply record.
- `v62/V63_CORE_CONTEXT.md` — next-session context.
