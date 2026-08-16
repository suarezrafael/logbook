# V104 scientific status

**Classification:** experimental frontier progress; not an official candidate.

Internally established symbolically:

- safe composition of a V101 distinct-head functional DAG with root-supported
  V103 affine-hull equations;
- deterministic `O(2^eta poly(N))` avoidance given a valid hybrid certificate,
  where `eta=n-f-R`;
- polynomial-time verification of a supplied certificate;
- explicit connected exact-stretch family with `eta=3` while `lambda`, `mu`,
  `beta`, and `nu` are all linear in the family parameter.

Sanity checks completed before registration:

- complete original-range checks for the strict family at `k=1` and `k=2`;
- structural rank/connectivity identities through `k=20`.

Not yet established:

- repository-CI passage of the larger V104 primary/independent verifier suites;
- a polynomial/FPT detector for an optimal hybrid certificate;
- any worst-case sublinear bound on `eta` for arbitrary circuits;
- unrestricted polynomial-time `NC0_3-Avoid`;
- novelty, priority, peer review, a new circuit lower bound, or P versus NP.
