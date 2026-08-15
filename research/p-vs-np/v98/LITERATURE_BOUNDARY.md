# V98 literature and external-validation boundary

## Kuntewar--Sarma, APPROX/RANDOM 2025

Neha Kuntewar and Jayalal Sarma, *Avoiding Range via Turan-Type Bounds*,
APPROX/RANDOM 2025, LIPIcs 353:62.

The published paper proves deterministic polynomial-time range avoidance for
monotone `NC0_3` circuits whenever `m>n`. Its hypergraph interface separates a
support structure from the gate-label question: a useful subhypergraph must
carry an edge coloring that no vertex coloring induces through the local gate
labels. Their linear-hypergraph theorem supplies loose-X structure; the
monotone analysis supplies the forbidden coloring.

V98 uses the monotone algorithm only as a black box after an exact coordinate
switching. It does **not** claim the published monotone theorem.

A targeted search of the paper did not reveal an explicit unate/switching
extension. Absence from one paper is not evidence of novelty, so V98 records
the switching theorem as an internal observation pending broader prior-art
review.

## Why the parity obstruction matters

The V98 parity construction shows that an arbitrary-label extension cannot say

```text
loose X exists  =>  some edge coloring of that X is unrealizable.
```

For parity labels on the explicit loose X, every edge coloring is realizable.
The exact-stretch completion merely shows that this local obstruction can live
inside a V97-irreducible positive-surplus component.

This does not make parity hard. Affine/parity range avoidance is algebraic and
is already on the laboratory's easy side.

## Brakensiek correspondence, 12 August 2026

Joshua Brakensiek replied to the laboratory's earlier arity-4 non-redundancy
questions and explicitly confirmed the interpretation that the seven previously
mapped predicates have non-redundancy `Theta(n^3)`. He noted that their
terminology does not use the adjective “homogeneous” for this.

On the separate zero-set-polynomial linear-dependence observation, he did not
claim novelty. He said he would presume the technique folklore in the
range-avoidance context and pointed to analogous polynomial/dependence methods
in CSP sparsification, including:

- Jansen--Pieterse, *Optimal Sparsification for Some Binary CSPs Using
  Low-Degree Polynomials*, MFCS 2016, Section 3;
- Chen--Jansen--Pieterse, *Best-case and Worst-case Sparsifiability of Boolean
  CSPs*, arXiv:1809.06171, Section 3;
- Khanna--Putterman--Sudan, *Efficient Algorithms and New Characterizations for
  CSP Sparsification*, arXiv:2404.06327, Section 9.

Accordingly, V98 treats polynomial linear-dependence avoidance as
CSP-sparsification-adjacent folklore unless a stronger novelty review says
otherwise. The parity host in this version is used only as a falsifier for a
support-only loose-X claim.

The email is external expert feedback, not peer review and not a publication.

## Huang--Li--Zhong benchmark

The unrestricted `k=3` benchmark retained by the laboratory is the
Huang--Li--Zhong all-instance algorithm

```text
O(N*2^(N/2)).
```

V98 establishes a polynomial subclass but does not improve that worst-case
bound.

## Novelty discipline

No novelty claim is made for:

- switching unate gates to monotone gates by consistent input/output
  complements;
- the XOR-cycle recognition test;
- affine/parity missing-output construction;
- the CSP polynomial-dependence technique.

The new value of V98 inside this laboratory is the precise integration of these
facts with the V97 irreducible-kernel frontier and the resulting positive/negative
classification of the next Turan-label step.
