# V90 core context — final budgeted Eval_H constructor laboratory

V90 is reserved while V89 remains a candidate.

## Frozen V89 contribution

V89 establishes:

1. target-independent injective addressing covers every target matrix;
2. an `F_2^3` basis coloring yields eight injective affine rows;
3. primal four-colorability is a sufficient special case;
4. eight is the exact target-independent ceiling for ternary supports;
5. all V80 and deterministic V87 controls are basis-colorable;
6. the controls are not primal-four-colorable;
7. strong four-coloring reduces to an exact cubic overlap objective;
8. the uniform overlap is locally stable for every density below `3/2`;
9. the global Birkhoff inequality and the asymptotic V87 bridge remain open.

## Priority one — close or kill the strong-four bridge

For a `4x4` doubly stochastic matrix `B`, define

```text
Phi_c(B)
  = H(B)/4 - ln(4)
    + c ln(4(2 + sum_ij B_ij^3)/9).
```

The first target is to prove or refute, for one explicit fixed `c0>1`,

```text
Phi_c0(B) <= 0
```

for every `B`, with equality only at the uniform matrix.

Acceptable closures:

- an analytic entropy/cubic inequality on the Birkhoff polytope;
- a rigorous interval or sum-of-squares certificate covering the full polytope;
- a line-by-line verified published theorem at `k=3,r=4,c0>1`;
- a concrete counterexample overlap with positive exponent.

A proof plus the standard second-moment bookkeeping must establish probability
bounded away from zero in the exact fixed-edge support model. Only then may the
V86/V87 high-probability barriers be intersected to raise the constructor lower
bound to nine.

## Priority two — seven-state basis CSP

If the strong-four route fails, analyze the more permissive CSP with domain
`F_2^3\{0}` and allowed constraints equal to ordered bases. Candidate routes:

- exact second-moment analysis of the `7x7` overlap;
- a core-peeling extension theorem;
- a rigorous coupling to a known symmetric random-CSP model;
- an explicit deterministic resistant family with a basis coloring.

Finite satisfiability of the eleven controls is not an asymptotic theorem.

## Priority three — superconstant constructor lower bound

Even a nine-row result is constant. Seek a mechanism that grows with `n`, or
prove a lower bound for a precise constructor class whose parameter grows.

## Stop rule

If V90 produces neither:

- a superconstant constructor lower bound;
- a constructive `O(n^(1/3))` list;
- nor a rigorously closed bridge with material consequences beyond the
  constant nine-row bound,

then close the `Eval_H` constructor front.

The next laboratory must return to one of:

1. rigidity or remote-point bridges;
2. average-case hardness tied to an established reduction;
3. bounded-arithmetic or proof-complexity parameter matching.

## Nonclaims

Local overlap stability and finite rational grids do not prove the global
second-moment inequality and are not evidence that `P != NP`.
