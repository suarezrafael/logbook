# V104 scientific status

**Classification:** frontier progress; official V104 candidate pending repository promotion gates.

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
- structural rank/connectivity identities through `k=20`;
- explicit canonical inconsistent-hull witness regression in both primary and
  independent implementations.

Operational state:

- V103 is promoted and merged on `main`;
- V104 is the current candidate registered in `LAB_STATUS.json`;
- primary and independent verifiers plus the standalone theorem module are
  registered in the repository runner/LaTeX contracts;
- promotion requires the normal draft quick/LaTeX gates, then ready-PR
  compatibility/full gates and a clean final review state.

Not established:

- any worst-case sublinear bound on `eta_AF` for arbitrary circuits;
- unrestricted polynomial-time `NC0_3-Avoid` or an improved unrestricted
  published worst-case exponent;
- novelty, priority, peer review, a new circuit lower bound, or P versus NP.
