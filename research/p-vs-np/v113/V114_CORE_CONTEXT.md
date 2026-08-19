# V114 frozen core context — excess-compatible overlap

## Inherited result

V113 decides the entire **minimum-overlap face** for every fixed opposite-phase repeated-selector MUX first pair.

For return destinations `d0,d1` to root selector `v`, let `H` be the common gate dominators. V113 proves

```text
minOverlap(d0,d1;v) = |H|.
```

A four-state DP over the ordered dominator chain decides whether any optimum pair is target-compatible. Thus the fixed-pair `Delta=0` case is closed, where

```text
Delta = minCompatibleOverlap - minOverlap.
```

The remaining obstruction is genuinely `Delta>0`: all optimum pairs can be target-incompatible even though a compatible pair may exist after deliberately sharing extra non-dominator gates.

## V114 primary question

Does bounded excess overlap give an FPT avoider?

Target theorem form:

```text
Given k, decide whether a fixed first pair has a target-compatible return pair
with overlap <= minOverlap + k in f(k) poly(N) time, and construct a missing word.
```

The first concrete target is `f(k)=c^k` for a small constant `c`.

## Track A — promote extra shared gates into temporary dominators

A compatible pair of overlap `|H|+k` shares a set `X` of at most `k` non-dominator gates in addition to `H`.

For a guessed `X`, give gates in `H union X` capacity two and all others capacity one. Seek a state-space description that determines target compatibility on `H union X` without enumerating complete routes.

Key question: can `X` be branched from a polynomial-size obstruction returned when the V113 optimum-face DP rejects?

## Track B — conflict-directed branching

When the V113 DP has no accepting path, extract a smallest phase conflict between dominator intervals. Determine whether every compatible higher-overlap pair must share at least one gate from a polynomially bounded conflict set `S`.

If yes, branch on `g in S` as an additional allowed shared gate and decrement the excess budget.

Desired recurrence:

```text
T(k) <= |S| T(k-1) + poly(N)
```

with `|S|=O(1)` or otherwise parameter-controlled.

## Track C — exact small-instance census for Delta

For `n<=6` signed MUX circuits, enumerate gate-simple return pairs for fixed opposite-phase first pairs and record

```text
minOverlap,
minCompatibleOverlap,
Delta,
common dominators,
phase-conflict signatures.
```

Use the census only to discover candidate obstruction rules. Do not promote a finite census by itself.

Priority questions:

1. Does `Delta=1` occur?
2. Is `Delta` unbounded on connected exact-stretch families?
3. When `Delta=1`, is there always one extra shared gate lying in a small separator or exchange cycle associated with the rejected optimum face?
4. Can a compatible pair require sharing a gate that is not on any minimum-overlap route?

## Track D — hardness falsification

Because forbidden-pair/path-selection problems can be NP-hard, test whether deciding existence of a target-compatible route pair with unrestricted excess can encode a known hard two-path problem.

Do not infer hardness from analogy. Require an explicit reduction respecting signed MUX branch semantics and exact positive stretch before recording a barrier theorem.

## Strict promotion rule

V114 is promotable only with at least one of:

- a proved FPT algorithm parameterized by `Delta` (or an explicit upper budget `k`) with a scalable separation family;
- a polynomial theorem for the full `Delta<=1` class with an infinite family beyond V113;
- an explicit hardness/barrier reduction for unrestricted compatible-overlap selection that materially redirects the program.

Larger brute-force tables, more random evidence, or another narrow serial template are not sufficient.

## Global boundary

Even a successful `Delta`-FPT theorem would not by itself prove all MUX `0x1b` circuits are in P unless `Delta=O(log N)` or otherwise structurally bounded for every residual circuit. Unrestricted `NC0_3-Avoid` and P versus NP remain open.
