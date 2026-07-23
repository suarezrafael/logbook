# Laboratory V25 — Four-input zero-set degree

**Status:** computer-assisted open research note; not peer reviewed; novelty and priority are not established; P versus NP is not resolved.

## Main result

V25 exhaustively classifies all 65,536 Boolean functions of four inputs under NPN equivalence: input permutations, input negations, and output complementation.

The 65,536 functions form 222 NPN classes. Over `GF(5)`, after an optional output complement, the minimum multilinear degree of a polynomial whose zero set represents the function is distributed as follows:

| Minimum degree | NPN classes | Truth tables |
|---:|---:|---:|
| 0 | 1 | 2 |
| 1 | 15 | 892 |
| 2 | 199 | 63,362 |
| 3 | 7 | 1,280 |

Thus 215 of the 222 NPN classes, containing 64,256 of the 65,536 truth tables (98.046875%), admit zero-set degree at most two over `GF(5)`.

Only seven balanced NPN classes require degree three. Canonical truth-table masks:

```text
0x017f  0x01bf  0x01ef  0x01fe
0x07f1  0x07f2  0x07f8
```

## Range-avoidance corollary

Let `Q5` be the class of four-input gates with zero-set degree at most two over `GF(5)`. For an `n`-input circuit whose `m` output gates all belong to `Q5`, deterministic range avoidance follows when

```text
m > D2(n) = 1 + n + binom(n,2),
```

or whenever the actual embedded coefficient rank is smaller than `m`.

A nonzero left dependency among the embedded local polynomials yields a solver-free one-violation certificate: request normalized output one on every other dependency-support coordinate and zero at one coordinate. The dependency forces that last polynomial to vanish as well, so the target is outside the range.

## Validation

- 222 independently recomputed NPN classes covering all 65,536 functions;
- all minimum-degree counts independently recomputed over `GF(2)`, `GF(3)`, `GF(5)`, and `GF(7)`;
- exact quadratic-nonexistence certificates for both orientations of all seven hard classes;
- 100 complete circuit certificates checked by exhaustive input enumeration;
- zero discrepancies.

## Scope

This is a substantial extension beyond symmetric gates: 205 of the 215 quadratic NPN classes have no symmetric representative. The sufficient stretch remains quadratic, and adversarial circuits may consist entirely of the seven cubic classes. The result does not solve general `NC0_4-Avoid`, prove an unrestricted circuit lower bound, or resolve P versus NP.

Files in this directory provide the proof statement, compact machine-readable results, and an independent verification entry point.