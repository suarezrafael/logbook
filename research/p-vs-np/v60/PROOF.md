# Proof of the V60 easy-membership theorem

Let `S=Range(C)`. A function on `n` Boolean inputs has at most `2^n` distinct outputs, hence

```text
|S| <= 2^n.
```

A uniformly sampled `m`-bit word lies in the image with probability

```text
Pr[y in S] = |S| / 2^m <= 2^n / 2^m = 2^(n-m).
```

Therefore one trial returns a missing output with probability

```text
p = Pr[y not in S] >= 1 - 2^(n-m).
```

Because `m>n`, we have `n-m <= -1`, and thus

```text
p >= 1/2.
```

Independent repetition until success is a geometric random variable with expectation `1/p`. Consequently,

```text
E[T] <= 1 / (1 - 2^(n-m)) <= 2.
```

The membership algorithm certifies every returned word as outside `S`, so the procedure is Las Vegas: its running time is random, but its answer is always correct. If one membership test runs in polynomial time, the expected total running time is polynomial.

## Tightness

For `m=n+1`, let `C` be injective. Then `|S|=2^n=2^(m-1)`, so exactly half of the output cube is absent. Each trial succeeds with probability exactly `1/2`, giving `E[T]=2`.

## Why this does not derandomize V58

V58 begins from a specified image point or orientation and searches deterministically for a nearby boundary witness. The theorem above ignores that starting point and samples the whole output cube. It therefore does not construct a deterministic walk, bound orientation depth, or identify a canonical absent word.

## Why the isoperimetric result remains mathematically valid

V59's boundary theorem describes the geometry of `S` under uniform sampling from the image. The V60 algorithm samples uniformly from the ambient output cube. The latter is simpler when membership is easy, but it does not invalidate the boundary theorem or its structural interpretation.
