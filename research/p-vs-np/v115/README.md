# V115 — DAG-stage budget-one repair for signed MUX

V115 continues the V113/V114 signed-MUX line at the first positive excess-overlap budget.

V113 proves that for a fixed opposite-phase first pair the minimum return-gate overlap equals the number of common gate dominators and decides target compatibility on that complete minimum-overlap face. V114 shows that leaving the optimum face by guessing an arbitrary extra shared gate leads to an NP-complete completion problem in general directed return graphs.

V115 isolates a nontrivial tractable boundary between these results.

## Main result

Fix an opposite-phase first pair. Compute the V113 common gate-dominator chain and partition the remaining return gates into the induced dominator stages. If every non-common stage branch graph is acyclic, then one can decide in polynomial time whether there is a target-compatible return pair with

```text
overlap <= minimum_overlap + 1.
```

The algorithm either returns a compatible minimum-overlap certificate, a compatible certificate with exactly one extra shared non-dominator gate, or `None` inside the stated all-DAG-stage class.

The key lemma is a prefix/suffix separation property. In an acyclic stage, once two routes share the unique extra gate `g`, no gate used before `g` on either route can reappear after `g` on either route; such a reuse would create a directed cycle. Consequently, for fixed `g` and its two branch choices, the prefixes into `g` and suffixes out of `g` can be solved by independent unit-capacity gate-flow computations and safely concatenated.

The V113 four-state phase DP then gains one budget bit recording whether the unique extra gate has already been spent.

## Strict separation family

`strict_dag_delta_one_family(depth)` gives, for every integer `depth >= 0`, an essential signed-MUX circuit with

```text
n = 8 + depth,
m = 9 + depth = n + 1,
minimum_overlap = 1,
minimum_target_compatible_overlap = 2,
Delta = 1.
```

The fixed first pair is rejected by the V113 optimum-face algorithm but accepted by the V115 budget-one algorithm. Every non-common stage is acyclic. Thus the new theorem is not a restatement of V113.

## Verification

The primary verifier cross-checks the algorithm against direct gate-simple route enumeration on seeded small exact-stretch instances in the all-DAG-stage class and checks the infinite family over a fixed reproducible depth range.

The independent verifier imports no V115 implementation. It reconstructs the strict family, route semantics, target compatibility, DAG property and a full-image control directly.

Finite testing is falsification evidence only. The theorem rests on the dominator decomposition, the acyclic prefix/suffix separation lemma, and the finite-state phase composition argument.

## Boundary

V115 does not handle a cyclic non-common stage. This restriction is material: V114 shows that unrestricted directed extra-overlap completion already contains a directed two-linkage hardness barrier.

V115 does not prove all signed-MUX / bijunctive `0x1b` avoidance is polynomial time, does not solve unrestricted `NC0_3-Avoid`, does not establish a general circuit lower bound, and does not resolve P versus NP. Novelty is not claimed pending external review.
