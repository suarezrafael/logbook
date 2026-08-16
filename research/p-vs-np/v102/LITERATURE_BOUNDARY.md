# V102 literature boundary

## Strong backdoors are established prior art

The term and paradigm of strong backdoor sets long predate this laboratory. The SAT/CSP literature defines a strong backdoor as a variable set such that every assignment to it reduces the instance to a tractable base class; enumerating the assignments gives an FPT evaluation algorithm. Gaspers, Misra, Ordyniak, Szeider and Zivny (arXiv:1509.05725) survey this framework and study FPT detection for bounded-domain/bounded-arity CSP backdoors, including affine polymorphism classes.

V102 therefore makes **no novelty claim** for:

- the notion of a strong backdoor;
- enumerating all assignments to a small backdoor;
- Gaussian elimination for affine Boolean constraints;
- bounded-search-tree detection from constant-size local obstructions.

## What V102 specializes to range avoidance

The internal theorem combines that classical backdoor idea with the range-avoidance prefix invariant:

1. after a backdoor assignment, every output-prefix condition is an affine system;
2. exact prefix *preimage counts* are summed across the disjoint backdoor branches;
3. choosing the smaller child repeatedly halves the count from `2^n` to below one because `m>n`.

The exact `0x1b` selector rule, signed-majority two-of-three rule, and the strict `beta=1` family are the laboratory-specific integration points.

## Current range-avoidance calibration

Guruswami--Lyu--Wang (ECCC TR22-102) give polynomial-time `NC0_2-Avoid` and pseudorandomness-based algorithms for broader low-depth classes.

Gajulapalli--Golovnev--Nagargoje--Saraogi (ECCC TR23-021 / arXiv:2303.05044) keep `NC0_3-Avoid` open at small stretch and give deterministic algorithms at much larger stretch, while connecting smaller-stretch algorithms to rigid-matrix constructions.

Kuntewar--Sarma (ECCC TR25-034 / arXiv:2503.17114) prove deterministic linear-stretch avoidance for monotone `NC0_3` and a high-stretch result for majority gates. Their result is stronger than V102 on monotone circuits; V102 concerns a structural parameter that includes nonmonotone MUX/signed-majority residuals.

Huang--Li--Zhong (ECCC TR25-049, revision 5) give improved general local algorithms and subexponential algorithms at superlinear stretch. V102 does not improve their unrestricted worst-case exponent.

A targeted search through August 2026 did not locate a source explicitly stating the V102 strong-affine-backdoor range-avoidance parameter or the exact residual `0x17/0x1b` integration. This is not evidence of novelty; external expert review is still required.
