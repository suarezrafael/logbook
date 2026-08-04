# Laboratory V90 — finite entropy certificate, barrier audit, and closure of `Eval_H`

## Classification

V90 is a **barrier-and-closure laboratory**, not a completed frontier advance.

Its mathematical component converts the V89 infinitesimal Hessian statement into a rigorous finite neighborhood. Its governance component applies the implication-ratio rule and closes the `Eval_H` constructor front because the declared material-advance condition was not met.

## Implication ratio

The intended chain was:

```text
global seven-state entropy contraction at some c0>1
  -> basis-colorability of the V87 random support model with high probability
  -> one support family covering every target list of at most eight rows
  -> support-only constructor lower bound at least nine.
```

The first global implication remains open, fixed-edge second-moment bookkeeping remains open, and no closed implication from the nine-row internal bound to a recognized circuit lower bound is known. Consequently V90 is not counted as frontier progress.

See `IMPLICATION.json` and the repository-wide `IMPLICATION_POLICY.md`.

## Finite local theorem

Let `B` be a `7x7` doubly stochastic overlap matrix, let `U` be the uniform matrix, and set `C=B-U`. Define

```text
D(B) = ln(7) - H(B)/7,
L(B) = ln(q(B)/(24/49)^2).
```

The exact Hoeffding decomposition gives

```text
q(B)
  = (24/49)^2
    + (48/2401)||C||_F^2
    + T_3(C),
```

with

```text
|T_3(C)| <= (312/2401)||C||_(2->2)^3.
```

For

```text
||B-U||_F <= 1/5,
```

strong convexity of row entropy yields

```text
D(B) >= (5/24)||C||_F^2,
```

while the spectral envelope and `ln(1+x)<=x` give

```text
L(B) <= (23/120)||C||_F^2.
```

Therefore, at the explicit density

```text
c0 = 21/20,
```

we obtain

```text
D(B) - (21/20)L(B)
  >= (17/2400)||B-U||_F^2.
```

This certifies a genuine finite ball around the uniform overlap. V89 had only the exact local Hessian.

## Exact decomposition data

For the ordered-basis indicator on three independent uniform nonzero vectors of `F_2^3`:

```text
basis probability                  = 24/49,
variance                           = 600/2401,
one pair-component norm squared   = 96/2401,
total degree-two norm squared     = 288/2401,
degree-three norm squared         = 312/2401.
```

The pair component equals `-24/49` on the diagonal and `4/49` off the diagonal. An exact 36-dimensional tangent audit checks all 1,296 bilinear pairs and reconstructs the relative quadratic coefficient `1/12` with zero mismatches.

## Remaining mathematical gap

The exterior region

```text
||B-U||_F > 1/5
```

inside the `7x7` Birkhoff polytope remains uncertified. The `GL(3,2)`-invariant diagonal/off-diagonal family remains only a diagnostic family; no theorem says every maximizer lies in it.

The literature audit did not locate a checked strong-colorability theorem whose stated hypotheses cover the required case `k=3`, four colors, and edge density one. This is a boundary statement, not a proof that no such theorem exists.

## Natural-proofs barrier audit

`NATURAL_PROOFS_BARRIER.md` records the corrected conclusion:

- a polynomially checkable certificate on circuit presentations is not automatically a Razborov–Rudich natural property;
- constructivity, largeness, usefulness, and representation independence must all be proved;
- nevertheless, the Hall/syndrome/width ladder has a natural-proof-like research profile and is closed as an open-ended certificate program.

## Stop-rule decision

The V89/V90 budget required one of:

1. a superconstant support-only constructor lower bound;
2. a constructive `O(n^(1/3))` list;
3. a rigorous asymptotic eight-row bridge with material consequences.

V90 obtained none of these. The stop rule therefore fires. `Eval_H` is closed after V90 unless a new externally recognized implication chain is supplied.

## Next laboratory

`V91_CORE_CONTEXT.md` defines a Williams-style feasibility audit. It must quantify an exact SAT/#SAT or Missing-String transfer theorem, identify a standard circuit class, and compare the required runtime saving with the present branchwidth engine.

The inherited engine is currently polynomial only for support branchwidth `O(sqrt(log m))`; V87 contains relevant linear-branchwidth families. Thus no Williams consequence follows from the current algorithms without a new structural reduction or a different target class.

## Files

- `local_global_entropy.py` — exact decomposition and local certificate generator;
- `RESULTS.json` — immutable result snapshot;
- `verify.py` — primary verifier;
- `verify_independent.py` — independent brute-force and policy verifier;
- `IMPLICATION.json` — machine-readable implication ratio and stop decision;
- `IMPLICATION_AUDIT.md` — retroactive V80–V90 classification;
- `NATURAL_PROOFS_BARRIER.md` — precise barrier statement and governance consequence;
- `V91_CORE_CONTEXT.md` — next-front feasibility audit.

## Nonclaims

V90 does not prove the global overlap inequality, random-model basis-colorability, a nine-row constructor lower bound, a constructive universal list, a new circuit lower bound, novelty, peer review, or `P != NP`.
