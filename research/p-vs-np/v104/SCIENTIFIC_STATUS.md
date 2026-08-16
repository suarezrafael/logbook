# V104 scientific status

**Classification:** experimental frontier progress; not an official candidate.

Internally established symbolically:

- safe deterministic composition of canonical affine-hull rank with functional
  graph compression by protecting every variable used by the affine basis;
- polynomial-time affine-first preprocessing that computes rank `R`, then
  greedily chooses `f` unprotected distinct functional heads while preserving
  acyclicity;
- deterministic `O(2^eta_AF poly(N))` avoidance with the computable parameter
  `eta_AF=n-R-f`;
- explicit connected exact-stretch family with `eta_AF=3` while V97 `lambda`,
  V101 `mu`, V102 `beta`, and V103 `nu` are all linear.

Falsification completed before candidate registration:

- 1,800 random exact-stretch circuits with `2<=n<=7` checked against complete
  original ranges under the canonical algorithm: zero failures;
- complete strict-family original-range checks for `k=1` and `k=2`;
- canonical strict-family `eta_AF=3` checked for `k=1..7`;
- 712 additional random residual-output mutations checked against complete
  original ranges: zero failures;
- structural rank/connectivity identities through `k=20`.

Not yet established:

- repository-CI passage of V104 verifiers aligned to the canonical routine;
- any worst-case sublinear bound on `eta_AF` for arbitrary circuits;
- unrestricted polynomial-time `NC0_3-Avoid` or an improved unrestricted
  published worst-case exponent;
- novelty, priority, peer review, a new circuit lower bound, or P versus NP.
