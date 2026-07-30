# Manuscript plan

## Working title

**Range Avoidance for Local Boolean Circuits: Affine Algorithms, Bijunctive Barriers and Orientation Depth**

## Central story

The paper is organized around one positive/negative pair:

> efficiently represented affine output fibers admit a deterministic consistency-or-redundancy algorithm at minimum positive stretch, while the natural block-redundancy extension to bijunctive fibers fails through an explicit minimal construction and an infinite family.

Orientation depth, boundary geometry and randomized easy-membership are supporting results that explain what remains after this failure.

## Proposed structure

### 1. Introduction

- Range Avoidance and local Boolean circuits.
- The affine-versus-bijunctive dichotomy.
- Difference between randomized avoidance and deterministic localization.
- Exact limitations and novelty status.

### 2. Preliminaries

- Boolean circuits, positive stretch and output fibers.
- Ternary NPN equivalence and the 14-class classification.
- Affine systems, 2-CNF, implication graphs and block entailment.
- Internal vertex boundary and orientation depth.

### 3. Affine-fiber avoidance

- Pure `AND_k` forcing-core separator, with explicit comparison to monotone `NC0_3-Avoid` prior work.
- V56 consistency-or-redundancy dichotomy.
- Minimum-positive-stretch deterministic algorithm.
- Constructive certificates and complexity.

### 4. Bijunctive redundancy barrier

- Standard 2-CNF redundancy and irredundant-equivalent-subset terminology.
- Explicit five-block orbit-`0x07` construction.
- Complete irredundancy proof.
- Exhaustive minimality evidence at `n=4,m=5`.
- Infinite direct-sum family.
- Why affine rank, SCC count and forced-variable count do not extend.

### 5. Orientation depth

- Boundary/forcing equivalence.
- Definition of orientation depth.
- `m^{O(d)} poly(n+m)` algorithm.
- Complete one-flip audit through `n=8`.
- Limited falsification role of `n=9`.

### 6. Boundary abundance and localization barriers

- Boolean-cube vertex isoperimetry.
- Uniform-image versus uniform-input measures.
- Flat exact-forcing, unit-propagation and fiber-size potentials.
- Limits of strict-improvement walking arguments.

### 7. Easy-membership randomized regime

- Las Vegas sampling theorem.
- Tightness at stretch one.
- Why this is a scope theorem rather than a novelty claim.
- Separation between avoidance and derandomization.

### 8. Computational methodology

- Symmetry normalization and complete finite searches.
- Independent verifiers.
- Retraction protocol and regression cases.
- V22 missing-artifact correction.
- Machine-readable results and hashes.

### 9. Related work

At minimum:

- Korten; Ren–Santhanam–Wang; Guruswami–Lyu–Wang; Gajulapalli et al. on Range Avoidance.
- Kuntewar–Sarma on monotone `NC0_3-Avoid` at `m>n`.
- Liberatore on CNF and 2-CNF redundancy and irredundant equivalent subsets.
- Savický on UCP-irredundant formulas.
- Boolean-cube isoperimetry.
- CSP solution-graph and reconfiguration parameters potentially related to orientation depth.

### 10. Limitations and open problems

- no general deterministic `NC0_3-Avoid` algorithm;
- no universal bounded orientation depth;
- no completed `n=9` classification;
- no unrestricted lower bound;
- exact novelty of V56–V58 pending specialist review.

## Supplementary material

The complete four-input V25 classification and V26–V27 follow-up are scientifically valid but not part of the main V54–V60 theorem chain. They may appear as:

- a separate appendix;
- an online supplementary note; or
- a later independent paper.

They should not occupy a main narrative section unless a reviewer identifies a direct conceptual dependency.

## Material to omit

- obsolete progress indices measuring distance to P versus NP;
- incomplete searches presented as confidence evidence;
- detailed version-by-version diary prose;
- unimplemented SMS/DRAT plans except as future-work notes;
- claims whose only support was retracted in V53;
- any statement that general 2-CNF irredundancy is new.

## External-review package

Before submission:

1. run `verify_all.sh --full` in a clean environment;
2. reconcile every theorem statement against `LEDGER.json`;
3. recover or formally close the V22 artifact issue;
4. obtain specialist review of the affine proof;
5. obtain specialist review of the bijunctive construction and orientation-depth proof;
6. complete a source-by-source novelty audit;
7. record all corrections before changing external-contact status.
