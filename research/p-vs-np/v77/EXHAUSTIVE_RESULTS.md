# V77 finite validation ledger

## Static topology hierarchy

All ordered full binary source shapes with two through nine leaves were
converted to subcubic unrooted source trees and processed by the deterministic
certificate constructor.

```text
ordered source shapes:       2,055
source vertices:             31,042
topology clusters:           73,239
retained label clusters:     33,097
maximum topology height:     6
maximum retained height:     4
retained degree-three:       0
```

Boundary-edge histogram over all topology clusters:

```text
0 edges:  2,055
1 edge:  36,356
2 edges: 18,514
3 edges: 16,314
```

Every degree-three cluster was a singleton, as required. After pruning to gate
labels, the histogram was:

```text
0 edges:  2,055
1 edge:  27,861
2 edges:  3,181
3 edges:      0
```

## Seeded transfer audit

With seed `770077`, 256 rank-at-most-three support systems were tested on
balanced and adversarial source trees. The audit reconstructed source middle
sets from raw leaf sides and checked every retained cluster boundary directly.

```text
systems:                    256
retained records checked: 5,132
maximum cover edges:          2
```

No transferred cluster exceeded twice the supplied source width.

## Two-edge tightness witness

A four-leaf quartet with supplied width `b=3` has a valid cluster whose two
boundary-edge middle sets are disjoint blocks of size three. Its support
boundary has size six. Therefore the two-edge cover inequality can attain
`2b` for one cluster. This does not prove a global factor-two lower bound.

## Five-variable isomorphism audit

The universe contains 25 nonempty supports of rank at most three. All simple
families through six gates were reduced under all 120 variable permutations.

| gates | raw families | isomorphism orbits | perfect-height inflations |
|---:|---:|---:|---:|
| 1 | 25 | 3 | 0 |
| 2 | 300 | 12 | 0 |
| 3 | 2,300 | 50 | 0 |
| 4 | 12,650 | 193 | 0 |
| 5 | 53,130 | 648 | 0 |
| 6 | 177,100 | 1,896 | 0 |
| **total** | **245,505** | **2,802** | **0** |

This extends the exact Pareto audit beyond four variables. The absence of a
small perfect-height inflation here is finite evidence only.

## V76 witness regression

All six seven-gate V76 witnesses retain exact minimum width two and minimum
perfect-height width three. Their finite statement remains valid and is
compatible with the V77 `2b` theorem because V77 promises `O(log m)` height,
not the minimum possible height.
