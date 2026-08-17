# V107 literature boundary

## Current range-avoidance calibration

The laboratory rechecked the primary range-avoidance line before elevating the
V107 signed-majority theorem.

Kuntewar--Sarma, *Range Avoidance in Boolean Circuits via Turan-type Bounds*
(ECCC TR25-034, 2025), gives deterministic polynomial-time monotone `NC0_3`
avoidance at exact positive stretch, a symmetric `NC0_3` regime at larger
stretch, and a majority special case at quadratic stretch.  The V107 candidate
is therefore potentially stronger for the very specific class of **essential
ternary signed-majority** outputs, but no novelty claim is made.

The general `NC0_3-Avoid` frontier remains calibrated against
Gajulapalli--Golovnev--Nagargoje--Saraogi, *Range Avoidance for Constant-Depth
Circuits: Hardness and Algorithms* (ECCC TR23-021), and later algorithmic work.
V107 does not close that general problem.

## Standard ingredients

No novelty is claimed for:

- Rado's matroid marriage theorem;
- unweighted matroid intersection;
- signed/biased graphs and signed-frame matroids;
- the frame-matroid rank formula and handcuff circuits;
- 2-SAT implication graphs / SCC unsatisfiability;
- path suppression by XOR transport composition;
- exhaustive computer-assisted verification of a constant kernel.

Modern frame-matroid references checked in the laboratory include
Chen--DeVos--Funk--Pivotto, *Graphical representations of graphic frame
matroids* (arXiv:1403.7733), together with standard biased-graph literature.

## What requires external validation

The exact composition that needs specialist scrutiny is:

1. support Hall inequalities become candidate-pair frame-rank inequalities
   because every majority candidate triangle is unbalanced;
2. deleting one gate from a minimal-surplus block yields a constructible
   frame-independent transversal;
3. rank tightness turns every component into an unbalanced unicyclic graph;
4. one omitted majority gate either joins two such components or interacts with
   one of them through a three-terminal kernel;
5. every such kernel compresses to at most six virtual paths;
6. the 16,032-case generated finite kernel check covers all reduced signed
   configurations and lifts soundly to the original gates.

Targeted searches did not locate this exact exact-stretch signed-majority
construction.  Search absence is not evidence of novelty or priority.

## Validation target

Before any public novelty statement, ask range-avoidance / Boolean-CSP / matroid
experts whether the following theorem is known under another formulation:

> Essential ternary signed-majority `NC0_3-Avoid` is deterministically
> polynomial-time solvable for every positive stretch `m>n`, via a
> signed-frame-matroid transversal and a constant three-terminal unicyclic
> implication kernel.

A stronger validation would independently reimplement the 164-kernel generator
and 16,032 signed/polarity census or formalize the finite lemma in a proof
assistant.
