# V116 scientific status

## Candidate result

V116 proves a structured polynomial-time theorem for fixed opposite-phase signed-MUX first pairs at excess-overlap budget one.

Let the V113 common gate-dominator decomposition define the non-common dominator stages. If every such stage has **feedback-gate number at most one**—that is, deleting at most one non-common output gate makes the stage branch graph acyclic—then target-compatible overlap at most `minimum_overlap+1` is decidable in polynomial time and a witness is constructible.

This strictly extends V115: V116 includes genuinely cyclic stages.

## Mechanism

A one-feedback stage is reduced to a bounded collection of fixed-request linkage problems in a DAG. After enumerating the feedback gate, the optional unique excess shared gate, their route order and branches, deleting those special gates leaves at most five gate-disjoint DAG requests. A product-state token dynamic program solves those requests in polynomial time because the request count is bounded by five.

The outer V113 phase DP still needs only the branch pair at the current common gate and one global excess-budget bit.

## Strict separation

V116 contains an infinite exact-stretch family with

```text
n = 8+t
m = 9+t = n+1
minimum_overlap = 1
minimum_target_compatible_overlap = 2
Delta = 1
```

and a genuine final-stage cycle `left -> split -> left`. The stage has feedback-gate number one, V115 is inapplicable, V113 rejects the entire minimum-overlap face, and V116 accepts with one extra shared gate.

## Verification status

Primary verification:

- direct cross-check on 300 seeded small `tau_g<=1` fixed-pair instances against exhaustive gate-simple return-route enumeration;
- strict cyclic family through depth 40;
- V113 optimum-face rejection and V115 non-applicability controls;
- exact-stretch and complete original-range target check.

Independent verification:

- imports no V116 implementation;
- reconstructs the strict family independently;
- exact return-route census through depth 60;
- independent feedback-cycle/deletion audit;
- independent full-image target check.

Finite verification supports the implementation and catches construction mistakes; it is not the proof of the theorem.

## Parameterized boundary

The same decomposition gives a straightforward XP direction for feedback-gate number `tau`: after enumerating visits to a feedback set, the residual DAG linkage has `O(tau)` fixed requests and can be solved in `N^{O(tau)}` time. V116 does not promote this to FPT. Generic DAG disjoint-path routing is known to be parameterically hard when the number of requests varies, so a true `f(tau) poly(N)` theorem requires additional signed-MUX/two-route structure.

## Global nonclaims

V116 does not establish arbitrary-`tau` FPT, unrestricted cyclic-stage tractability, all MUX `0x1b` avoidance in P, unrestricted `NC0_3-Avoid`, a general circuit lower bound, or a resolution of P versus NP. Novelty, priority and peer review remain unconfirmed.
