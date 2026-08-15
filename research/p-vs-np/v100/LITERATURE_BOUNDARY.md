# V100 literature boundary

## Guruswami--Lyu--Wang, APPROX/RANDOM 2022

Venkatesan Guruswami, Xin Lyu, and Xiuhan Wang, *Range Avoidance for Low-Depth
Circuits and Connections to Pseudorandomness*, APPROX/RANDOM 2022.

Their algorithmic results include deterministic polynomial-time range avoidance
for `NC0_2` circuits. V100 uses this theorem only as the final black box after
all peelable essential ternary gates have been eliminated.

## Kuntewar--Sarma, APPROX/RANDOM 2025

The closest published proof pattern is Theorem 22 of Kuntewar--Sarma. In their
reduction from monotone `NC0_3-Avoid` to `MAJ3-Avoid`, every non-MAJ monotone
ternary gate is handled by selecting an output value, fixing one or more input
values forced by that selection, deleting the output, and continuing with a
smaller positive-surplus circuit.

V100 should therefore not describe “delete an output after extracting a forced
input” as a novel proof idea. Its internal advance is the abstraction to
**literal-graph fibers** and the observation that copy/negation substitution
`x_v=x_u XOR c` also preserves locality three. This extends the safe reduction
to three non-unate NPN orbits and yields the exact 144/74 ternary gate-label
split. Prior-art status of that abstraction has not been externally established.

## V56--V62 internal boundary

The earlier laboratory established an infinite `0x07` family of consistent,
complete-block-irredundant 2-CNF fibers. That result is still correct. V100 does
not obtain a redundant block; it relaxes a selected fiber after retaining only
one forced literal relation. Thus the older barrier and the V100 algorithm
address different proof models.

## Novelty discipline

No novelty is claimed for:

- deterministic `NC0_2-Avoid`;
- monotone forced-variable elimination;
- Boolean input renaming/complementation;
- NPN equivalence itself.

External review is needed before claiming novelty for the five-orbit
literal-substitution theorem or the exact 144/74 preprocessing classification.
