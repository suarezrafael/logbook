# Laboratory V97 — comparison-free peeling kernels

V97 continues the V95/V96 stop rule: do not reproduce the PP-hard exact V92
canonical trajectory.  Instead, simplify a positive-surplus support component
by reductions that preserve the existence of an avoided output and enumerate
only the residual kernel.

## Main result

After essential-support normalization, repeatedly apply:

```text
unused input deletion,
leaf input + its unique output deletion,
constant-output termination,
essential-unary output forcing and substitution.
```

Let `lambda(C)` be the smallest number of inputs left by this deterministic
reducer among positive-surplus support components.  Then V97 gives a fully
deterministic comparison-free avoider in

```text
O(2^lambda(C) * poly(N)).
```

Thus `lambda=O(log N)` is a polynomial-time regime.

V96 used the size `rho(C)` of the smallest original positive-surplus component.
V97 proves `lambda<=rho` and gives an explicit exact-stretch family with one
connected positive-surplus component satisfying

```text
rho=N,
lambda=ceil(log_2 N).
```

The family uses essential parity-of-three gates, so it is genuinely ternary and
nonmonotone.  V97 therefore gives a strict parameterized extension of the V96
component enumerator rather than only changing constants.

## Literature calibration

The 2025 Kuntewar--Sarma Turan-type framework already gives deterministic
polynomial-time range avoidance for monotone `NC0_3` circuits whenever `m>n`.
That result is stronger on the monotone class.  The V97 strict family is
nonmonotone and is used only to demonstrate the new peeling parameter.

V84 already supplied an `FP^NP` small-Hall-witness route.  V97 does not claim a
new general Hall extractor; it removes the oracle on a structural family where
leaf/unary reductions expose the small deficient kernel directly.

The unrestricted comparison remains the Huang--Li--Zhong `k=3` all-instance
runtime `O(N*2^(N/2))`.  V97 can beat it exponentially on favorable instances
but does not improve that worst-case bound.

## Files

- `peeling_kernel.py` — executable reducer, constructor, and audits;
- `RESULTS.json` — immutable regression snapshot;
- `THEOREMS.md` — symbolic safe-reduction and runtime proofs;
- `LITERATURE_BOUNDARY.md` — current prior-art calibration;
- `IMPLICATION.json` — conservative implication declaration;
- `verify.py`, `verify_independent.py` — primary and independent gates;
- `V97_PEELING_KERNEL_THEOREM.tex` — formal theorem module;
- `V98_CORE_CONTEXT.md` — next irreducible-kernel/Turan-label frontier.

## Nonclaims

No unrestricted polynomial-time `NC0_3-Avoid` algorithm, no worst-case runtime
improvement, no triggered circuit-lower-bound transfer, no novelty or peer-review
claim, and no P-versus-NP resolution.
