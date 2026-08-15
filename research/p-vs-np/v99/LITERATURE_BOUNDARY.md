# V99 literature boundary

## Kuntewar--Sarma 2025

The primary source is Neha Kuntewar and Jayalal Sarma, *Avoiding Range via
Turan-Type Bounds*, APPROX/RANDOM 2025, LIPIcs 353:62.

Their Theorem 8 gives deterministic polynomial-time range avoidance for
monotone `NC0_3` circuits when `m>n`. V99 uses that theorem as a black box in
the conflict-free singleton-core branch.

For the majority subproblem, their Lemma 26 exhibits the alternating forbidden
edge coloring on `X_{2 ell}` and Corollary 27 carries it to loose X cycles. V99
does not re-claim that forbidden coloring. It asks what happens after each MAJ
gate is allowed independent literal signs and proves an internal switching-class
classification for the simple X structure.

The proceedings paper does not use the terms `unate`, `signed`, or `literal`
for such an extension. A targeted primary-source search also found no paper
formulating this signed/unate loose-X extension. This absence is not a novelty
proof.

## Signed-graph switching

Switching equivalence and the characterization of balanced signed graphs as
those switching to the all-positive signature are classical signed-graph facts,
usually associated with Harary and Zaslavsky. V98/V99 use that language to
organize incidence-direction constraints. No novelty is claimed for:

- switching signs at vertices;
- cycle-sign invariance;
- balance iff switching to all-positive;
- describing switching classes by cycle parities / first graph cohomology.

The research-specific candidate requiring external review is the exact range
behavior of the signed-majority simple X map under its four switching classes.

## Singleton-core theorem

The conflict certificate for two conjunctions demanding opposite literals is
elementary, and the conflict-free branch is an exact coordinate reduction to
the published monotone class. V99 treats the resulting full singleton-core
`m>n` algorithm as an internal integration theorem, not as a priority claim.

## Brakensiek correspondence boundary

The 12 August 2026 Brakensiek reply remains in force: generic polynomial
linear-dependence arguments should be treated as likely folklore / adjacent to
CSP sparsification. V99 does not use that route.

## Unrestricted benchmark

The Huang--Li--Zhong ITCS 2026 all-instance `k=3` benchmark retained by the
laboratory is `O(N*2^(N/2))`. V99 gives no unrestricted worst-case improvement.
