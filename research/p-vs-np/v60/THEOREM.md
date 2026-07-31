# V60 theorem statement

## Theorem 1 — Las Vegas avoidance in the easy-membership regime

Let

```text
C : {0,1}^n -> {0,1}^m
```

be any function with `m>n`. Assume there is a deterministic polynomial-time algorithm deciding, for an arbitrary `y in {0,1}^m`, whether `y` belongs to `Range(C)`.

Then Range Avoidance for `C` has a Las Vegas algorithm whose expected number of membership tests is at most

```text
1 / (1 - 2^(n-m)).
```

In particular, because `m>n`, the expected number of tests is at most two.

### Algorithm

Repeat:

1. sample `y` uniformly from `{0,1}^m`;
2. run the image-membership algorithm on `y`;
3. return `y` if it is not in `Range(C)`.

The algorithm never returns an incorrect answer.

## Corollary 2 — Bijunctive local fibers

Whenever membership in the circuit image is expressible and decidable by a polynomial-size 2-SAT instance, the theorem gives an expected-polynomial-time randomized range-avoidance algorithm for every positive stretch `m>n`.

This corollary applies to the easy-membership regime isolated in V57–V59. It does not give a deterministic algorithm.

## Tightness of the trial bound

At stretch one, `m=n+1`, an injective circuit has image size `2^n`, exactly half of the output cube. The success probability is then exactly `1/2`, so the expected number of independent trials is exactly two.

## Program-level interpretation

The following is a research-management conclusion, not a complexity-theoretic theorem:

> In a subclass where image membership is polynomial-time and positive stretch is guaranteed, randomized avoidance is already elementary. Further work in that subclass should be framed as deterministic derandomization, structural classification or local-circuit geometry, rather than as direct progress toward P versus NP without an additional reduction.
