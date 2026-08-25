# V117 frozen core context — XP versus FPT beyond one feedback gate

## Inherited facts

V113 completely decides target compatibility on the minimum-overlap face for each fixed opposite-phase signed-MUX first pair.

V114 rules out a generic unrestricted one-extra completion oracle by an NP-complete directed-linkage reduction, but does not prove `Delta=1` hardness.

V115 decides `Delta<=1` in polynomial time when all non-common dominator stages are DAGs.

V116 extends that theorem to the first genuinely cyclic class: every non-common stage may have feedback-gate number at most one. After fixing the feedback gate and optional unique extra shared gate, the two routes reduce to at most five fixed requests in a DAG, solved by a product-state token DP.

## Immediate parameterized observation

Suppose a stage is supplied with a feedback-gate set `F` of size `tau`. A gate-simple route visits each member of `F` at most once. Enumerating the subsets/orders/branches used by the two routes and the optional unique extra shared gate leaves a DAG and `O(tau)` residual source-target requests.

The direct product-state extension therefore gives only

```text
N^O(tau)
```

(up to the enumeration of feedback-gate orders): an XP algorithm, not an FPT algorithm.

This is not a cosmetic distinction. Generic directed disjoint-path routing on DAGs is W[1]-hard when parameterized by the number of requests (Slivkins 2010, with later strengthenings). V117 may not relabel the variable-dimensional product DP as `f(tau) poly(N)`.

## V117 primary question

Does the residual linkage created by **two original gate-simple routes cut at a feedback set** have enough ordered structure to evade generic DAG multi-request hardness?

The residual requests are not arbitrary: they occur as two ordered chains, one per original return route, and the chain endpoints are feedback-gate selectors/data destinations plus the stage boundaries.

### Track A — two-chain DAG linkage compression

Define the residual problem explicitly:

```text
TWO-CHAIN-GATE-LINKAGE-DAG
```

Input: a DAG with gate resources and two ordered chains of terminal pairs. Decide whether all pairs can be linked by globally gate-disjoint directed paths, respecting each chain order.

Try to prove an FPT algorithm parameterized by the total number of chain breakpoints using:

- interval/frontier states rather than one token coordinate per request;
- representative sets / important separators on the two chains;
- a bounded antichain of reachable frontier pairs;
- dominance compression using the shared stage topological order.

A true bridge would replace `N^O(tau)` with `f(tau) poly(N)`.

### Track B — hardness of the two-chain residual problem

Attempt a parameterized reduction from the known W[1]-hard DAG disjoint-path problem into TWO-CHAIN-GATE-LINKAGE-DAG while preserving the two-chain endpoint order. If successful, the naive feedback-set route cannot be made FPT without additional signed-MUX structure.

Do not import generic W[1]-hardness unless the two-chain restriction is actually preserved by the reduction.

### Track C — first constant beyond V116

As a control, implement `tau<=2`. The direct method has constant residual request count and is polynomial, so it should be mechanically feasible. This is useful for falsification and for discovering interface patterns, but by itself it is a weaker conceptual advance because every fixed constant `tau` is already suggested by the XP observation.

Promote a `tau<=2` laboratory only if it exposes a new compression invariant or an infinite family that falsifies a plausible FPT lemma.

### Track D — strengthen hardness at small cyclic parameter

Try to adapt the V114 linkage gadget so the V113 optimum face rejects and the source hardness is carried by a stage with a very small feedback-gate set. A proof of NP-hardness at a fixed `tau` would contradict the polynomial fixed-constant decomposition above, so any such attempt must first identify exactly which V116 assumption fails. More plausible targets are W[1]-hardness parameterized by `tau` or hardness when the feedback set is not supplied/structurally localized.

## Promotion rule

V117 is promotable only with at least one of:

- an FPT theorem `f(tau) poly(N)` exploiting the two-chain residual structure, with implementation and independent verification;
- a correct W[1]-hardness reduction for the two-chain residual problem or the signed-MUX feedback-gate parameter;
- a rigorous structural compression theorem that reduces the residual interface to `f(tau)` representatives and materially advances an FPT proof;
- a different externally recognized barrier that decisively closes the XP-to-FPT route.

A larger fixed-`tau` implementation or larger finite census alone is not promotable.

## Global boundary

Even an FPT result in feedback-gate number does not solve all MUX `0x1b` unless that parameter is bounded universally or coupled to a universal kernel. Unrestricted `NC0_3-Avoid`, general circuit lower bounds, and P versus NP remain open.
