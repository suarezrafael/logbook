# V112 core context — target compatibility over the flow polytope

## Promoted input to V112 if V111 passes

V111 shows that unboundedly many shared MUX bottlenecks are not themselves the obstruction.  A two-unit min-cost return flow can cross `d=Theta(n)` shared gates and still give a polynomial missing-output certificate when all shared target requirements agree.

## Remaining obstruction

For a fixed repeated selector and opposite first phases, the deterministic minimum-cost flow chosen by V111 may be target-incompatible even though:

1. another decomposition of the same integral min-cost flow may be compatible;
2. another equal-cost min-cost flow may be compatible; or
3. a slightly higher-overlap flow may be compatible.

V111 does not decide those possibilities.

## Track A — compatibility on the optimal-flow face

Represent each selected branch implication by its required target bit.  Study whether all minimum-cost two-flows can be compressed into a polynomial state graph whose states record only the phase obligations at currently shared gates.

Target: a polynomial algorithm that either finds a target-compatible minimum-overlap pair or certifies none exists among all optimum flows.

## Track B — 2-SAT / parity exchange

For a shared gate, incompatibility is one Boolean disagreement.  Search for an exchange theorem showing that residual cycles of the min-cost flow can flip route choices and repair disagreements.  Model the exchange choices as 2-SAT, parity constraints, or a signed residual graph.

Target: prove that compatibility on the optimum-flow face reduces to a polynomial Boolean system.

## Track C — hardness falsification

Before assuming Track A/B is possible, search for a reduction from a known hard path-selection / labeled-path problem into target compatibility among equal-cost two-flows.  The generic Minimum Shared Edges literature warns that shared-path optimization becomes hard outside the exact flow structure used by V111.

Target: either a small scalable hardness gadget or a proof that the MUX phase symmetry rules such gadgets out.

## Track D — bounded excess overlap

If optimum-flow compatibility is hard, parameterize by

```text
Delta = compatible overlap cost - unconstrained minimum overlap cost.
```

Seek `O(c^Delta poly(N))` with a strict family where `Delta=O(1)` but V111's deterministic optimum is incompatible.

## Stop rule

Do not promote V112 from a larger random census.  Require at least one of:

- a polynomial compatibility algorithm over all minimum-cost flows;
- an FPT theorem in a new compatibility/excess parameter with strict asymptotic separation;
- a rigorous hardness/barrier result for target-compatible flow selection;
- a structural exchange theorem that strictly enlarges V111 on an infinite family.

All-MUX, unrestricted `NC0_3-Avoid`, and P versus NP remain open unless separately proved.
