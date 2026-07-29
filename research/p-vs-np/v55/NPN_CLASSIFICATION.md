# Ternary NPN classification and V55 routes

| Canonical | Orbit | Essential arity | Affine orientation | Route |
|---|---:|---:|---|---|
| `0x00` | 2 | 0 | full cube | trivial constant |
| `0x01` | 16 | 3 | singleton | affine blocks for `m>n+1`; V54 stronger in coherent regimes |
| `0x03` | 24 | 2 | adjacent pair | reduces to `NC0_2` |
| `0x06` | 24 | 3 | distance-two pair | affine blocks for `m>n+1` |
| `0x07` | 48 | 3 | none | frontier |
| `0x0f` | 6 | 1 | literal hyperplane | trivial / `NC0_1` |
| `0x16` | 16 | 3 | none | frontier |
| `0x17` | 8 | 3 | none | frontier; monotone representative, arbitrary NPN polarities not covered |
| `0x18` | 8 | 3 | antipodal pair | stretch-one affine-block algorithm |
| `0x19` | 48 | 3 | none | frontier |
| `0x1b` | 24 | 3 | none | frontier |
| `0x1e` | 24 | 3 | none | frontier |
| `0x3c` | 6 | 2 | binary-parity hyperplane | reduces to `NC0_2` |
| `0x69` | 2 | 3 | ternary-parity hyperplane | affine output rank for `m>n` |

## Geometry of two-point fibers

- Distance one (`0x03`): one coordinate is free and two fixed, so the gate is effectively binary.
- Distance two (`0x06`): one literal is fixed and one parity relation links the other two; genuinely ternary, solved here for `m>n+1`.
- Distance three (`0x18`): the assignments are complements; both defining parity equations have even coefficients, yielding the stretch-one theorem.

## Remaining finite frontier

```text
0x07, 0x16, 0x17, 0x19, 0x1b, 0x1e.
```

V56 will seek finite-state forcing systems for these six essential non-affine classes.
