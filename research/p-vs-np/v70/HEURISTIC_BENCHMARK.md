# Polynomial-time gate-order heuristic benchmark

V70 compares six deterministic orders:

1. natural order;
2. reverse order;
3. minimum remaining support overlap;
4. frontier greedy — minimize the next support frontier, then future incidence pressure;
5. closure greedy — maximize variables whose last remaining occurrence is processed;
6. support lookahead-2 — inspect every ordered pair of next gates and minimize the maximum frontier and the affine-subspace counting proxy.

All heuristics use only supports and fixed-depth combinatorial calculations. For fixed lookahead depth two, the implementation is polynomial in the number of gates and variables.

## Preserved natural-order records

| n | natural | reverse | min overlap | frontier | closure | lookahead-2 | exact optimum |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 6 | 48 | 20 | 22 | 22 | 22 | 26 | 15 |
| 8 | 99 | 35 | 31 | 31 | 22 | 25 | 15 |
| 10 | 263 | 25 | 42 | 39 | 39 | 33 | 17 |
| 12 | 580 | 67 | 75 | 59 | 59 | 52 | 29 |
| 14 | 583 | 156 | 147 | 41 | 41 | 41 | not computed |

The `n=14` tested upper bound improves from V69's `147` to `41`, with support-frontier width five.

## New finite records

A deterministic exact-objective mutation search starting from the V69 witnesses gives:

```text
n=8:  seed=7008, 30 steps, record at step 26, G*_proj=29
n=10: seed=7010, 45 steps, record at step 43, G*_proj=30
```

Quick verification checks the preserved witnesses and their exact optima. Full verification replays both seeded searches in isolated processes. The independent verifier recomputes each optimum from explicit assignment relations without importing the GF(2) engine.

## Interpretation

Support heuristics strongly repair adversarial fixed orders but do not uniformly approximate `G*_proj` on the robust witnesses. This is evidence for a parameterized and structural algorithm route, not a general polynomial ordering theorem.
