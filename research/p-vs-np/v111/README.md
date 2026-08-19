# Laboratory V111 — target-compatible minimum-overlap MUX flows

V111 extends the MUX flow line from V109/V110.

A fixed MUX output gives two exact 2-SAT clauses.  If two opposite-phase return cycles share output gates, they still form a valid missing-output certificate whenever every shared gate is assigned the same target bit by both cycles.

V111 therefore gives each output gate two unit-capacity copies in a return network:

```text
first use  cost 0
second use cost 1
```

A minimum-cost two-flow minimizes the number of output gates shared by the two return routes.  If the deterministic minimum-cost decomposition is target-compatible on all shared gates, V111 constructs a missing output in polynomial time.

## Strict nested-bottleneck family

For `k=2` and arbitrary depth `d>=1`, V111 builds an exact-stretch family with

```text
n = 5(d+1),
m = n+1,
minimum shared-gate overlap = d,
beta_V102 = 3(d+1) = 3n/5.
```

Every return route must cross all `d` shared hub MUX gates.  The canonical two routes share exactly those gates and require compatible targets on every one.

For `d>=2`, V109 returns a bottleneck and V110 still returns a nested bottleneck after upgrading the first shared gate.  V111 crosses all `d` bottlenecks at once using min-cost flow.

## Verification

`verify.py` executes the real V111 implementation, checks exact overlap on the nested family, compares missing words with complete ranges for the small members, verifies Hall minimality, exact small V102 beta, signed switchings, V109/V110 separation, and exhaustive V108 absence on the first two depths.

`verify_independent.py` does not import V111.  It reconstructs the family and canonical target, verifies unsatisfiability using an independent 2-SAT SCC engine through depth 100, checks complete ranges for the first two depths, independently audits Hall minimality, verifies the symbolic beta formula, and exhausts the V108 ignored-output search for the first two depths.

## Boundary

V111 is a sound polynomial recognizer, not a complete solver for all MUX circuits.  It does not prove that every instance admitting some compatible path pair is found by the particular deterministic minimum-cost flow chosen by the implementation.  The remaining front is to understand target compatibility across alternative equal-cost flows and the phase-conflict residual.

No novelty, priority, peer-review, unrestricted `NC0_3-Avoid`, general circuit-lower-bound, or P-versus-NP claim is made.
