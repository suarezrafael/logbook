# V113 — common-dominator optimum-flow DP

V113 closes the exact completeness gap left by V111/V112 **inside the minimum-overlap face** of a fixed opposite-phase MUX first-branch pair.

## Main result

For return destinations `d0,d1` and root selector `v`, let `H` be the output gates used by every `d0 -> v` route and every `d1 -> v` route. These are the common gate dominators.

V113 proves

```text
minimum return-gate overlap = |H|.
```

The common dominators form a chain. Between consecutive dominators, an optimum pair uses disjoint noncommon gates. Compatibility can therefore be searched by a four-state DP whose state is the two branch choices at the current common gate.

For each state transition, V113 enumerates the first local branch used by each route, checks that both traversals require the same target at the shared gate, and completes the two tails with an ordinary gate-capacitated two-flow.

Hence, for a fixed initial pair, V113 decides in polynomial time whether **any minimum-overlap route pair is target-compatible**, and constructs a missing output when one exists.

Scanning all repeated-selector first pairs remains polynomial.

## Why this is stronger than V111/V112

- V111 computes one deterministic minimum-overlap flow and succeeds only when that selected decomposition is compatible.
- V112 proves that equal-cost optimum decompositions can disagree on compatibility and solves a serial `k=2` phase-transfer template.
- V113 searches the entire optimum face for every fixed first pair by dominator decomposition; it is not tied to one min-cost-flow representative and is not restricted to the V112 serial support.

## Strict nonserial family

For every `d>=1`, V113 includes a signed MUX family with

```text
n = 7(d+1),
m = n+1,
minimum overlap = d,
beta_V102 = 5(d+1) = 5n/7.
```

Each layer uses two three-variable lobes, so V112's exact two-variable-lobe recognizer rejects the support. The optimum face contains both a compatible and an incompatible route pair with the same overlap `d`; V113 finds a compatible optimum.

## Verification

The primary verifier runs the actual V113 implementation, cross-checks small random fixed pairs against exhaustive path enumeration, checks the strict family, Hall matching controls, exact small backdoor, and malformed inputs.

The independent verifier does not import V113. It independently enumerates gate-simple paths, recomputes common dominators by deletion, reconstructs the strict family, and verifies its missing targets with an independent signed-MUX 2-SAT SCC solver.

## Boundary

V113 settles the `Delta=0` case, where

```text
Delta = minimum_target_compatible_overlap - minimum_overlap.
```

It does **not** prove that every MUX circuit has a compatible optimum. The next residual is `Delta>0`: compatible route pairs may exist only after deliberately sharing extra non-dominator gates.

All-MUX `0x1b`, unrestricted `NC0_3-Avoid`, general circuit lower bounds, and P versus NP remain open. No novelty, priority, or peer-review claim is made.
