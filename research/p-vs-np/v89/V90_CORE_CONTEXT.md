# V90 core context — final budgeted Eval_H constructor laboratory

V90 is reserved after the promotion of V89. It is the final result-oriented
laboratory on the current `Eval_H` constructor front.

## Trajectory classification

V90 is classified as a final bridge-or-barrier attempt, not an open-ended
certificate search. Its only admissible trajectory claim is:

```text
Eval_H constructor theorem
  -> constructive support-only target list or a growing constructor lower bound
  -> an explicitly cited rigidity, remote-point, or lower-bound bridge.
```

If no such bridge is closed, V90 remains a legitimate barrier/closure
laboratory but is not counted as movement toward a circuit lower bound.

No new generic Hall, syndrome, width, coloring, peeling, or other
polynomially-verifiable certificate family may be opened inside V90. The
remaining budget is restricted to the frozen overlap problems, the stated
superconstant lower-bound target, or a source-matched external bridge.

## Frozen V89 contribution

V89 establishes:

1. target-independent injective addressing covers every target matrix;
2. an `F_2^3` basis coloring yields eight injective affine rows;
3. primal four-colorability is a sufficient special case;
4. eight is the exact target-independent ceiling for ternary supports;
5. all V80 and deterministic V87 controls are basis-colorable;
6. the controls are not primal-four-colorable;
7. strong four-coloring reduces to an exact cubic overlap objective;
8. the strong-four uniform overlap is locally stable below density `3/2`;
9. empty 3-core does not imply basis colorability;
10. an eight-vertex empty-core obstruction is minimal through seven vertices;
11. even linear empty-core supports admit an exact basis-coloring obstruction;
12. the full seven-state basis CSP has an exact `7x7` overlap objective;
13. its uniform overlap is locally stable below density `6`;
14. both global overlap inequalities and the asymptotic V87 bridge remain open.

## Priority one — global seven-state entropy contraction

For a `7x7` doubly stochastic overlap `B`, define

```text
q(B)=7^-3 sum_{x,y ordered bases}
     B[x1,y1] B[x2,y2] B[x3,y3],

D(B)=ln(7)-H(B)/7,
L(B)=ln(q(B)/(24/49)^2).
```

The relative exponent is

```text
Psi_c(B)=-D(B)+cL(B).
```

The exact local expansion at the uniform matrix `U` is

```text
Psi_c(U+tDelta)
  = -(6-c)t^2 ||Delta||_F^2/12 + O(t^3).
```

Thus the target density one has a strict local margin `5/12`. The main V90
target is to prove

```text
sup_{B != U} L(B)/D(B) < 1.
```

Any explicit bound below one gives a fixed `c0>1`. For example,
`L(B)<=D(B)/2` would certify the balanced exponent through density two.

Acceptable closures:

- an analytic entropy-contraction or strong-data-processing inequality;
- a rigorous interval or sum-of-squares certificate over the `7x7` Birkhoff
  polytope;
- a symmetry reduction proving that the extremizer belongs to a tractable
  orbit family;
- a concrete overlap with positive exponent at density one.

A global inequality must still be followed by the standard balanced-overlap,
boundary, and fixed-edge second-moment bookkeeping.

## Priority two — strong-four fallback

For a `4x4` doubly stochastic matrix `B`,

```text
Phi_c(B)
  = H(B)/4 - ln(4)
    + c ln(4(2 + sum_ij B_ij^3)/9).
```

The uniform overlap is locally stable below `3/2`, but the diagonal-family
transition near `1.086445` leaves less room than the seven-state formulation.
The strong-four route remains valid if its global inequality is easier to
certify.

## Closed shortcut — universal core peeling

The V87 density is below the random 3-core threshold, but the universal
implications

```text
empty 3-core => basis-colorable,
linear empty 3-core => basis-colorable
```

are both false. The committed eight- and twelve-vertex obstructions close this
shortcut. Because each fixed obstruction occurs with vanishing probability in
the sparse random model, a genuinely random-specific structural theorem is not
logically excluded, but it is now secondary to the exact overlap program.

## Priority three — superconstant constructor lower bound

Even a nine-row result is constant. Seek a mechanism that grows with `n`, or
prove a lower bound for a precise constructor class whose parameter grows and
whose relevance is stated through a source-verified implication chain.

## Stop rule

If V90 produces neither:

- a superconstant constructor lower bound;
- a constructive `O(n^(1/3))` list;
- nor a rigorously closed bridge with material consequences beyond the
  constant nine-row bound,

then close the `Eval_H` constructor front.

The stop rule cannot be reset by:

- a larger finite census;
- a new constant-row bound;
- a different polynomially checkable certificate;
- a constant-factor width or state-count optimization;
- a heuristic overlap scan without a rigorous global conclusion.

## Mandatory V91 transition

After V90, the next laboratory is V91, a reorientation laboratory. It must not
begin with a new result search. It must first execute the documents reserved in
this directory:

- `V91_CORE_CONTEXT.md`;
- `TRAJECTORY_GATE_TEMPLATE.md`;
- `NATURALNESS_AND_BARRIER_AUDIT.md`;
- `ALGORITHM_TO_LOWER_BOUND_AUDIT.md`;
- `METACOMPLEXITY_REDUCTION_LEDGER.md`;
- `EXTERNAL_VALIDATION_PLAN.md`.

V91 will rank three possible continuations only after their implication and
barrier audits:

1. SAT or `#SAT` algorithms tied to a Williams transference theorem;
2. range-avoidance and remote-point reductions in meta-complexity;
3. bounded-arithmetic or proof-complexity parameter matching.

The algorithms-to-lower-bounds audit is the primary front. Meta-complexity is
the secondary front. External validation is permanent.

## Nonclaims

Local Hessian stability, finite scans, empty random cores, and the absence of
fixed obstructions do not prove asymptotic basis colorability and are not
evidence that `P != NP`.

The V91 reservation does not claim that the V85--V89 certificates formally
satisfy the Razborov--Rudich definition, that the V74--V77 engine already gives
a Williams-qualified SAT algorithm, or that posting a note publicly constitutes
peer review.
