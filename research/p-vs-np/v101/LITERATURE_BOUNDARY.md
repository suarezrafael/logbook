# V101 literature boundary

## Relation to V100 and Kuntewar--Sarma

V100 already generalized a published monotone forced-input deletion pattern to
constant and copy/negation substitutions that preserve locality three. V101
does something different when the forced relation depends on two variables: it
does **not** compose that function into neighboring gates. It stores selected
relations globally as a functional dependency DAG and enumerates only the DAG
roots.

The general principle “acyclic functional dependencies are determined by root
variables” is elementary and may be folklore. No novelty is claimed for that
principle or for DAG evaluation.

## Relation to V85

V85 isolated 56 balanced non-affine ternary predicates by Fourier behavior.
V101 penetrates 24 of those 56: the `0x1e` graph-of-AND orbit has a total
functional fiber. The 32 balanced/non-affine predicates still invisible to
functional anchors are exactly signed majority (`0x17`) and the mux/bijunctive
selector orbit (`0x1b`).

Thus V101 changes the constructive frontier from “all balanced non-affine” to a
smaller two-orbit class, but it does not invalidate V85's Fourier theorem.

## Relation to V56--V62

Earlier laboratories studied bijunctive fibers and proved that fixed-fiber
block redundancy can fail in infinite families. V101 again avoids a redundancy
claim: it only needs selected functional graph relaxations and a small root set.
The remaining `0x1b` orbit is precisely where this functional projection test
fails, making the old implication-graph perspective newly relevant.

## Novelty discipline

No external source found so far establishes the V101 `functional-anchor`
terminology or exact 186/32 integration theorem. That absence is not evidence of
novelty. The result remains an internal, reproducible theorem pending targeted
prior-art review.
