# V88 core context — constructivity after the three-certificate obstruction

## Frozen output from V87

1. Direct McDiarmid plus a union bound over all balanced cuts does not close;
   its best possible exponent is below the entropy of the cut family.
2. A random pair inside a random ternary support is an independent uniform
   graph edge.
3. For rank-at-most-three hypergraphs,
   `tw(primal)+1 <= max(3,ceil(3 bw/2))`.
4. The V86 random support model has branchwidth `Omega(n)` with high
   probability.
5. For all sufficiently large `n`, one simple ternary support family
   simultaneously has:
   - no Hall-deficient set below `n/(16e^2)`;
   - no nonzero constant syndrome under `NOR3`;
   - support branchwidth `Omega(n)`.
6. This family is probabilistic and nonexplicit.
7. Linear width is proved for the resistant family, not for every instance in
   the V84 Hall-expander branch.
8. The fixed-cut expectation at the one-third cut is `0.546572...n`, not a
   uniform all-cuts lower bound and not a claimed branchwidth constant.

## Priority one — constructive repeated-table Eval_H

Return to the unresolved constructive problem from V85.

`Eval_H` has repeated truth-table coordinates across witness layers. Exploit
that repetition explicitly rather than treating it as arbitrary
`NC0_11`.

Required deliverables:

- a finite census of affine rank and collision structure across repeated
  layers;
- candidate constructions from diagonal codes, small-bias sets, cyclic
  automorphisms, or tensor products;
- a deterministic list of size `O(n^(1/3))`, or a lower bound in a precisely
  specified constructor model;
- an explicit separation between support-only existence and efficient
  construction.

## Priority two — derandomize the three-certificate obstruction

V87 proves existence but not explicitness.

Seek a deterministic family of simple 3-uniform supports with:

```text
local Hall expansion to a linear scale;
support branchwidth Omega(n);
polynomial-time constructibility.
```

`NOR3` then eliminates constant syndromes automatically.

Possible routes:

- lift explicit constant-degree graph expanders to ternary supports;
- use bipartite lossless expanders with a bounded-degree right side;
- use explicit sparse graphs of linear treewidth as pair shadows;
- preserve support uniqueness during the lift.

Every claimed construction must verify the target stretch
`m=n+ceil(n^(2/3))`, not merely constant-factor stretch.

## Priority three — calibrate the remote-point bridges

Complete the quantitative ledger postponed from V86:

- exact distance and dimension required by the APY rigidity bridge;
- exact parameters in Huang-Li-Zhong average-case hardness bridges;
- uniformity and oracle requirements;
- multiplicative and exponent gaps from the V85 guarantee.

Do not convert `Omega(n^(2/3)/log n)` into a qualitative claim of proximity.

## Priority four — bounded arithmetic

Formalize one complete certificate chain in a weak theory:

1. V86 `NOR3` unique cubic pivot;
2. V87 rank-three transfer lemma;
3. V75/V85 pair-count conservation;
4. the prefix pigeonhole step.

Record exactly where `PV`, `PV_1`, or `APC^1` is needed.

## Priority five — proof-complexity parameter matching

Continue only when all of the following match:

```text
predicate, encoding, generator, field, proof system,
expansion notion, parameter scale, and target stretch.
```

The V87 family supplies a genuinely simultaneous obstruction to the current
algorithmic certificates. It does not automatically inherit a lower bound in
any proof system.

## Stop conditions

V88 is promotable if it delivers any one of:

1. a constructive repeated-table `Eval_H` candidate list;
2. a rigorous constructor-model lower bound;
3. an explicit deterministic three-certificate obstruction family;
4. a complete quantitative remote-point bridge ledger;
5. a verified bounded-arithmetic formalization boundary.

## Nonclaims

No direct route to `P != NP` is active. V88 begins after an existential
obstruction theorem, not after an avoidance algorithm or a circuit lower
bound.
