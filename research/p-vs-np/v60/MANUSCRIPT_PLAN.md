# Manuscript plan

## Working title

**Range Avoidance for Local Boolean Circuits: Affine Algorithms, Bijunctive Barriers and Orientation Depth**

## Intended contribution

A self-contained structural paper about `NC0_k-Avoid`, with reproducible finite classifications and explicit negative results. The paper should not use P versus NP as its headline or imply that the current regime directly yields unrestricted lower bounds.

## Proposed structure

### 1. Introduction

- Range Avoidance and local Boolean circuits.
- Difference between finding an absent output and deciding image membership.
- Summary of positive affine results, bijunctive barriers and geometric localization.
- Exact statement of limitations.

### 2. Preliminaries

- Boolean circuits and positive stretch.
- NPN equivalence.
- Output fibers, orientations and image membership.
- Affine systems, 2-CNF and implication graphs.
- Internal vertex boundary and orientation depth.

### 3. Local classifications

- Ternary 14-class NPN classification.
- Four-input 222-class classification as supplementary context.
- Affine and non-affine fiber frontier.

### 4. Affine-fiber avoidance

- Pure `AND_k` forcing-core separator.
- V56 consistency-or-redundancy dichotomy.
- Minimum-positive-stretch deterministic algorithm.

### 5. Bijunctive redundancy barrier

- Explicit five-block `0x07` construction.
- Complete irredundancy proof.
- Infinite direct-sum family.
- Why dimension, SCC count and forced-variable count do not replace affine rank.

### 6. Orientation depth

- Boundary/forcing equivalence.
- Definition of orientation depth.
- `m^{O(d)} poly(n+m)` algorithm.
- Complete one-flip audit through `n=8` and the limited role of `n=9`.

### 7. Boundary abundance and localization barriers

- Harper profile for internal boundary.
- Uniform-image versus uniform-input measures.
- Flat exact-forcing, unit-propagation and fiber-size potentials.
- Limits of monotone walking arguments.

### 8. Easy-membership randomized regime

- Las Vegas theorem with expected trials at most two.
- Why the theorem is elementary but strategically decisive.
- Separation between randomized avoidance and deterministic derandomization.

### 9. Computational methodology

- Symmetry normalization.
- Independent verifiers.
- Retraction protocol and preserved regression cases.
- Machine-readable results and hashes.

### 10. Related work

External review must specifically check:

- Range Avoidance and explicit constructions;
- local circuit image problems;
- 2-CNF irredundant subsets and implication systems;
- CSP redundancy and minimal unsatisfiable/irredundant formulas;
- isoperimetry of the Boolean cube;
- proof-producing exhaustive generation and SAT Modulo Symmetries.

### 11. Limitations and open problems

- no general deterministic `NC0_3-Avoid` algorithm;
- no universal bounded depth;
- no completed `n=9` classification;
- no unrestricted lower bound;
- novelty pending review.

## Material to omit from the main narrative

- obsolete progress indices measuring distance to P versus NP;
- incomplete searches presented as confidence evidence;
- detailed version-by-version diary prose;
- unimplemented SMS/DRAT plans except as future-work notes;
- claims whose only support was retracted in V53.

## External-review package

Before submission:

1. run `verify_all.sh --full` in a clean environment;
2. reconcile every theorem statement against `LEDGER.json`;
3. produce one archive and SHA-256 manifest;
4. obtain at least one specialist review of the affine proof;
5. obtain at least one specialist review of the bijunctive construction and orientation-depth proof;
6. perform a dedicated prior-art review;
7. record all corrections before changing external-contact status.

## Suggested article boundary

The strongest coherent paper ends at V60. A future project on general lower bounds or hard-membership regimes should use a new directory, new state ledger and a new motivating reduction rather than silently extending this version sequence.
