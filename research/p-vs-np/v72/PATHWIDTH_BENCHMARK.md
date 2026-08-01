# Pathwidth-order benchmark on preserved V69–V70 records

V72 computes an exact minimum vertex-separation order of the primal graph, converts it to a path decomposition, and orders each gate by the rightmost bag containing its support. V71 proves that the resulting gate order has frontier width at most `pathwidth+1`.

The table compares this constructible support-only order with the exact preserved projected-DAG optimum `G*_proj`.

| Record | primal pathwidth | path-order frontier | path-order `G_proj` | exact `G*_proj` | ratio |
|---|---:|---:|---:|---:|---:|
| V69 natural `n=6` | 4 | 4 | 21 | 15 | 1.400 |
| V69 natural `n=8` | 4 | 5 | 28 | 15 | 1.867 |
| V69 natural `n=10` | 4 | 5 | 35 | 17 | 2.059 |
| V69 natural `n=12` | 4 | 5 | 57 | 29 | 1.966 |
| V70 exact-objective `n=8` | 4 | 5 | 40 | 29 | 1.379 |
| V70 exact-objective `n=10` | 4 | 5 | 50 | 30 | 1.667 |

All six path-derived orders satisfy the V71 width guarantee. On this fixed finite corpus, their `G_proj` values are at most `2.1` times the exact objective.

## Width objective versus residual objective

Minimizing maximum frontier width is not the same optimization problem as minimizing the total number of projected residual states. For example, on the V70 `n=10` exact-objective record, the deterministic exact linear-width order selected by the V72 tie rule has

```text
frontier width = 5,
G_proj = 61,
```

while the pathwidth-derived order has

```text
frontier width = 5,
G_proj = 50,
```

and the exact residual objective is

```text
G*_proj = 30.
```

This is a finite objective-mismatch witness. It does not show that every width-optimal order is poor, nor does it provide an approximation lower bound.

## Reproducibility

The benchmark reads the frozen specifications from

- `../v69/seed_data.json`, and
- `../v70/SEARCH_SPEC.json`.

The exact pathwidth order is computed by an `O(n 2^n)` vertex-separation DP. The gate order is reconstructed from the resulting path decomposition and evaluated by the V68–V70 projected affine residual engine.

## Interpretation

The experiment supports pathwidth as a useful constructible proxy, while also showing that a sharper algorithm should optimize residual-state cost inside the set of low-frontier orders. No asymptotic approximation factor is claimed from six instances.
