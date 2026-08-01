# V74 finite validation ledger

## Exact local fibers

- 3 affine cells in arity one;
- 11 affine cells in arity two;
- 51 affine cells in arity three;
- all 256 ternary subsets reconstructed exactly;
- minimum affine-partition histogram `1, 51, 196, 8` for zero through three cells;
- the eight three-cell cases are exactly the complements of single points.

## Exhaustive positive-stretch circuits

All circuits with:

```text
n = 2 inputs,
m = 3 output gates,
all gates supported on both inputs,
all 16 binary Boolean truth tables independently allowed
```

were checked. This gives:

```text
16^3 = 4,096 circuits,
4,096 * 8 = 32,768 full target words,
4,096 constructive avoided outputs.
```

For every target, weighted affine counting equaled direct enumeration of all four inputs. Every constructed output had zero direct preimages.

## Seeded ternary circuits

Ninety-six deterministic circuits with three inputs, four ternary gates, arbitrary truth masks, and independent output flips were checked on all 16 target words:

```text
1,536 target-count comparisons,
96 constructive avoided outputs.
```

## Output polarity

All 256 ternary truth tables were checked under output flip one at all eight local points, giving 2,048 direct polarity checks.

## OR-path family

The exact subset table and optimum over all gate orders were computed through nine path edges. Independent permutation optimization was repeated through seven edges. The values agree with:

```text
G*_proj = 1                         for m=1,
G*_proj = 3m-3                      for m>=2.
```

These computations are regression evidence for the proved formula, not the proof itself.
