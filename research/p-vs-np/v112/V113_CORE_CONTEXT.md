# V113 core context — compatibility beyond serial MUX phase transfer

## Input from V112

V112 establishes two facts that should be treated as the starting point, not rediscovered:

1. minimum gate overlap does **not** determine target compatibility — one exact-stretch serial instance can have compatible and incompatible flows at the same optimum overlap;
2. when the return network decomposes into a serial chain of two-lobe blocks, target compatibility factorizes into constant-size local phase-transfer decisions and is solvable in linear time.

Thus the remaining problem is the non-serial optimum-flow face.

## Small control

Maintain a tiny signed MUX control with `n=4,m=5` where overlap minimum is one and the same first-gate pair has both compatible and incompatible optimum return pairs.  The deterministic V111 choice is incompatible.  This is a regression target against any false claim that all optimum decompositions have the same phase behavior.

## Track A — zero-cost residual exchanges

Given a minimum-overlap two-flow, characterize every equal-cost optimum by zero-reduced-cost residual cycles.  Each shared MUX gate has a binary target-mode requirement.  Determine whether compatibility across all optimum flows can be expressed as:

- a parity system over residual exchanges;
- 2-SAT over exchange choices;
- or a signed residual graph with a polynomial consistency test.

Target: decide whether **some** minimum-overlap flow is target-compatible, not merely whether the canonical flow is compatible.

## Track B — dominator/block decomposition

V109 produced one-gate dominators; V112 solves a pure serial chain of such separators.  Compute the dominator tree / two-flow block decomposition of an arbitrary one-SCC return network.

Target: prove that every separator-chain block is handled by phase transfer and isolate the first genuinely 2-connected compatibility core.  A provably shrinking recursive decomposition would be a material advance even without solving the core.

## Track C — hardness falsification

Do not assume optimum-face compatibility is polynomial.  Generic forbidden-pair and labeled-path problems have strong hardness results even on restricted DAGs.  Attempt a reduction only into the **actual MUX branch-transition structure**; hardness of a broader abstract path problem is not enough.

Target: either a rigorous MUX-compatible hardness gadget or a proof that MUX phase symmetry prevents the known path-selection gadgets.

## Track D — conflict/excess parameters

If the general optimum face is hard, define parameters that V112 does not already trivialize:

```text
chi = minimum number of shared-gate target conflicts in an optimum-overlap flow,
Delta = minimum compatible overlap - unconstrained minimum overlap.
```

Seek a fixed-parameter algorithm only if the parameters are algorithmically checkable or come with a verifiable certificate.  Require a strict infinite family where V111/V112 fail structurally but `chi` or `Delta` stays small.

## Stop rule

Do not promote V113 from a larger random census.  Require at least one of:

- a polynomial algorithm over all optimum flows for a non-serial class;
- a dominator/block theorem with provable shrinking and a strictly smaller residual core;
- a rigorous hardness/barrier result under the exact MUX transition structure;
- an FPT compatibility theorem with a meaningful parameter and strict infinite-family separation.

All-MUX, unrestricted `NC0_3-Avoid`, and P versus NP remain open unless separately proved.
