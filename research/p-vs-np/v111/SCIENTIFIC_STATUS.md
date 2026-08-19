# V111 scientific status

## Established inside the candidate package

- Two opposite-phase MUX return cycles may share arbitrarily many output gates and still give a sound missing-output certificate when every shared gate receives the same target requirement from both cycles.
- A two-unit min-cost return network with cost zero for first use and cost one for second use computes a minimum-overlap integral flow in polynomial time.
- The deterministic V111 recognizer constructs a missing word whenever its selected minimum-cost decomposition is target-compatible.
- Infinite `k=2` nested-chain family with `n=5(d+1)`, `m=n+1`, and minimum overlap exactly `d`.
- On that family V109 returns a bottleneck; for `d>=2`, V110 returns a nested bottleneck; V111 succeeds for arbitrary `d`.
- Exact V102 affine-backdoor size on the family: `beta=3(d+1)=3n/5`.
- Primary and independent verifier suites included.

## Deliberately not established

- Completeness of the deterministic min-cost decomposition for all instances that possess some target-compatible flow pair.
- Polynomial search over all equal-cost decompositions or higher-cost compatible reroutings.
- All phase-conflict cases.
- All nested-bottleneck MUX circuits.
- All essential MUX/bijunctive `0x1b` circuits.
- Unrestricted `NC0_3-Avoid`.
- Any new general circuit lower bound.
- P versus NP.

## Validation status

No novelty, priority, or peer-review claim is made.  The path-optimization primitive is calibrated against prior min-cost-flow / shared-edge literature; the range-avoidance-specific object requiring validation is the MUX target-compatibility and missing-word lifting argument.
