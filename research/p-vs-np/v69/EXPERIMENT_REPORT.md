# V69 order-robustness experiments

## Natural-order adversarial search

A deterministic hill climber mutates ordered supports and one of the three affine-cell partitions of the positive `0x07` fiber. It optimizes only the natural order. The preserved records are:

| n | m | natural `G_proj` | best simple heuristic | exact `G*_proj` |
|---:|---:|---:|---:|---:|
| 6 | 7 | 48 | 20 | 15 |
| 8 | 9 | 99 | 31 | 15 |
| 10 | 11 | 263 | 25 | 17 |
| 12 | 13 | 580 | 67 | 29 |
| 14 | 15 | 583 | 147 | not computed |

The exact values use the subset-lattice algorithm. The `n=14` row is reported only with explicit heuristic upper bounds.

## Search directly against the optimum

A second, smaller search maximizes exact `G*_proj` where exact optimization is cheap enough. The preserved finite witnesses have:

| n | natural `G_proj` | exact `G*_proj` |
|---:|---:|---:|
| 6 | 31 | 20 |
| 8 | 69 | 28 |
| 10 | 56 | 24 |

These are search-budget records, not maxima over all systems. They do not show monotone, polynomial, or superpolynomial asymptotic behavior.

## Interpretation

The large natural-order values are not robust on the exactly checked witnesses: order optimization reduces `48 -> 15`, `99 -> 15`, `263 -> 17`, and `580 -> 29`. Thus a lower bound for one fixed order is insufficient for the algorithmic question.

The remaining target is either a constructible polynomial-quality ordering theorem or an explicit family whose `G*_proj` is superpolynomial, requiring a genuine all-orders argument.
